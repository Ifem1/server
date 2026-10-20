# StudioNet deployment and lifecycle evidence

All transactions below were submitted to stable StudioNet, chain ID `61999`, using the repository-local GenLayer CLI `0.39.1`. A receipt marked `ACCEPTED` by the CLI is finalized for this network. Validator vote labels describe GenLayer's consensus result; they do not imply every validator independently agrees with every semantic classification.

## Release deployment status

The contract source has been remediated after the deployment below. This historical deployment does not contain the corrected validator and is not a deployment of the current release source. A submission-readiness claim requires a new matched deployment and lifecycle.


## Corrected deployment and Lifecycle A (2026-10-20)

The corrected Sever source from commit `fec306810fb0f138a3baf7f6656bdd5c48395192` is deployed at `0xD7D258B09B21017D42EEcb14158d062e60E2064b`. Its [deployment receipt](https://explorer-studio.genlayer.com/tx/0x5cc3de50b3368f91bbda5916fceb2efa58f7bfaa85e2dd5e82b536247879cdcf) is finalized with leader GenVM `SUCCESS`. The retrieved source matches the local contract exactly: raw SHA-256 `0e8d657c356b58d41dc2f427cd2671c91b98bd79a7799710eb46f7ca3e6cfa12`; normalized SHA-256 `416497261308fbfb524cce99b33cab32552b3dfc96ab392918cdf77f436f3cbd`.

Lifecycle A agreement 1 genesis is `1fec5974896f2601cdfcb3531c1551143f6f248a37830d57c40ac526634a3ea4`; its certified graph hash is `8aceeb34cc813f5a26126f024dfb2c69dcea5c911f3de0f2d1d193cb6d9234a9`. The graph includes `2 REQUIRES 1`; all other five directed pairs are `INDEPENDENT`. The graph was finalized in [transaction](https://explorer-studio.genlayer.com/tx/0x547aeeecdb62bef90e57107b723f3425e6950565ab94a94233981668fc995101).

The matching consumer at `0xAf9A540b170255b5CBe8FBA844822cedce95a731` was deployed in [transaction](https://explorer-studio.genlayer.com/tx/0x1899a02be92dd645a247a35982afd57f6c655818ab32a9f05b57144eeb612c01), bound to agreement 1, clause 2, and that genesis. It executed successfully in [transaction](https://explorer-studio.genlayer.com/tx/0x65607e499f6d77d052c7fdbf09b40606646a2d3cb02fad062eab51f7940ae93f). The [invalidation proposal](https://explorer-studio.genlayer.com/tx/0xb654593592e608f96c463dda26b8f91a84833afb9df9dffb5fa1dea22d3250b0) and [second-party endorsement](https://explorer-studio.genlayer.com/tx/0x6f9faa173395d3e7463ac331081177e21bf1249cb48de0d1335d81c2b8312b36) preceded [finalization](https://explorer-studio.genlayer.com/tx/0x84d501aefa3265029d22bbc6f95ed4e8ce95c9d16bdc4bb6cc57d51ff4526b27). Direct reads show clause 1 INVALID, clause 2 SUSPENDED, clause 3 ACTIVE. The same consumer's [post-invalidation action](https://explorer-studio.genlayer.com/tx/0x85fe4ee6bdcd33acc475c1f4839c40e3f3af9dac6aa660617a66cdd096ae8a57) finalized with leader GenVM `ERROR`; its action count remained 2. Full raw and normalized source comparisons are in [source-parity-report.json](../artifacts/source-parity-report.json).

Lifecycle B has been created and ratified with essential clause 4 and dependent clause 5, but pair certification has not reached consensus. One attempt finalized `MAJORITY_DISAGREE`; a retry remained pending at the time of the last read. There is no verified Lifecycle B graph, essential-collapse result, or B-bound consumer result, so the release is not yet submission-ready.
## Historical deployed source

| Field | Value |
|---|---|
| Sever contract | `0x631fF4E9C44f8AD5496Ea5EeC10B3c476aA0c1CD` |
| Deployment transaction | `0x36ede6be2268f582d81f1948d0121bf5da131217cb9357624ec216bb10929654` |
| Source version | `a33def3684586e7e6c0cf815ecd1ea50b596a14f` (pre-remediation) |
| Deployed Sever raw-byte SHA-256 | `9c0205d994da16cc81dff15223a7fbceab6e45420a813e130b0925563c3ef9b2` |
| Deployed Sever SHA-256 after CRLF→LF normalization | `6dc67c8eb662137a085ef39c868a71d1c32779456893e7c8031ea42479b310ac` |
| Pre-remediation manifest hash | `9c0205d994da16cc81dff15223a7fbceab6e45420a813e130b0925563c3ef9b2` (raw bytes) |
| Historical consumer raw and normalized SHA-256 | `d92133f0ec3ff0079591227697dd2028f1155176025b5cdcd89d9d6781610d27` |

The pre-remediation source hashes were different because the manifest recorded raw CRLF bytes (`9c02…`) while the deployment prose recorded LF-normalized bytes (`6dc6…`). They identify the same source after explicit CRLF→LF normalization. Both deployed contracts were retrieved with `gen_getContractCode`; the captured bytes and current local comparison are recorded in [source-parity-report.json](../artifacts/source-parity-report.json), with source snapshots under `artifacts/onchain-source/`. The current corrected Sever source differs from this historical deployment and requires redeployment. The separate CLI `trace` endpoint is unavailable on this RPC (`gen_dbg_traceTransaction` returns `Method not found`); finalized transaction receipts remain available.

## Real validator disagreement investigation

These three whole-matrix certification transactions all finalized `MAJORITY_DISAGREE` after four rounds, with three `DISAGREE` and two `IDLE` votes in the last round:

| Agreement | Transaction | Finding |
|---:|---|---|
| 1 | `0xf3d29dbb167a7a329f3e646feeaafc1cec0aa08252b57a5e4cc15da4745640c5` | Validators did not accept the leader's full-matrix result. |
| 1 | `0x63a51a159b896c49bb5a280294c4af9b8f34dce9243639861dd9211d5d36fd80` | Repeat attempt on the same sealed terms still disagreed. |
| 2 | `0x98ae3c499395fbe6f97534fa41d92666c3a4b6eada4fd3d485bec33d7b256eb7` | Revised six-clause matrix still disagreed. |

These are live StudioNet receipts from the deployed semantic validator path, not mock responses. The initial implementation asked independent validators to accept an entire directed matrix in one consensus round. The observed failures established that a single disputed relationship could block all graph progress. Bounded, epoch-pinned pair batches reduce the consensus unit while retaining independent classification, complete ordered-pair coverage, and fail-closed `UNCERTAIN` handling. No disputed marker is counted toward a certified graph.

## Agreement 3: four-clause bounded certification

Agreement 3 is titled `Sever final direct dependency lifecycle 2026`. Both parties ratified genesis `f627295027e8570445d8b142622dcf3277a74da3b4fbc7a689f8c516f76ea6e5`; activation fixed epoch `a7a3f27b0de0c24420b96fa552f6de876baf3177977abaf051c5c848aad0b92d`. Its 12 directed pair transactions are recorded in [final-pair-certification.txt](../artifacts/final-pair-certification.txt). All 12 markers are true in that same epoch. Finalization transaction `0x3ad1ec16b8fcae7c4bb1706f64763e558132e5df56ea90896245f06e3531e0be` committed graph hash `1949666fb48ffa8408ddbcc1bb207ea3fb75bd75a1e8bfc50c3409a8f2bbabfa`.

The onchain graph includes required edges and a conservative `UNCERTAIN` edge (`10 → 12`); uncertainty is preserved as potentially dependent. The independent workshop edges remain explicitly classified. Agreement 3 demonstrates that all 12 relationships can be certified in bounded transactions before one graph finalization.

## Agreement 4: complete invalidation and consumer lifecycle

Agreement 4 is titled `Sever compact lifecycle 2026`. It uses explicit immutable IDs:

| ID | Clause | Frozen text | Status after invalidation |
|---:|---|---|---|
| 14 | Report preparation | Provider prepares one report from Customer's public dataset. This is the specific report delivered under Clause ID 15. | `INVALID` |
| 15 | Report delivery | Provider delivers to Customer the report prepared under Clause ID 14. If Clause ID 14 is inoperative, this delivery duty cannot be performed. | `SUSPENDED` |
| 16 | Independent workshop | Provider delivers a separately priced Python workshop with independent scope. It does not require or depend on Clauses 14 or 15 and remains performable if either is inoperative. | `ACTIVE` |

The agreement's creation transaction is `0xe1e32df0eb5671948ba27cd4ae01092679e091851fad0b2b639032d1989dd213`; Aase was added in `0x78e8ef47aeaeffe2005a8b8b405c4a3317c5dff5c9461a6ce2b7125cebb5ced1`. Clause transactions were `0x96ab3a3ad66186c95d720f26caf389555e82e7b07a51caf3a0ad27404f76c8f7` (14), `0x7f2a9ef11461b21e6d53514ccb2e1338d58a754ac474f2656a84d6e223b4e220` (15), and `0xa5594b154dfc4eef03a4300d4c2a251ed8f9bfee128e41a0c396a59514a51564` (16). Seal transaction `0xdb04688c9ab4fdb7b06bc7fd54f14168fc6b146b6d14f28e30399c40a7e7e1e5` committed genesis `6b31263cdb7658072c7788dcc6f935ef1f0f7fc0eaea0d18a6cc515069bbb0f7`. Aase ratified in `0xf962cc4d98c33e2e5cdf074d68ea8e07e7d665b389af0a106666b66c33807b98`; the creator ratified in `0x8f2d09fd43487c2496efffb7177166843b039e78657973e13e6433232044749c`. Activation transaction is `0xf310f34e22a0020b94e4b1d45cd0ee49954cbb522486ab794c32d1ca12146a8e`.

The six directed pairs finalized in one round each with `MAJORITY_AGREE`:

| Pair index | IDs | Transaction | Last-round votes |
|---:|---|---|---|
| 0 | 14 → 15 | [transaction](https://explorer-studio.genlayer.com/tx/0x46bcc13b82edc47b496b61a1f4ff63c7d2270d07e28804c1e9aa59b4d8a50e60) | 3 agree, 2 idle |
| 1 | 14 → 16 | [transaction](https://explorer-studio.genlayer.com/tx/0x4f7a6d4426737f672ceb24c66bdfe3a7fa133792e0c8cb4f9be07885ad1e53b5) | 3 agree, 2 idle |
| 2 | 15 → 14 | [transaction](https://explorer-studio.genlayer.com/tx/0x5727f92daff117b39762f8d2c530d797b251f673728fcc4984c543f9cd2345a7) | 3 agree, 2 idle |
| 3 | 15 → 16 | [transaction](https://explorer-studio.genlayer.com/tx/0x1b160eb591c107919208557b4a26058464f589b7097f911b02900e0dea35b5f7) | 3 agree, 2 idle |
| 4 | 16 → 14 | [transaction](https://explorer-studio.genlayer.com/tx/0xdd8492069de93f5e0e9867dc1e2117c532bcd2482b6e28d3089ef2b707a34dee) | 3 agree, 1 disagree, 1 idle |
| 5 | 16 → 15 | [transaction](https://explorer-studio.genlayer.com/tx/0x9c395d21225ba6101e70c8e32bdfd743d25a29c1ef43e7eb9f644299177ba8cc) | 3 agree, 2 idle |

Finalization [receipt](https://explorer-studio.genlayer.com/tx/0xec4a96f4e4d3943f881b64df8f06766c30877a731634bdce341a96f3aed63795) is `FINALIZED` / `MAJORITY_AGREE`; its leader GenVM execution is `SUCCESS`, with four agree and one idle validator. It committed graph hash `8254945f56aa6a37bade8351ac8f3821a25e822f6f0a1ded49e58d1a3723749a`. A direct live `get_graph(4)` read returned:

| Directed pair | Stored relation |
|---|---|
| 14 → 15 | `REQUIRES` |
| 14 → 16 | `INDEPENDENT` |
| 15 → 14 | `REQUIRES` |
| 15 → 16 | `INDEPENDENT` |
| 16 → 14 | `INDEPENDENT` |
| 16 → 15 | `INDEPENDENT` |

The earlier deployment prose and `artifacts/lifecycle-certification.txt` omitted the `15 → 14 REQUIRES` edge. The six finalized pair transactions show the full pair coverage; the edge direction and classes above are from the live graph read. The clause texts establish a reciprocal relationship: clause 15 explicitly requires the report prepared by 14, while clause 14 describes preparation of the specific report delivered under 15. The observed statuses are consistent with the stored graph and the deployed `impact_closure`: when 14 is invalid, 15 suspends through `15 → 14`; 14's outgoing edge cannot suspend its own root; 16 survives because both its edges are independent. This is not a propagation defect or a status contradiction. It is a historical evidence-description omission. The current regression test asserts this direction and demonstrates that the reversed single edge does not suspend 15.

The pinned consumer was deployed at `0xf2DE8057a2416307C7F77cd62365E15E8A880caA` in [transaction](https://explorer-studio.genlayer.com/tx/0xbd3eab8bc7899b8f50f4def45ab63c348628243c2750b2f447f4dacbe6bab739), bound to Sever, agreement 4, clause 15, and the exact genesis hash. Its [action transaction](https://explorer-studio.genlayer.com/tx/0x605ef7a734cee097200b78ef1868e0b1e94f183fb8740b1bc19f9d8f42531aea) finalized with leader GenVM `SUCCESS` while the clause was operative.

The [invalidation proposal](https://explorer-studio.genlayer.com/tx/0x9ae1e3da2073d038a518974a9489fbb986a0fb7a4f9ab55a650f1573e4c3e5e7) targeted clause 14 at the current head. The other party [endorsed](https://explorer-studio.genlayer.com/tx/0x164e38944c6efd6fbc24c1241b908919ea33bf13c998374acc163720c1675dad) failure ID 1. [Finalization](https://explorer-studio.genlayer.com/tx/0xf950bc37bfdd73c2d6373d17fd01991d31e7d0e0d350060a9be95cf3f5f29c6c) produced the states above. A direct `get_failure(1)` read reports finalized=true and status snapshot `[[14,2],[15,3],[16,1]]`; live views returned false for clause 15 and true for clause 16.

After invalidation, the same consumer's [rejected action transaction](https://explorer-studio.genlayer.com/tx/0xf1deceb415bd13ee778ab72e6e925f66ddc89d5ccfa252466ba8b6691330423c) finalized by consensus with leader GenVM execution `ERROR` and contract rollback payload `SEVER_CLAUSE_NOT_OPERATIVE`. Its `action_count()` stayed at `1`, confirming the failed action did not change consumer state. This completes the historical certified graph → unanimous invalidation → dependent suspension → independent survival → consumer acceptance and rejection lifecycle.

The structured receipts for the deployment, all six pair calls, graph finalization, consumer deployment/actions, and invalidation steps are in [historical-transaction-receipts.json](../artifacts/historical-transaction-receipts.json). These are historical receipts from the pre-remediation deployment; Direct Mode and offline tests cover the corrected validator but do not replace a new live lifecycle.

## Earlier agreements

Agreements 1 and 2 and their initial failed certification attempts are retained as historical diagnostics. Their sealed terms remain immutable and their certification failures did not change their uncertified state. The successful Agreement 3 and Agreement 4 evidence above supersedes any earlier statement that no live lifecycle was demonstrated. No wallet keys or credentials are stored in this repository.
