#!/usr/bin/env node
// Explicit operator consent required. Repository-local CLI only.
import {spawnSync} from 'node:child_process';
import {existsSync,readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {stdin as input,stdout as output} from 'node:process';
import readline from 'node:readline/promises';
const root=resolve(import.meta.dirname,'..');
const cli=resolve(root,'node_modules','genlayer','dist','index.js');
const rpc='https://studio.genlayer.com/api';
function cliCall(args){
  const p=spawnSync(process.execPath,[cli,...args],{cwd:root,encoding:'utf8',stdio:'inherit'});
  if(p.status!==0) throw new Error(`GenLayer CLI failed: ${args.join(' ')}`);
}
try {
  if(!existsSync(cli)) throw new Error('Missing repository-local CLI: run npm install');
  const manifest=JSON.parse(readFileSync(resolve(root,'package.json'),'utf8'));
  if(manifest.devDependencies?.genlayer!=='0.39.1') throw new Error('CLI pin changed');
  const v=spawnSync(process.execPath,[cli,'--version'],{cwd:root,encoding:'utf8'});
  const vs=(v.stdout||'')+' '+(v.stderr||'');
  if(v.status!==0||!/(^|\D)0\.39\.1(\D|$)/.test(vs)) throw new Error('Require GenLayer CLI exactly 0.39.1');
  const rpcRes=await fetch(rpc,{method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({jsonrpc:'2.0',id:21,method:'eth_chainId',params:[]}),
    signal:AbortSignal.timeout(15000)});
  if(!rpcRes.ok) throw new Error(`RPC HTTP ${rpcRes.status}`);
  const chain=await rpcRes.json();
  if(chain.error||Number.parseInt(chain.result,16)!==61999) throw new Error('Wrong/unavailable StudioNet chain ID');
  cliCall(['network','set','studionet']);
  cliCall(['network','info']);
  const rl=readline.createInterface({input,output});
  const choice=await rl.question('You are deploying SEVER to StudioNet chain 61999. Type DEPLOY-61999: ');
  rl.close();
  if(choice.trim()!=='DEPLOY-61999') throw new Error('Not confirmed; nothing deployed');
  cliCall(['deploy','--contract','contracts/sever.py','--rpc',rpc]);
} catch(err){ console.error(err.message);process.exitCode=1; }
