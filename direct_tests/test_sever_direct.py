"""Official genlayer-test Direct Mode scenarios.

These exercise GenVM SDK semantics and mocked consensus responses; they are
not evidence of live StudioNet consensus or finalized network transactions.
"""


def fixture(direct_vm,direct_deploy,direct_alice,direct_bob):
    # The contract's pinned py-genlayer hash is present in this official
    # runner bundle. The current GenVM manager bundle moved legacy runners to
    # executor/v0.2.17/legacy-runners, which gltest-direct 0.29.0 cannot read.
    c=direct_deploy('contracts/sever.py', sdk_version='v0.3.0-rc7')
    from genlayer.py.types import Address
    direct_alice=Address(direct_alice)
    direct_bob=Address(direct_bob)
    direct_vm.sender=direct_alice
    aid=c.create_agreement('Delivery and support',
        'Two-party agreement for delivery and support. Only essential clauses collapse the whole bargain.')
    c.add_party(aid,direct_bob)
    delivery=c.add_clause(aid,'Delivery','Provider delivers five reports to the customer by Friday.',False)
    payment=c.add_clause(aid,'Payment','Customer pays only after accepting the five delivered reports.',False)
    training=c.add_clause(aid,'Training','Provider conducts a separate and independent training workshop.',False)
    genesis=c.seal_agreement(aid)
    c.ratify_agreement(aid,genesis)
    with direct_vm.prank(direct_bob):c.ratify_agreement(aid,genesis)
    c.activate_agreement(aid)
    ids=[delivery,payment,training]
    pairs=[[x,y] for x in ids for y in ids if x!=y]
    m={'edges':[[x,y,'REQUIRES' if (x,y)==(payment,delivery) else 'INDEPENDENT'] for x,y in pairs]}
    return c,aid,ids,genesis,m


def cert(direct_vm,c,aid,genesis,m):
    ids=sorted({x for edge in m['edges'] for x in edge[:2]})
    for batch_index in range(len(m['edges'])):
        pairs=m['edges'][batch_index][:2]
        pairs=[pairs]
        row={'edges':[edge[:] for edge in m['edges'] if edge[:2] in pairs]}
        direct_vm.mock_llm(fr'SEVER / LEADER BOUNDED PAIR {batch_index}',row)
        c.certify_dependency_batch(aid,genesis,batch_index)
    return c.finalize_dependency_certification(aid,genesis)


def test_sealed_ratification_and_head(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,a,ids,g,m=fixture(direct_vm,direct_deploy,direct_alice,direct_bob)
    assert c.get_agreement(a)['sealed']
    assert c.get_agreement(a)['active']
    assert c.get_agreement(a)['certified'] is False
    assert len(g)==64
    with direct_vm.expect_revert('SEALED'):
        c.add_clause(a,'bad','No amendment after sealing.',False)
    assert c.is_clause_operative(a,ids[0],g) is False


def test_certified_matrix_survival(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,a,ids,g,m=fixture(direct_vm,direct_deploy,direct_alice,direct_bob)
    gh=cert(direct_vm,c,a,g,m)
    assert len(gh)==64
    assert c.is_clause_operative(a,ids[0],g)
    assert c.get_graph(a)['edges'][0][2] in ('REQUIRES','INDEPENDENT','UNCERTAIN')
    head=c.agreement_head(a)
    f=c.propose_invalidation(a,ids[0],'Both parties stipulate delivery clause inoperative.',head)
    with direct_vm.expect_revert('INVALIDATION_NOT_UNANIMOUS'):
        c.finalize_invalidation(f,head)
    with direct_vm.prank(direct_bob):c.endorse_invalidation(f,head)
    h2=c.finalize_invalidation(f,head)
    assert h2!=head
    assert c.get_clause(ids[0])['status']=='INVALID'
    assert c.get_clause(ids[1])['status']=='SUSPENDED'
    assert c.get_clause(ids[2])['status']=='ACTIVE'
    assert not c.is_clause_operative(a,ids[1],g)
    assert c.is_clause_operative(a,ids[2],g)
    with direct_vm.expect_revert('STALE_OR_FINAL_FAILURE'):
        c.finalize_invalidation(f,head)


def test_validator_independently_checks_every_edge(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,a,ids,g,m=fixture(direct_vm,direct_deploy,direct_alice,direct_bob)
    cert(direct_vm,c,a,g,m)
    direct_vm.clear_mocks()
    ids=sorted({x for edge in m['edges'] for x in edge[:2]})
    batch_index=len(m['edges'])-1
    row_pairs=[m['edges'][batch_index][:2]]
    row={'edges':[edge[:] for edge in m['edges'] if edge[:2] in row_pairs]}
    direct_vm.mock_llm(fr'SEVER / INDEPENDENT BOUNDED PAIR {batch_index}',row)
    direct_vm.mock_llm(fr'SEVER / ADVERSARIAL DEPENDENCY AUDIT BATCH {batch_index}',{'ok':True})
    assert direct_vm.run_validator() is True


def test_validator_rejects_hidden_dependency(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,a,ids,g,m=fixture(direct_vm,direct_deploy,direct_alice,direct_bob)
    cert(direct_vm,c,a,g,m)
    hostile={'edges':[row[:] for row in m['edges']]}
    dependency_pair=[ids[2],ids[0]]
    batch_index=m['edges'].index(next(edge for edge in m['edges'] if edge[:2]==dependency_pair))
    row_pairs=[dependency_pair]
    row={'edges':[edge[:] for edge in hostile['edges'] if edge[:2] in row_pairs]}
    for edge in row['edges']:
        if edge[:2]==[ids[2],ids[0]]:edge[2]='REQUIRES'
    direct_vm.clear_mocks()
    direct_vm.mock_llm(fr'SEVER / INDEPENDENT BOUNDED PAIR {batch_index}',row)
    assert direct_vm.run_validator() is False


def test_validator_adversarial_veto(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,a,ids,g,m=fixture(direct_vm,direct_deploy,direct_alice,direct_bob)
    cert(direct_vm,c,a,g,m)
    direct_vm.clear_mocks()
    ids=sorted({x for edge in m['edges'] for x in edge[:2]})
    batch_index=len(m['edges'])-1
    row_pairs=[m['edges'][batch_index][:2]]
    row={'edges':[edge[:] for edge in m['edges'] if edge[:2] in row_pairs]}
    direct_vm.mock_llm(fr'SEVER / INDEPENDENT BOUNDED PAIR {batch_index}',row)
    direct_vm.mock_llm(fr'SEVER / ADVERSARIAL DEPENDENCY AUDIT BATCH {batch_index}',{'ok':False})
    assert direct_vm.run_validator() is False


def test_validator_malformed_full_matrix(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,a,ids,g,m=fixture(direct_vm,direct_deploy,direct_alice,direct_bob)
    cert(direct_vm,c,a,g,m)
    direct_vm.clear_mocks()
    ids=sorted({x for edge in m['edges'] for x in edge[:2]})
    batch_index=len(m['edges'])-1
    row_pairs=[m['edges'][batch_index][:2]]
    row={'edges':[edge[:] for edge in m['edges'] if edge[:2] in row_pairs]}
    direct_vm.mock_llm(fr'SEVER / INDEPENDENT BOUNDED PAIR {batch_index}',{'edges':row['edges'][:-1]})
    assert direct_vm.run_validator() is False


def test_veto_and_stale_head(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,a,ids,g,m=fixture(direct_vm,direct_deploy,direct_alice,direct_bob)
    cert(direct_vm,c,a,g,m)
    h=c.agreement_head(a)
    f=c.propose_invalidation(a,ids[0],'This is disputed and will be vetoed.',h)
    with direct_vm.prank(direct_bob):c.reject_invalidation(f)
    assert c.get_failure(f)['rejected'] is True
    assert c.agreement_head(a)==h
    with direct_vm.expect_revert('STALE_OR_FINAL_FAILURE'):
        c.finalize_invalidation(f,h)


def test_no_unilateral_invalidation(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
    c,a,ids,g,m=fixture(direct_vm,direct_deploy,direct_alice,direct_bob)
    cert(direct_vm,c,a,g,m)
    direct_vm.sender=direct_charlie
    with direct_vm.expect_revert('PARTY_ONLY'):
        c.propose_invalidation(a,ids[0],'Not a party',c.agreement_head(a))


def test_consumer_gates_action_on_provider_response(
    direct_vm,direct_deploy,direct_alice
):
    """Exercise consumer code with mocked Direct Mode transport responses."""
    # Load the pinned SDK before making an Address constructor argument; the
    # Direct Mode fixtures provide byte addresses until a contract is loaded.
    direct_deploy('contracts/sever.py',sdk_version='v0.3.0-rc7')
    from genlayer.py.types import Address
    import genlayer.gl.genvm_contracts as contract_registry
    contract_registry.__known_contract__=None
    provider_address=Address(direct_alice)
    consumer=direct_deploy(
        'contracts/sever_consumer_example.py',
        sdk_version='v0.3.0-rc7',
        sever_address=provider_address,
        agreement_id=17,
        clause_id=23,
        genesis_hash='a'*64,
    )
    from genlayer.py import calldata
    from genlayer.py.public_abi import ResultCode
    provider_state=[True]

    def cross_contract_read(vm,request):
        call=request.get('CallContract')
        if call is None:
            return None
        assert call['address'].as_bytes==provider_address.as_bytes
        invocation=call['calldata']
        assert invocation['method']=='is_clause_operative'
        assert invocation['args']==[17,23,'a'*64]
        return bytes([ResultCode.RETURN])+calldata.encode(provider_state[0])

    direct_vm._gl_call_hook=cross_contract_read
    consumer.do_clause_bound_action()
    assert consumer.action_count()==1
    provider_state[0]=False
    with direct_vm.expect_revert('SEVER_CLAUSE_NOT_OPERATIVE'):
        consumer.do_clause_bound_action()
    assert consumer.action_count()==1
    direct_vm._gl_call_hook=None
