#!/usr/bin/env node
// Deploy the consumer only after a real agreement has been sealed and certified.
// Requires explicit operator consent and a fresh StudioNet chain-ID check.
import {spawnSync} from 'node:child_process';
import {existsSync,readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {stdin as input,stdout as output} from 'node:process';
import readline from 'node:readline/promises';

const root=resolve(import.meta.dirname,'..');
const rpc='https://studio.genlayer.com/api';
const cli=resolve(root,'node_modules','genlayer','dist','index.js');
function cliCall(args){
  const p=spawnSync(process.execPath,[cli,...args],{cwd:root,encoding:'utf8',stdio:'inherit'});
  if(p.status!==0) throw new Error(`GenLayer CLI failed: ${args.join(' ')}`);
}
try {
  if(!existsSync(cli)) throw new Error('Missing repository-local CLI: run npm ci');
  const manifest=JSON.parse(readFileSync(resolve(root,'package.json'),'utf8'));
  if(manifest.devDependencies?.genlayer!=='0.39.1') throw new Error('CLI pin changed');
  const v=spawnSync(process.execPath,[cli,'--version'],{cwd:root,encoding:'utf8'});
  if(v.status!==0||!/(^|\D)0\.39\.1(\D|$)/.test((v.stdout||'')+' '+(v.stderr||'')))
    throw new Error('Require GenLayer CLI exactly 0.39.1');
  const sever=process.env.SEVER_ADDRESS||'';
  const agreement=process.env.AGREEMENT_ID||'';
  const clause=process.env.CLAUSE_ID||'';
  const genesis=process.env.GENESIS_HASH||'';
  if(!/^0x[0-9a-fA-F]{40}$/.test(sever)) throw new Error('SEVER_ADDRESS must be a deployed 20-byte contract address');
  if(!/^[1-9][0-9]*$/.test(agreement)||!Number.isSafeInteger(Number(agreement))) throw new Error('AGREEMENT_ID must be a positive safe integer');
  if(!/^[1-9][0-9]*$/.test(clause)||!Number.isSafeInteger(Number(clause))) throw new Error('CLAUSE_ID must be a positive safe integer');
  if(!/^[0-9a-f]{64}$/.test(genesis)) throw new Error('GENESIS_HASH must be the lowercase 64-character sealed agreement hash');
  const response=await fetch(rpc,{method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({jsonrpc:'2.0',id:22,method:'eth_chainId',params:[]}),signal:AbortSignal.timeout(15000)});
  if(!response.ok) throw new Error(`RPC HTTP ${response.status}`);
  const chain=await response.json();
  if(chain.error||Number.parseInt(chain.result,16)!==61999) throw new Error('Wrong/unavailable StudioNet chain ID');
  cliCall(['network','set','studionet']);
  cliCall(['network','info']);
  const rl=readline.createInterface({input,output});
  const choice=await rl.question('You are deploying the pinned consumer to StudioNet chain 61999. Type DEPLOY-61999: ');
  rl.close();
  if(choice.trim()!=='DEPLOY-61999') throw new Error('Not confirmed; nothing deployed');
  cliCall(['deploy','--contract','contracts/sever_consumer_example.py','--rpc',rpc,
    '--args',sever,agreement,clause,genesis]);
} catch(err){ console.error(err.message); process.exitCode=1; }
