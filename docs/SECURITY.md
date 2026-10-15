# Threat model, constraints, and failure handling

**Protected asset:** correct survivor set following a stipulated clause invalidation, for a frozen multiparty bargain.

| Threat | Defence | Residual limitation |
|---|---|---|
| Proposer edits text after ratification | Immutable seal/genesis, ratification binds exact digest | Parties must read what they sign |
| Fake legal invalidation | Every named party must endorse before finalization | An unwilling party can refuse to stipulate a genuine legal event; external courts are out of scope |
| Malicious leader omits dependency | Full ordered matrix, independently re-executed by validators, separate omission-oriented audit | All models can share semantic blind spots; live adversarial replay is necessary |
| Missing edge treated as independent | Exact `N×(N−1)` schema with strict ordering | No safe partial certification |
| Ambiguous clause link | `UNCERTAIN` propagates SUSPENDED when target fails | Can over-suspend; deliberate conservative bias |
| Dependency only indirectly impairs essential clause | Recompute transitive closure, collapse all on essential INVALID or SUSPENDED | Essentiality is explicitly agreed by parties, not inferred after the fact |
| Cross-agreement ID substitution | Agreement, clause ID and genesis pinned in calls and storage | Consumers must pin intended IDs/hash |
| Replaying old invalidation | Expected current head; one pending; finalized/rejected terminal flags | No automated re-opening/reversal of final invalidations |
| Minority malicious veto or unwilling signer | A nonproposer can reject pending proposal; unanimity is required | Availability tradeoff: cannot force disputed claims through without a separate trusted authority system |
| Spam open/reject loop | 12 opened attempts per agreement and a single pending slot | A malicious party can exhaust its own agreement's opening quota; this intentionally halts further proposals |
| Model prompt injection inside clauses | All clause content explicitly marked UNTRUSTED; validator reads immutable same text | Prompt-injection resistance is not absolute; must test live |
| Large consensus scope | At most six clauses, at most 30 directed edges, 800 chars/ clause | Does not scale to unbounded legal documents |
| Wrong chain deployment | Exact stable RPC chain-ID guard, pinned CLI version | Requires operator to check signed transactions and live results |
| Consumer performs unsafe transfers | Sever has no GEN movement. Sample consumer merely increments a counter | Downstream funds and authorization remain consumer responsibility |

## Safety choices

1. Uncertain relationships are not approved as safe independence.
2. Essential flags are party-authored and mutually ratified, never model-proposed.
3. A model cannot invalidate a clause, set payment terms, impose remedies or manufacture a replacement agreement.
4. Commitments are append-only: historical invalidation remains visible even after later failures.
5. All post-consensus graph effects are deterministic.
6. No administrative master key can rewrite active agreements or revive invalidated clauses.

## Known economic/design tradeoffs

- Strict unanimity sacrifices liveness to prevent adversarial unilateral invalidation.
- The graph is certified **once** at agreement activation, not refreshed using later outside evidence. Amendments require a new agreement.
- Consensus agreement on a full relation vector can be costly, especially at six clauses; no fixed fee guarantee is made.
- The contract cannot prove a clause is *legally* severable in any particular jurisdiction. Its output is the logical operability of a frozen synthetic bargain under party-ratified invalidation.
- The protocol is a **v1 bounded contract primitive** rather than an entire document parser, clause-renegotiation framework or legal execution platform.
- If a downstream consumer needs all clauses active, it must check every relevant clause, not just `is_agreement_operative`.
