# Architecture and semantics

## Primitive boundary

Sever is deliberately **not** a free-form court. It cannot rule that a clause is unlawful, unenforceable, frustrated or void. All listed parties explicitly ratify agreement contents and later must jointly stipulate an invalidated clause. Any non-proposing party can veto a pending invalidation. The GenLayer semantic boundary is only the **material dependency graph** between fully signed clauses.

`A REQUIRES B` is a directed edge. Its definition is narrower than similarity, citation, topical overlap or common actors: A must need B to retain the agreed legal/economic role as expressed in the signed contract. `INDEPENDENT` is affirmative survival independence; `UNCERTAIN` is fail-closed, not equivalent to independence.

## Freeze before classify

1. Creator registers 2–4 parties and 2–6 clauses; every clause carries an explicit `essential` bit.
2. Creator seals; `genesis_hash` commits to creator, every party, purpose, titles, complete clause text, IDs and essential designations.
3. Every party submits `ratify_agreement(id, genesis_hash)` from its own wallet. There are no proxy signatures or inferred consent.
4. Agreement becomes active. Anyone can initiate the consensus graph certification against that exact genesis.
5. Result is stored as 1–30 directed edges, typed as INDEPENDENT, REQUIRES or UNCERTAIN. Graph and versioned head are committed to storage.
6. Later clause invalidation may only occur after explicit unanimous party approval and a pre-existing graph. No participant can change clause text, purpose or essentiality after seal.

## Bounded certification in one immutable epoch

Activation derives an epoch hash from the agreement ID, genesis hash, purpose, exact clause IDs and text, and ordered source IDs. For N clauses, certification is split into N × (N−1) batches of one directed pair each. The epoch and pair order cannot change between calls. A batch can be committed only once; the deterministic finalizer requires every batch and validates the complete N × (N−1) directed graph before publishing it.

For each bounded pair, the leader classifies the directed relationship and each validator independently classifies the same relationship from the frozen purpose, IDs and exact clause text. A validator accepts only an exact relation match, then makes a second contradiction-oriented semantic check that challenges the proposed class. This applies equally to `INDEPENDENT`, `REQUIRES` and `UNCERTAIN`: unsupported dependency inflation and unsupported uncertainty are rejected alongside unsafe independence. Malformed, omitted, reordered or foreign pair data is rejected before semantic acceptance. GenLayer's validator quorum determines transaction finality; validators can disagree and block a batch, while a finalized result is not a proof that all models interpreted legal meaning correctly. Each call covers one directed pair, so disagreement is bounded and an unsuccessful batch can be retried without marking that pair complete.

The protocol's practical liveness condition is semantic agreement for each pair among enough participating validators. It does not force a fallback relation when models conflict: `UNCERTAIN` is accepted only when the validator's own classification is also `UNCERTAIN` and its challenge accepts the ambiguity. This avoids turning disagreement into either automatic suspension or automatic survival. A clause prompt injection cannot change IDs or flags, but models can still share a semantic blind spot or accept an injected argument; this remains a residual model risk.

The stored graph contains only consensus-bound relation labels, not natural-language rationales masquerading as agreed facts. There is no local “majority vote” shortcut in the contract: every batch must pass GenLayer consensus and the complete set must be finalized in the same immutable epoch.

## Deterministic closure

Given known-invalid root set `R`, each clause is:
- `INVALID` iff its own invalidation has been unanimously finalized;
- `SUSPENDED` if it requires or might require any invalid/suspended prerequisite (including transitive closure);
- `ACTIVE` if independent from all invalid/suspended prerequisites.

All propagation is deterministic fixed-point iteration bounded by N. If any party-designated essential clause becomes INVALID *or SUSPENDED*, `core_failed = true` and every non-invalid clause becomes SUSPENDED. The protocol cannot silently revive a suspended clause. An invalidation is append-only and hash-linked to the previous head.

## Auth and anti-replay

- Creator-only draft edits; parties approve sealed genesis.
- Every party receives at most one ratification per agreement.
- Failure proposer must be a party; one failure at a time; all parties must endorse.
- Non-proposer party veto clears pending failure without modifying canonical status.
- At most twelve proposal openings and six successful invalidations per agreement.
- A proposal pins current head, a target clause and reason; duplicates/stale state are rejected.
- Consumer pins immutable `genesis_hash` so a similarly indexed clause from another agreement is not confused.

## Composability

`is_clause_operative(agreement_id, clause_id, expected_genesis_hash)` is the authoritative gate for clause-bound actions. `is_agreement_fully_operative` checks that all clauses remain active; `is_agreement_operative` checks core survival and can be true during partial severance. The caller must understand that “ACTIVE” means not affected by **recorded stipulated invalidations** under this graph; it does not certify real-world compliance or independent legal enforceability.

No payments, escrow state, private client records, owner fiat accounting, frontend or off-chain backend are required by Sever.
