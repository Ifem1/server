# Builder integration guide

## Deployment order

The consumer constructor pins four values: a deployed Sever address, an agreement ID, a clause ID that belongs to that agreement, and the exact 64-character genesis hash returned by sealing the agreement. Create and certify an agreement before deploying the consumer. A placeholder or stale genesis does not identify an operative clause.

This repository targets stable StudioNet (`https://studio.genlayer.com/api`, chain ID `61999`) and pins `genlayer@0.39.1` locally. Confirm the target and wallet in the CLI before sending a transaction:

```powershell
npm ci
npm run cli:version
npm run network:guard
node_modules\.bin\genlayer.cmd network set studionet
node_modules\.bin\genlayer.cmd network info
node_modules\.bin\genlayer.cmd account list
```

Never put a private key or seed in this repository. Keep the CLI account in the local GenLayer wallet store.

## Create and activate an agreement

Deploy `contracts/sever.py` using the guarded script. It verifies the RPC chain ID and requires the literal confirmation `DEPLOY-61999`:

```powershell
npm run deploy:guarded
```

Record its finalized address and transaction ID. Then use that address to create a draft with `create_agreement(title, purpose)`. The creator adds the other party and between two and six clauses with `add_party` and `add_clause`; clause text and the essential flag freeze when the creator calls `seal_agreement`. The returned genesis hash commits to the party list, purpose, titles, text, clause IDs, and essential designations.

Every party must call `ratify_agreement(agreement_id, genesis_hash)` from their own address. Only then can anyone call `activate_agreement(agreement_id)`. Activation freezes an immutable certification epoch over the signed purpose, clause IDs, and clause text. Call `certify_dependency_batch(agreement_id, genesis_hash, batch_index)` once for each directed pair (indices `0` through `clause_count × (clause_count − 1) − 1`). Each validator independently classifies that pair and audits any proposed independent edge. Finally call `finalize_dependency_certification(agreement_id, genesis_hash)`. It rejects incomplete coverage and commits only after every ordered pair has been certified in the same epoch.

Use `get_agreement`, `get_clause`, `get_graph`, and `agreement_head` to inspect state. For state-changing calls, check the CLI receipt and trace and verify both finalization and successful execution before proceeding. Do not treat submission or an accepted receipt alone as completion.

## Bind the consumer

After certification, deploy `contracts/sever_consumer_example.py` with constructor values:

```text
sever_address: Address   deployed Sever contract
agreement_id:  integer   agreement containing the clause
clause_id:      integer   clause whose operation is required
genesis_hash:   string    exact sealed agreement genesis hash
```

The CLI accepts these types through its `deploy --args` option. Follow the CLI's quoting guidance for the local shell. Query `action_count()` to read the consumer's counter. `do_clause_bound_action()` calls the pinned provider's typed read-only `is_clause_operative(agreement_id, clause_id, genesis_hash)` before incrementing. It reverts with `SEVER_CLAUSE_NOT_OPERATIVE` when the provider says false; a provider-call failure also prevents the action from completing.

The guarded deploy helper validates the arguments and requires a separate operator confirmation. In PowerShell, set the values from the finalized Sever deployment and certified agreement, then run:

```powershell
$env:SEVER_ADDRESS = '0x...'
$env:AGREEMENT_ID = '1'
$env:CLAUSE_ID = '1'
$env:GENESIS_HASH = '<64 lowercase hex characters>'
npm run deploy:consumer:guarded
```

The example has no payment, transfer, or external side effect. Production consumers should make the Sever check and the protected effect part of one atomic transaction, pin the intended agreement and clause at construction or in an equally tamper-resistant way, and assess their own authorization and replay behavior.

## Party-stipulated invalidation

A listed party calls `propose_invalidation(agreement_id, clause_id, reason, expected_head)` with the current `agreement_head`. Every other party calls `endorse_invalidation(failure_id, expected_head)`; any non-proposer party can instead call `reject_invalidation(failure_id)`. Once all parties endorse, anyone can call `finalize_invalidation(failure_id, expected_head)`. The contract checks the expected head and recomputes the deterministic dependency closure.

After finalization, query `get_clause` and the `is_clause_operative` view. A direct or transitive dependent clause is suspended; an independent clause can remain active; impairment of any designated essential clause suspends the remaining bargain. The consumer test for rejection should target the exact pinned clause and verify both the consumer transaction's successful revert and an unchanged `action_count()`.

## API groups

- **Draft and freeze:** `create_agreement`, `add_party`, `add_clause`, `seal_agreement`.
- **Consent and activation:** `ratify_agreement`, `activate_agreement`.
- **Semantic graph:** `certify_dependency_batch`, `finalize_dependency_certification`, `get_graph`.
- **Stipulated failure:** `propose_invalidation`, `endorse_invalidation`, `reject_invalidation`, `finalize_invalidation`.
- **Read state:** `get_agreement`, `get_clause`, `get_failure`, `get_vote`, `agreement_head`, `is_clause_operative`, `is_agreement_operative`, `is_agreement_fully_operative`.

Generated ABIs are in `artifacts/sever-abi.json` and `artifacts/sever-consumer-abi.json`. They should be regenerated with the versioned validation procedure in `docs/TESTING.md` whenever the contract interface changes.
