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

No second party or clause text was committed, and no ratification, certification, invalidation, or consumer call has been claimed. Automatic approval review rejected a batch that would add a second signer and bind proposed legal/economic test language, and separately rejected a 4 GEN transfer to fund two independent wallets. I stopped those state changes and did not retry them through another route. The consumer deploy helper requires a real, sealed genesis hash and clause ID, so no placeholder consumer was deployed.

To complete the live multi-party demonstration, the operator must explicitly approve the test-party identity and synthetic clause text. The current CLI includes unlocked local aliases `aase-deployer` (`0x3926627eb9d353e29c7d6f8f914be96f38631bab`) and `civec-deployer` (`0xf8c03f1e5f6e6cee945a9b37807924d70e2a9c5f`), each with a zero GEN balance when checked. Funding those accounts would require explicit approval for the exact recipients and amounts. No credentials or private keys are included in this repository.
