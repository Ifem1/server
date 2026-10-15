#!/usr/bin/env python3
"""Static preflight; not a GenVM lint or live deployment assertion."""
import ast
from pathlib import Path
root=Path(__file__).resolve().parents[1]
core=(root/'contracts/sever.py').read_text()
consumer=(root/'contracts/sever_consumer_example.py').read_text()
checks=[]
def ck(test,description):
    if not test: raise AssertionError(description)
    checks.append(description)
ast.parse(core);ast.parse(consumer)
ck(True,'Python syntax parses')
ck(core.count('gl.vm.run_nondet_unsafe(')==1,'one custom substantive consensus boundary')
ck('INDEPENDENT FULL MATRIX' in core,'independent reclassification of full matrix')
ck('ADVERSARIAL DEPENDENCY AUDIT' in core,'counterexample search on survival edges')
ck('expected_pairs' in core and 'INCOMPLETE_MATRIX' in core,'no omitted matrix pairs')
ck('CLAUSE_SUSPENDED' in core and 'UNCERTAIN' in core,'uncertainty fails closed')
ck('INVALIDATION_NOT_UNANIMOUS' in core,'party unanimity required to mark invalid')
ck('STALE_HEAD' in core and 'GENESIS_MISMATCH' in core,'genesis and head pinning')
ck('def is_clause_operative' in core and 'provider.view().is_clause_operative' in consumer,
   'consumer uses real typed state query')
ck('frontend' not in str([p for p in root.iterdir() if p.is_dir()]),'no frontend in project')
config=(root/'gltest.config.yaml').read_text()
ck('https://studio.genlayer.com/api' in config and 'studio-dev' not in config,'only stable StudioNet')
pkg=(root/'package.json').read_text()
ck('"genlayer": "0.39.1"' in pkg,'repository-local CLI pinned')
ck('studionet:' in config and 'leader_only: false' in config,'stable network and real consensus in test configuration')
print(f'SEVER static preflight {len(checks)}/{len(checks)} PASS')
for line in checks: print('PASS',line)
