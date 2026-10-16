# Sever

**Sever is a contract-only GenLayer primitive for preserving the operable remainder of a multi-party agreement after an agreed clause invalidation.**

A clause can fail without necessarily destroying every other clause. A refund can depend on a delivery term; an independent training obligation can survive that delivery term. Conventional smart contracts cannot reliably derive such material dependencies from free-form contractual language. Sever asks validators to discover those dependencies once on **the fully ratified, immutable agreement**, then uses a deterministic directed graph to propagate suspension when an invalidation occurs.

**Design invariant:** *No invalidated clause remains operative; no clause requiring an inoperative clause remains operative; a party-designated essential clause becoming inoperative suspends the entire bargain. Independent clauses survive.*

## What this is (and isn't)

- A reusable **Intelligent Contract**, not a full app. **No frontend**, backend, wallet UI, database server or Docker application is needed.
- A semantic dependency and deterministic severance protocol, **not legal advice, a court, a legal-validity oracle, a replacement for contract drafting or a source-truth oracle**.
- **GenLayer cannot unilaterally invalidate a clause.** Every listed party must explicitly ratify that precise clause-invalidation proposal. The model has no say on whether a law, court, legislature or regulator rendered a clause invalid.
- A small agreement primitive, bounded to **2–4 parties, 2–6 clauses, 12 opened attempts and 6 successful invalidations per agreement**. Bounds control model-context size, gas/state growth and worst-case directed-pair analysis.
- No escrow or token transfer. It publishes state that a different contract can consume, with one small consumer demonstration contract included.

## The algorithm

```text
Draft: creator adds parties, clauses, purpose, and essential flags
       ↓
Seal: genesis hash freezes every word and role
       ↓
Ratify: ALL named parties sign the same genesis hash
       ↓
Activate
       ↓
One immutable certification epoch: one directed pair per bounded batch
       ↓
For every batch, validators independently classify all directed pairs
and audit each proposed independent edge
       ↓
Deterministic finalizer requires all N × (N−1) pairs exactly once
       ↓
Certified graph (immutable)
       ↓
Any party proposes: clause X is inoperative
       ↓
ALL parties consent to this exact proposal or another party vetoes
       ↓
Deterministic closure:
    X INVALID
    every dependent / uncertain chain SUSPENDED
    independent clauses ACTIVE
    essential clause impaired => core COLLAPSED
       ↓
Hash-linked status head + consumer read-only API
```

A directed edge `A REQUIRES B` means **A materially depends on B**, not that A and B share a topic or use similar words. If B is inoperative, A is suspended. `UNCERTAIN` is treated as *potentially dependent* when its target fails; uncertainty cannot be silently treated as independence.

## Reader example

Frozen clauses:

| ID | Clause | Essential? |
|---|---|---|
| 1 | Deliver five reports on Friday | No |
| 2 | Pay after accepting the five delivered reports | No |
| 3 | Provide report-specific support for 30 days | No |
| 4 | Conduct separate independent training | No |

Consensus establishes `2 REQUIRES 1` and `3 REQUIRES 1`; the training clause is independent.

Both parties explicitly invalidate clause 1. Deterministic graph closure yields:

```json
{"1":"INVALID","2":"SUSPENDED","3":"SUSPENDED","4":"ACTIVE"}
```

A downstream contract using `is_clause_operative(agreement_id, 4, genesis_hash)` continues to operate on independent training. A downstream contract bound to clause 2 is blocked.

If clause 1 were designated **essential** by the parties before signing, every other clause would be suspended. If an essential clause becomes suspended *indirectly*, the bargain also collapses.

## Public API

| Write | Purpose |
|---|---|
| `create_agreement(title, purpose)` | Draft a new agreement, caller initially listed as party |
| `add_party(agreement_id, party)` | Creator adds up to three other parties before seal |
| `add_clause(agreement_id, name, text, essential)` | Creator adds 2–6 immutable intended clauses |
| `seal_agreement(agreement_id)` | Freeze genesis commitment; no further edits |
| `ratify_agreement(agreement_id, genesis_hash)` | Each party personally signs exact contents |
| `activate_agreement(agreement_id)` | Open only after all parties ratify |
| `certify_dependency_batch(agreement_id, genesis_hash, batch_index)` | Independently certify one bounded directed pair in the activation-bound epoch |
| `finalize_dependency_certification(agreement_id, genesis_hash)` | Require every batch and every directed pair before publishing the immutable graph |
| `propose_invalidation(agreement_id, clause_id, reason, expected_head)` | A party opens a proposed stipulated invalidation |
| `endorse_invalidation(failure_id, expected_head)` | Another party ratifies the same exact assertion |
| `reject_invalidation(failure_id)` | Non-proposer vetoes a disputed assertion, opening slot clears |
| `finalize_invalidation(failure_id, expected_head)` | Any caller finalizes unanimous consent, propagates graph closure |

Read-only operations include `get_agreement`, `get_clause`, `get_graph`, `get_failure`, `get_vote`, `agreement_head`, `is_clause_operative`, `is_agreement_operative` and `is_agreement_fully_operative`.

`is_agreement_operative` means **core not collapsed**, not “all individual clauses are active.” Consumers with an actual clause-bound effect should prefer `is_clause_operative` and pin the genesis hash. To require **every** clause active, use `is_agreement_fully_operative`.

All consensus-dependent writes should be treated as pending until the GenLayer transaction reaches the requisite finalized state.

## Development and testing

Requires Python 3.12+, Node.js 20.11+ (Node 22 LTS recommended), and the pinned GenLayer test/lint tools.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux:       source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python scripts/preflight.py
python -m pytest tests -q

# Use the contract's pinned SDK artifact. See docs/TESTING.md for the
# GenVM 0.11.0 artifact-layout limitation and why this exact bundle is needed.
# PowerShell: $env:GENVM_VERSION='v0.3.0-rc7'
# macOS/Linux: export GENVM_VERSION=v0.3.0-rc7
genvm-lint check contracts/sever.py
genvm-lint validate contracts/sever.py
genvm-lint typecheck contracts/sever.py --strict
genvm-lint schema contracts/sever.py --output artifacts/sever-abi.json
genvm-lint check contracts/sever_consumer_example.py
genvm-lint validate contracts/sever_consumer_example.py
genvm-lint typecheck contracts/sever_consumer_example.py --strict
genvm-lint schema contracts/sever_consumer_example.py --output artifacts/sever-consumer-abi.json
gltest direct_tests -v -s

# Pinned repository-local GenLayer CLI:
npm ci
npm run cli:version
npm run network:guard
```

**Stable StudioNet only:** RPC `https://studio.genlayer.com/api`; chain **61999**, alias `studionet`. The CLI is pinned to `genlayer@0.39.1`. Each guarded deploy script checks the remote chain ID and requires a manual `DEPLOY-61999` confirmation. The consumer deploy guard also requires the Sever address, agreement ID, clause ID, and sealed genesis hash. The repository does not contain a wallet key.

The current source is deployed at `0x631fF4E9C44f8AD5496Ea5EeC10B3c476aA0c1CD`; the retrieved onchain source matches `contracts/sever.py` at canonical SHA-256 `6dc67c8eb662137a085ef39c868a71d1c32779456893e7c8031ea42479b310ac`. Agreement 3 completed 12 bounded pair batches and Agreement 4 completed a full certified invalidation/consumer lifecycle on StudioNet. Exact finalized receipts and state snapshots are in [deployment evidence](docs/DEPLOYMENT.md).

The offline tests use a small **mock GenLayer adapter** to verify deterministic state invariants and validator-logic shape. Direct Mode executes the real contract code with mocked LLM/model responses; its consumer case also mocks the provider response. Those checks do not prove public-network semantic consensus. See [deployment evidence](docs/DEPLOYMENT.md) for finalized StudioNet execution receipts and [test evidence](docs/TESTING.md) for test limits.

## Builder integration

`contracts/sever_consumer_example.py` defines an `ISever` typed view interface and a small `SeverGatedConsumer`. A consumer can pin `(sever_address, agreement_id, clause_id, genesis_hash)` at construction and reject any clause-bound action once that clause is invalidated or suspended.

The example deliberately performs **no transfers or irreversible external operations**. Builders can incorporate the same query into bounded executors after separately auditing their own execution and replay protections.

## Source tree

- `contracts/sever.py` — single deployable GenLayer Intelligent Contract with semantic consensus
- `contracts/sever_consumer_example.py` — independent consumer contract example
- `tests/` — offline deterministic and adversarial unit tests, no GenLayer dependencies
- `direct_tests/` — GenLayer Direct Mode validator adversarial tests and a mocked consumer-gating test
- `examples/` — public fixture and outcome explanation
- `docs/` — architecture, security, testing evidence and builder integration guide
- `scripts/` — static preflight and fail-closed StudioNet/CLI guards
- `.github/workflows/checks.yml` — CI for offline tests, GenVM lint and Direct Mode

## License

MIT. See `LICENSE`.
