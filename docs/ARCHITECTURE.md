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

## One-shot full matrix consensus

For N clauses, validators must classify **N × (N−1)** ordered pairs. No edge is optional, including edges that appear unrelated. The leader's normalized output schema requires all edges in one exact deterministic order. Malformed/truncated/duplicated/reordered matrices are rejected.

On validation, validators independently recompute the entire directed relation vector **from the frozen agreement**. Every relation label must match, not just graph size or JSON formatting. Then a second adversarial check explicitly attempts to find any suppressed dependency among edges labeled INDEPENDENT. A validator rejects if an omitted material dependency or unresolved safety doubt exists.

The stored graph contains only consensus-bound relation labels, not natural-language rationales masquerading as agreed facts. Semantic disagreements may cause retries, rotations or appeals under normal GenLayer consensus; there is no local “majority vote” shortcut in the contract.

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
