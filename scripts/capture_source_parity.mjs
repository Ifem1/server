import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const rpc = 'https://studio.genlayer.com/api';
const expectedChainId = 61999;
const contracts = [
  {
    name: 'sever',
    address: process.env.SEVER_ADDRESS || '0x631fF4E9C44f8AD5496Ea5EeC10B3c476aA0c1CD',
    local: 'contracts/sever.py',
  },
  {
    name: 'consumer',
    address: process.env.CONSUMER_ADDRESS || '0xf2DE8057a2416307C7F77cd62365E15E8A880caA',
    local: 'contracts/sever_consumer_example.py',
  },
];

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function normalizedLf(bytes) {
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  return Buffer.from(`${text.replace(/\r\n/g, '\n').replace(/\n+$/, '')}\n`, 'utf8');
}

async function rpcCall(id, method, params) {
  const response = await fetch(rpc, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id, method, params }),
    signal: AbortSignal.timeout(20000),
  });
  if (!response.ok) throw new Error(`${method}: HTTP ${response.status}`);
  const body = await response.json();
  if (body.error) throw new Error(`${method}: ${JSON.stringify(body.error)}`);
  return body.result;
}

const chain = Number.parseInt(await rpcCall(1, 'eth_chainId', []), 16);
if (chain !== expectedChainId) {
  throw new Error(`Refusing source capture: chain ${chain}, expected ${expectedChainId}`);
}

const root = process.cwd();
const outputDirectory = resolve(root, 'artifacts', 'onchain-source');
await mkdir(outputDirectory, { recursive: true });
const entries = [];
for (const [index, contract] of contracts.entries()) {
  const encoded = await rpcCall(index + 2, 'gen_getContractCode', [contract.address]);
  if (typeof encoded !== 'string') throw new Error(`${contract.name}: source result is not base64 text`);
  const deployed = Buffer.from(encoded, 'base64');
  if (deployed.length === 0) throw new Error(`${contract.name}: empty source result`);
  const local = await readFile(resolve(root, contract.local));
  const deployedPath = resolve(outputDirectory,
    `${contract.name}-${contract.address.slice(2).toLowerCase()}.py`);
  await writeFile(deployedPath, deployed);
  const deployedLf = normalizedLf(deployed);
  const localLf = normalizedLf(local);
  entries.push({
    name: contract.name,
    address: contract.address,
    local_path: contract.local,
    retrieved_path: `artifacts/onchain-source/${contract.name}-${contract.address.slice(2).toLowerCase()}.py`,
    deployed_original_bytes: deployed.length,
    local_original_bytes: local.length,
    deployed_sha256_original_bytes: sha256(deployed),
    local_sha256_original_bytes: sha256(local),
    deployed_sha256_lf_normalized: sha256(deployedLf),
    local_sha256_lf_normalized: sha256(localLf),
    exact_original_bytes_match: deployed.equals(local),
    lf_normalized_bytes_match: deployedLf.equals(localLf),
  });
}

const report = {
  rpc,
  chain_id: chain,
  captured_at_utc: new Date().toISOString(),
  head_commit: execFileSync('git', ['rev-parse', 'HEAD'], {
    encoding: 'utf8',
    env: {
      ...process.env,
      GIT_CONFIG_COUNT: '1',
      GIT_CONFIG_KEY_0: 'safe.directory',
      GIT_CONFIG_VALUE_0: root,
    },
  }).trim(),
  working_tree_dirty: execFileSync('git', ['status', '--porcelain'], {
    encoding: 'utf8',
    env: {
      ...process.env,
      GIT_CONFIG_COUNT: '1',
      GIT_CONFIG_KEY_0: 'safe.directory',
      GIT_CONFIG_VALUE_0: root,
    },
  }).trim().length > 0,
  contracts: entries,
};
await writeFile(resolve(root, 'artifacts', 'source-parity-report.json'), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));
