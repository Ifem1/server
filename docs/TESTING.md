# Test and validation evidence

## Tool versions

The repository pins `genlayer-test==0.29.0`, `genvm-linter==0.11.0`, `pytest==8.4.2`, and local `genlayer@0.39.1`. Python 3.12+ and Node 20.11+ are required; Node 22 LTS is recommended.

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

Sever is deployed and source-matched on StudioNet. Agreement 1 has two parties, five clauses, a sealed genesis, unanimous ratification, and active state. Agreement 2 has two parties, the approved six-clause report dependency chain, a sealed genesis, unanimous ratification, and active state. Both agreements' dependency certification transactions finalized with `MAJORITY_DISAGREE` after four rounds; their final rounds each had three `DISAGREE` votes and two `IDLE` votes. Both remain uncertified, so no live invalidation or consumer deployment/call has been demonstrated. StudioNet's CLI cannot calculate the appeal bond because its fee-manager/rounds-storage contracts are missing. See `docs/DEPLOYMENT.md` for exact transaction hashes and states. Deployment or agreement-write consensus does not prove semantic dependency certification succeeded.

## Verification run

On 2026-10-15, the Windows local toolchain produced these results:

- Static preflight: **13/13 passed**.
- Offline deterministic/adversarial suite: **21 passed**.
- Direct Mode: **9 passed**; model and consumer provider responses are mocked as described above.
- For each contract, `check` passed all three lint checks, `validate` passed (Sever: 20 methods; consumer: 2 methods), strict typecheck reported no type errors, and schema generation succeeded.
- Local CLI reported **0.39.1**. The RPC guard independently verified StudioNet chain ID **61999**.
- `npm audit --omit=dev` found **0 production dependency vulnerabilities**. Initial npm installation reported **six development dependency advisories** (four moderate, two critical); a later full audit request failed at the npm advisory endpoint, so those advisories remain untriaged.

These local results are distinct from the public-chain evidence above. GitHub Actions also passed for commit `2e60e870f1334de692c36513ce5ecf9b0d59ad92` in [run 38784650281](https://github.com/Ifem1/server/actions/runs/38784650281); that run includes the corrected GenVM runner cache path.
