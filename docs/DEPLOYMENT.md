# StudioNet deployment evidence

## Network and deployed source

| Field | Evidence |
|---|---|
| Network | StudioNet, chain ID `61999` |
| RPC | `https://studio.genlayer.com/api` |
| CLI | Repository-local GenLayer CLI `0.39.1` |
| Sever address | `0x83766112084fBEA07873b241Cf37e770438d928C` |
| Deploy transaction | `0x3664fa80c05a7e608a8a455d8655abb7f2d9107f3e6f1f893f97a25a4dc6d5e2` |
| Source commit used for deployment | `973dc494d3e3c396c770e62cd3c1bb485083f55e` |
| Canonical deployed source SHA-256 | `840b0e3a64c8e018d3f884396eab982cf10e7523d1c7aa3402cbb3a875297158` |

The CLI receipt reached `FINALIZED` with `MAJORITY_AGREE`; the round showed five validator commits and five reveals. The leader receipt reports GenVM `SUCCESS`, with no error code or description. The repository-local CLI `code` command retrieved the deployed contract source. After normalizing line endings to LF and using one terminal newline, the retrieved text matched both the worktree and the listed source commit byte-for-byte under the same normalization; the SHA-256 above was computed over that canonical UTF-8 text.

The CLI `trace` command could not retrieve a trace because this RPC returns `Method not found` for `gen_dbg_traceTransaction`. The receipt's leader execution result and consensus status are available, but a separate detailed execution trace is not.

## Agreement 1 lifecycle evidence

Agreement ID `1` is titled `Sever live integration 2026`. Its creation transaction is `0x2a5c9d07d36ca8b077d5d99f76be98e6b3520afbca85b9541b5cffe72d4b8e12`. The creator added local demo alias `aase-deployer` (`0x3926627eb9d353e29c7d6f8f914be96f38631bab`) as its second party in transaction `0x8ff1dfeecc16c049104a00d9fb824537b2ec3fca67ca4582b2d9f401ed5563b4`; that receipt reported `MAJORITY_AGREE`, five validator commits/reveals, and leader GenVM `SUCCESS`.

The creator wallet transferred exactly 5 GEN to `aase-deployer` for its transaction fees. The unitless CLI argument `5` first submitted `0xc14b7604f06ff3ad3a2fc4722730858eb6fe990da622d4e673d093d0875e1fcd`, which finalized with 5 wei credited. Transaction `0xf8f8e525a77de18eca88da224cfe2bfe4dc949341b38737f8e74314ff90a62ee` then transferred the remaining `4.999999999999999995 GEN`; its finalized receipt reports `value_credited=true`. The two transfers total exactly 5 GEN. The alias balance read afterward was 15 GEN, including its pre-existing 10 GEN.

The user approved the exact synthetic clauses and essential flags below. Each add-clause write finalized with `MAJORITY_AGREE`, five validator commits/reveals, and successful leader execution:

| ID | Name | Essential | Text | Transaction |
|---:|---|---|---|---|
| 1 | Essential acceptance | Yes | Customer's ability to accept the report delivered under clause 2 is essential to this synthetic agreement. | `0x4cb5ae45a6fd54f606f669a8c12290097fd8e1ed4e9e83be85e2c431c7c7fe81` |
| 2 | Delivery | No | Provider delivers one report to Customer on Friday. | `0xbafbdaa1c5e34efd05dcc175bad4e10f98c2cecf33ea0e89690c16a19f9b3a2d` |
| 3 | Acceptance payment | No | Customer pays Provider only after accepting the report delivered under clause 2. | `0x8313c75abeb394bc4216cdf63bcca789d88403327de7aef109865c61b4a464f6` |
| 4 | Report support | No | Provider supports the report after payment under clause 3 for 30 days. | `0xd6f6f1e61064e73ab653f2507332e1b48184a498a40ef9f4142358ae67251a72` |
| 5 | Independent workshop | No | Provider supplies an independent Python workshop unrelated to report delivery, payment, or support. | `0x989d96c00f879df88c2a6032bafd26bcc40db662871ed1de0063f3cebfc1480a` |

The seal transaction `0x8e167b174b0910cda47c9b07b2c9a32e81c97b45a3d3992d302879613912101d` finalized with `MAJORITY_AGREE` and successful leader execution. Its genesis hash is `bfdeac51cb7c664791500b5a005342fc71637aa4bfd98cbbc902f7f054ff788c`. Both parties ratified the same hash: second-party transaction `0x8f11b76d1302446a1cd79a694be748c4a05bb5ddd34303fdaa1760af770c9c44`, creator transaction `0x4f27269d08ee3b017170a0d27c8cae7288f17fcedb4122943a844f7e3a072f36`. Both finalized successfully; `get_vote` returned `ratified=true` for each party. Activation transaction `0xfc23504455b1f4d1e890e97dbb984100d09ff924f80dac41562f8d0070c1cdaa` finalized with `MAJORITY_AGREE`, five commits/reveals, and successful execution. The agreement is sealed and active.

## Live dependency certification result

Two live `certify_dependencies(1, genesis_hash)` attempts were made against the unchanged sealed agreement:

| Transaction | Final result | Consensus rounds | Last-round votes |
|---|---|---:|---|
| `0xf3d29dbb167a7a329f3e646feeaafc1cec0aa08252b57a5e4cc15da4745640c5` | `FINALIZED`, `MAJORITY_DISAGREE` | 4 | 3 `DISAGREE`, 2 `IDLE` |
| `0x63a51a159b896c49bb5a280294c4af9b8f34dce9243639861dd9211d5d36fd80` | `FINALIZED`, `MAJORITY_DISAGREE` | 4 | 3 `DISAGREE`, 2 `IDLE` |

Both leader GenVM executions reported `SUCCESS`, but validators did not agree on the complete dependency matrix. A final `get_agreement(1)` read showed `active=true`, `certified=false`, empty `graph_hash`, no invalidations, and version `0`; `get_graph(1)` failed with `NOT_CERTIFIED`, as expected. The CLI cannot calculate an appeal bond on this chain because the configured fee-manager/rounds-storage contracts are missing. No more certification attempts were made. Since the agreement is uncertified, no invalidation, clause status transition, or consumer deployment/call is claimed. The sealed terms cannot be edited; a revised agreement would need separately approved wording.

The CLI `trace` command could not retrieve detailed traces because the RPC returns `Method not found` for `gen_dbg_traceTransaction`. No credentials or private keys are included in this repository.

## Agreement 2 retry lifecycle evidence

After the first agreement remained uncertified, the user approved a second synthetic package with a revised six-clause chain. Agreement ID `2` was created by transaction `0x9529b895c2752c29093097bc97e55ad92a4a3b00c1ad63cc575eb459da004629`; it finalized with `MAJORITY_AGREE` and leader execution `SUCCESS`. Its title is `Sever live integration 2026 retry` and its purpose is `Synthetic test of a report dependency chain, indirect essential-clause collapse, payment invalidation, and independent workshop survival.` Aase (`0x3926627eb9d353e29c7d6f8f914be96f38631bab`) was added by `0xff7d17084497556f9660080fbf40a625510460c5db7b5167b7b925d40b8a8918`.

All six exact approved clauses finalized with `MAJORITY_AGREE`, five validator commits/reveals, and successful leader execution:

| ID | Name | Essential | Text | Transaction |
|---:|---|---|---|---|
| 6 | Source data access | No | Provider grants Customer access to the source data needed for the report under clause 2. | `0x01b737a2f01acc9f766738fc4a11d673d9275a105a521f34bac1f2efb6e8935b` |
| 7 | Data processing | No | Provider processes Customer's source data using the access granted under clause 1 to produce the report under clause 3. | `0x5daf8df4ef291018f7fa1a44e7f4a258b8a86f0fdd04431057deeb15a6674630` |
| 8 | Report delivery | Yes | Provider delivers the report produced under clause 2; delivery is essential to this synthetic agreement. | `0x97cc429818c260dcf893e9772a99981d6a4bd61793f66472e38ad65b2c510c3b` |
| 9 | Acceptance payment | No | Customer pays Provider only after accepting the report delivered under clause 3. | `0xfded5fc505a4304c65de13e883c21083dbba1245db82df2ef0cc9ff9d4599b3c` |
| 10 | Report support | No | Provider supports the report after payment under clause 4 for 30 days. | `0x8d6b688984e866b96d008ad1be72ab8b8142b3adf5a4d5e58d224754f66249cd` |
| 11 | Independent workshop | No | Provider supplies an independent Python workshop unrelated to source data access, processing, report delivery, payment, or support. | `0x6747cc67cd10e625f9debf97da6edfc0bb9dbef5f7e7a61651319061718d155f` |

On-chain reads confirmed parties `[creator, Aase]`, clause IDs `[6, 7, 8, 9, 10, 11]`, and essential IDs `[8]`. The agreement was sealed by `0x7dfec18bcdafa81979ccc5e6e424102a41ccd86410a9d0bf1a969de613b5250d`; its genesis hash is `b71d48c1e96f8611491272a329ef10ab27f49bd5b1105938467dc78ff95e3293`. Aase ratified in `0xcd947cb290cf862fba84897547d96ce5f06456d404d4c730c0da5f70fe60caf0`, and the creator ratified in `0x0ae6d851541a96f1f49b6336aa2949fa222a1d3c5955e248f5798f086feac9f4`. Activation transaction `0x7bdb2386d23625832349622f57327834700885f129d9948ceab9b64516d112f1` finalized successfully.

The revised dependency-certification attempt `0x98ae3c499395fbe6f97534fa41d92666c3a4b6eada4fd3d485bec33d7b256eb7` finalized `MAJORITY_DISAGREE` after four rounds; the last round had three `DISAGREE` and two `IDLE` votes. A state read confirmed agreement 2 remains sealed and active but `certified=false`, `graph_hash=''`, `version=0`, with zero invalidations and no pending proposal. The CLI cannot calculate an appeal bond on StudioNet because the configured fee-manager/rounds-storage contracts are missing. Since certification did not succeed, no invalidation, clause propagation, or live consumer operation was submitted. Both agreements therefore remain uncertified on StudioNet; the synthetic invalidation/consumer lifecycle is not demonstrated as complete.
