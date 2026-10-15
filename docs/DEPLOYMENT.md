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

## Draft agreement transaction

A second finalized transaction created agreement ID `1` with title `Sever live integration 2026`. Its transaction is `0x2a5c9d07d36ca8b077d5d99f76be98e6b3520afbca85b9541b5cffe72d4b8e12`; the receipt reports `FINALIZED`, `MAJORITY_AGREE`, and successful GenVM execution. A read-only `get_agreement(1)` confirmed the draft has only its creator, no clauses, and `sealed=false`, `active=false`, `certified=false`.

The creator later added the local demo alias `aase-deployer` (`0x3926627eb9d353e29c7d6f8f914be96f38631bab`) as a second party. The write transaction is `0x8ff1dfeecc16c049104a00d9fb824537b2ec3fca67ca4582b2d9f401ed5563b4`; its receipt reports `MAJORITY_AGREE`, five validator commits and reveals, and leader GenVM `SUCCESS` with no error. A subsequent read confirmed two parties, zero clauses, and `sealed=false`, `active=false`, `certified=false`.

The creator wallet transferred exactly 5 GEN to `aase-deployer` for its transaction fees. The first CLI argument was unitless `5`, so transaction `0xc14b7604f06ff3ad3a2fc4722730858eb6fe990da622d4e673d093d0875e1fcd` finalized with 5 wei credited. Transaction `0xf8f8e525a77de18eca88da224cfe2bfe4dc949341b38737f8e74314ff90a62ee` then transferred the remaining `4.999999999999999995 GEN`; its receipt is `FINALIZED` with `value_credited=true`. Together, these transfers equal exactly 5 GEN. The recipient balance read after transfer was 15 GEN, including its pre-existing 10 GEN.

No clause text has been committed, and no ratification, certification, invalidation, or consumer call has been claimed. Automatic approval review rejected writes binding proposed legal-like test language because the exact wording and essential flags had not been explicitly approved. I stopped those writes and did not retry them through another route. The consumer deploy helper requires a real, sealed genesis hash and clause ID, so no placeholder consumer was deployed.

To complete the live multi-party demonstration, the operator must explicitly approve the exact synthetic clause wording and essential flags before those terms are written to the public chain. The `aase-deployer` alias is the second party and has a 15 GEN balance at the last read. No credentials or private keys are included in this repository.
