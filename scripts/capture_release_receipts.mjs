import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';

const endpoint = 'https://studio.genlayer.com/api';
const entries = [
  ['Corrected Sever deployment', '0x5cc3de50b3368f91bbda5916fceb2efa58f7bfaa85e2dd5e82b536247879cdcf'],
  ['Lifecycle A graph finalization', '0x547aeeecdb62bef90e57107b723f3425e6950565ab94a94233981668fc995101'],
  ['Lifecycle A consumer deployment', '0x1899a02be92dd645a247a35982afd57f6c655818ab32a9f05b57144eeb612c01'],
  ['Lifecycle A consumer accepted action', '0x65607e499f6d77d052c7fdbf09b40606646a2d3cb02fad062eab51f7940ae93f'],
  ['Lifecycle A invalidation proposal', '0xb654593592e608f96c463dda26b8f91a84833afb9df9dffb5fa1dea22d3250b0'],
  ['Lifecycle A invalidation endorsement', '0x6f9faa173395d3e7463ac331081177e21bf1249cb48de0d1335d81c2b8312b36'],
  ['Lifecycle A invalidation finalization', '0x84d501aefa3265029d22bbc6f95ed4e8ce95c9d16bdc4bb6cc57d51ff4526b27'],
  ['Lifecycle A consumer rejected action', '0x85fe4ee6bdcd33acc475c1f4839c40e3f3af9dac6aa660617a66cdd096ae8a57'],
  ['Lifecycle B agreement 3 creation', '0xe89d0a0e2b5459f9ffdfbd9a94a9ef9733f7d15ba48dd3ff2d3680b8268b9219'],
  ['Lifecycle B agreement 3 first directed pair', '0xa89d65b0de8d8160533d054f2caeffdff2eb9071c0b39f6f2596b8b84cc3cfb5'],
  ['Lifecycle B agreement 3 second directed pair', '0x2f8511b5f62c9ce7f740046171d378a797e7d78dd1516d8bc6c18e7d367b02c3'],
  ['Lifecycle B graph finalization', '0xad790fc5fff990d7b2d2c9f13621d92b0100a7e15ea1e896bce88f4411c9f60d'],
  ['Lifecycle B essential invalidation proposal', '0xc7bfc1ca810ab9ea1afedcca5b3eef491212901e523815d526fb2cbb61adbcb6'],
  ['Lifecycle B second-party endorsement', '0x1a0310ce88fc0510d13965e68a1f26f00d330cc09026c733c7599067c3e4408d'],
  ['Lifecycle B duplicate endorsement rejected', '0x277f1c97ec6f018a84da9365b0afc97b73df73c8114e1422b1f46def3671696b'],
  ['Lifecycle B essential invalidation finalization', '0xd0eb27dcebfa5a5595b86bee42fbd13a6964a112a3fe5bc206d0f124a0a2f586'],
  ['Lifecycle B consumer deployment', '0x1ab7bf52b48c88df5d929c90d8559776b08927c06b50a918f07dcc01805651b6'],
  ['Lifecycle B collapsed-consumer rejected action', '0x4e665162558c1f876e8911aedb1be3e772a4f390a19e89170665b662fba5dfd6'],
];

const client = createClient({ chain: studionet, endpoint });
const chainId = await client.getChainId();
if (chainId !== 61999) throw new Error(`Wrong chain ${chainId}`);
const transactions = [];
for (const [label, hash] of entries) {
  const receipt = await client.getTransaction({ hash });
  const leader = (receipt.consensus_data?.leader_receipt || []).find((x) => x.mode === 'leader');
  const votes = receipt.consensus_data?.votes || {};
  const voteCounts = {};
  for (const vote of Object.values(votes)) voteCounts[vote] = (voteCounts[vote] || 0) + 1;
  transactions.push({
    label,
    transaction_hash: hash,
    explorer_url: `https://explorer-studio.genlayer.com/tx/${hash}`,
    status: receipt.statusName,
    consensus_result: receipt.result_name,
    leader_execution_result: leader?.execution_result ?? null,
    genvm_error_code: leader?.genvm_result?.error_code ?? null,
    leader_stderr: leader?.genvm_result?.stderr ?? '',
    contract_return_status: leader?.result?.status ?? null,
    contract_return_payload: typeof leader?.result?.payload === 'string' ? leader.result.payload : leader?.result?.payload?.readable ?? null,
    validator_vote_counts: voteCounts,
    from: receipt.from_address,
    to: receipt.to_address,
  });
}

const report = { rpc: endpoint, chain_id: chainId, captured_at_utc: new Date().toISOString(), transactions };
await mkdir(resolve('artifacts'), { recursive: true });
await writeFile(resolve('artifacts', 'current-live-receipts.json'), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));
