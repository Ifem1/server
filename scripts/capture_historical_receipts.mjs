import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';

const endpoint = 'https://studio.genlayer.com/api';
const transactions = [
  ['Sever deployment', '0x36ede6be2268f582d81f1948d0121bf5da131217cb9357624ec216bb10929654'],
  ['Agreement 4 pair 0: 14->15', '0x46bcc13b82edc47b496b61a1f4ff63c7d2270d07e28804c1e9aa59b4d8a50e60'],
  ['Agreement 4 pair 1: 14->16', '0x4f7a6d4426737f672ceb24c66bdfe3a7fa133792e0c8cb4f9be07885ad1e53b5'],
  ['Agreement 4 pair 2: 15->14', '0x5727f92daff117b39762f8d2c530d797b251f673728fcc4984c543f9cd2345a7'],
  ['Agreement 4 pair 3: 15->16', '0x1b160eb591c107919208557b4a26058464f589b7097f911b02900e0dea35b5f7'],
  ['Agreement 4 pair 4: 16->14', '0xdd8492069de93f5e0e9867dc1e2117c532bcd2482b6e28d3089ef2b707a34dee'],
  ['Agreement 4 pair 5: 16->15', '0x9c395d21225ba6101e70c8e32bdfd743d25a29c1ef43e7eb9f644299177ba8cc'],
  ['Agreement 4 graph finalization', '0xec4a96f4e4d3943f881b64df8f06766c30877a731634bdce341a96f3aed63795'],
  ['Consumer deployment', '0xbd3eab8bc7899b8f50f4def45ab63c348628243c2750b2f447f4dacbe6bab739'],
  ['Consumer action accepted', '0x605ef7a734cee097200b78ef1868e0b1e94f183fb8740b1bc19f9d8f42531aea'],
  ['Invalidation proposed', '0x9ae1e3da2073d038a518974a9489fbb986a0fb7a4f9ab55a650f1573e4c3e5e7'],
  ['Invalidation endorsed', '0x164e38944c6efd6fbc24c1241b908919ea33bf13c998374acc163720c1675dad'],
  ['Invalidation finalized', '0xf950bc37bfdd73c2d6373d17fd01991d31e7d0e0d350060a9be95cf3f5f29c6c'],
  ['Consumer action rejected after invalidation', '0xf1deceb415bd13ee778ab72e6e925f66ddc89d5ccfa252466ba8b6691330423c'],
];

const client = createClient({ chain: studionet, endpoint });
const chainId = await client.getChainId();
if (chainId !== 61999) throw new Error(`Wrong chain ${chainId}; expected StudioNet 61999`);
const records = [];
for (const [label, hash] of transactions) {
  const receipt = await client.getTransaction({ hash });
  const leader = (receipt.consensus_data?.leader_receipt || [])
    .find((item) => item.mode === 'leader');
  const votes = receipt.consensus_data?.votes || {};
  const voteCounts = {};
  for (const vote of Object.values(votes)) {
    voteCounts[vote] = (voteCounts[vote] || 0) + 1;
  }
  records.push({
    label,
    transaction_hash: hash,
    explorer_url: `https://explorer-studio.genlayer.com/tx/${hash}`,
    status: receipt.statusName,
    consensus_result: receipt.result_name,
    execution_result: leader?.execution_result ?? null,
    genvm_error_code: leader?.genvm_result?.error_code ?? null,
    genvm_stderr: leader?.genvm_result?.stderr ?? '',
    contract_return_status: leader?.result?.status ?? null,
    contract_return_payload: leader?.result?.payload ?? null,
    validator_vote_counts: voteCounts,
    rounds: Number(receipt.num_of_rounds),
    created_at: receipt.created_at,
    from: receipt.from_address,
    to: receipt.to_address,
  });
}

const report = {
  rpc: endpoint,
  chain_id: chainId,
  captured_at_utc: new Date().toISOString(),
  scope: 'Historical pre-remediation StudioNet deployment and Agreement 4 evidence',
  transactions: records,
};
await mkdir(resolve('artifacts'), { recursive: true });
await writeFile(resolve('artifacts', 'historical-transaction-receipts.json'), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));
