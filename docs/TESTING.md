# Test and validation evidence

## Tool versions

The repository pins `genlayer-test==0.29.0`, `genvm-linter==0.11.0`, `pytest==8.4.2`, and local `genlayer@0.39.1`. The release environment uses Python 3.12 and Node 22 LTS.

## Reproducible local checks

From PowerShell at the repository root:

```powershell
.venv\Scripts\Activate.ps1
python scripts/preflight.py
python -m pytest tests -q
npm ci
npm run network:guard
$env:GENVM_VERSION = 'v0.3.0-rc7'
genvm-lint check contracts/sever.py
genvm-lint validate contracts/sever.py
genvm-lint typecheck contracts/sever.py --strict
genvm-lint schema contracts/sever.py --output artifacts/sever-abi.json
genvm-lint check contracts/sever_consumer_example.py
genvm-lint validate contracts/sever_consumer_example.py
genvm-lint typecheck contracts/sever_consumer_example.py --strict
genvm-lint schema contracts/sever_consumer_example.py --output artifacts/sever-consumer-abi.json
$env:USERPROFILE = (Resolve-Path .venv\isolated-home).Path
.venv\Scripts\gltest.exe direct_tests -v -s
```

On macOS/Linux, activate `.venv`, export the same two environment variables (use the isolated cache path for `USERPROFILE` only on Windows), and run `gltest direct_tests -v -s`.

## GenVM artifact compatibility

Both source files retain the exact `py-genlayer` dependency hash declared in their contract headers. That dependency is present in the official `v0.3.0-rc7` GenVM bundle in the legacy `runners/py-genlayer/<hash>.tar` layout consumed by `genvm-linter==0.11.0`. The current default GenVM manager bundle moved the legacy runners under `executor/v0.2.17/legacy-runners`; this linter version raises a lookup error with that layout. Accordingly, lint validation, strict typecheck, and ABI generation use `GENVM_VERSION=v0.3.0-rc7`, an official prerelease artifact that contains the *already pinned* runner. This is an artifact-layout workaround, not a change to the contract SDK header and not evidence that StudioNet executes that prerelease bundle. The deployment target remains stable StudioNet chain 61999.

Strict typecheck completed with zero diagnostics for each contract. Static `Protocol` casts describe the expected shapes at GenLayer's dynamic consensus runner, view decorator, and typed cross-contract proxy boundaries, where the linter's SDK stubs do not expose concrete types. These casts do not change runtime values or bypass runtime validation.

## Test layers and what they show

- `scripts/preflight.py` performs repository-level source/configuration checks without contacting StudioNet.
- `pytest tests` uses the local mock adapter to check deterministic state transitions, graph propagation, auth checks, stale heads, and adversarial shapes. These are unit tests, not GenVM or public-chain execution.
- `gltest direct_tests` runs the real contract source in GenLayer Direct Mode. Its model responses are mocked. The consumer test also mocks the provider cross-contract response; it proves the consumer gate reacts to true/false responses, not that a live provider call or public consensus succeeded.
- `genvm-lint check`, `validate`, `typecheck`, and `schema` exercise the pinned source against the selected official SDK runner artifact; they do not deploy or prove consensus finalization.
- `npm run network:guard` queries StudioNet's RPC chain ID and verifies 61999. A successful guard alone is not deployment evidence.

## Direct Mode bundle-name compatibility

The official `v0.3.0-rc7` release publishes the 134 MB runner archive as `genvm-runners-all.tar.xz`. Linter 0.11.0 recognizes that current asset name, but Direct Mode 0.29.0 still requests the removed generic `genvm-universal.tar.xz` URL. CI caches the linter's downloaded official archive and copies the exact same bytes into Direct Mode's versioned cache filename. This addresses the old download URL only; the SDK artifact and the contracts' pinned dependency hash do not change.

## Windows Direct Mode note

`gltest-direct==0.29.0` unlinks its stdin message tempfile while Windows still has that file locked. `direct_tests/conftest.py` defers deletion only for this specific Windows sharing violation; it passes the same SDK input and does not alter assertions or contract behavior.

## Live evidence

Historical source retrieval is captured by `scripts/capture_source_parity.mjs` and `artifacts/source-parity-report.json`; the report includes raw-byte and LF-normalized hashes for both deployed contracts. The historical Sever source matched the repository's pre-remediation source after LF normalization. Its raw deployed hash matches the original manifest; the raw hash in older prose used the LF-normalized bytes. The Agreement 4 live graph contains both `14 → 15 REQUIRES` and `15 → 14 REQUIRES`; the latter explains suspension of clause 15 after invalidating clause 14. The previous deployment record omitted that reciprocal edge. The corrected validator and direction regression tests are offline and Direct Mode checks, not live semantic-consensus evidence. A new corrected live lifecycle is still required after any contract-source change.

## Verification run

On 2026-10-20, the repository-local toolchain produced these results:

- Python **3.12.10**, Node **22.23.3**, pytest **8.4.2**, GenLayer Testing Suite **0.29.0**, GenVM Linter **0.11.0**, local CLI **0.39.1**.
- Static preflight: **15/15 passed**.
- Offline deterministic/adversarial suite: **23 passed**.
- Direct Mode: **12 passed** against the real contract source with mocked model responses. The consumer case also mocks its provider response.
- For Sever and consumer, `check` passed, `validate` passed (21 and 2 methods), strict typecheck reported zero errors, and ABI schema generation succeeded.
- The network guard independently verified StudioNet chain ID **61999**.

These checks verify local source behavior and target selection; they do not prove the corrected source is live. The old GitHub Actions run for commit `f02a04a` is historical only; the final pushed commit still needs its own successful Actions run.
