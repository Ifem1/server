#!/usr/bin/env node
// Do not permit deployment to an endpoint other than stable StudioNet chain 61999.
const RPC = 'https://studio.genlayer.com/api';
const EXPECTED = 61999;
try {
  const response = await fetch(RPC, {
    method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({jsonrpc:'2.0',id:19,method:'eth_chainId',params:[]}),
    signal:AbortSignal.timeout(15000)
  });
  if (!response.ok) throw new Error(`RPC HTTP ${response.status}`);
  const body = await response.json();
  if (body.error || typeof body.result !== 'string') throw new Error('chain ID unavailable');
  const chain=Number.parseInt(body.result,16);
  if (chain!==EXPECTED) throw new Error(`wrong chain ID ${chain}; expected ${EXPECTED}`);
  console.log(`Verified StudioNet ${EXPECTED}: ${RPC}`);
} catch(err) {
  console.error(`Refusing deployment: ${err.message}`);
  process.exitCode=1;
}
