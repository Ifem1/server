"""Minimal deterministic GenLayer adapter for offline state-machine tests.
This is *not* a GenVM simulator and tests make no claim of live consensus.
"""
import hashlib
import importlib.util
import sys
import types
from pathlib import Path
import pytest


class StorageMap(dict):
    def __init__(self, value_type):
        super().__init__()
        self.value_type=value_type
    def get_or_insert_default(self,key):
        if key not in self:
            obj=self.value_type.__new__(self.value_type)
            for name in ('parties','clause_ids','essential_ids','invalidations','certification_batches'):
                if name in getattr(self.value_type,'__annotations__',{}): setattr(obj,name,[])
            self[key]=obj
        return self[key]

class GenericType:
    def __class_getitem__(cls,item): return cls

class Emitter:
    def __init__(self,*args,**kwargs): pass
    def emit(self): pass

class Identity:
    def __call__(self, fn): return fn
    def __getattr__(self,name): return self

class Return:
    def __init__(self, calldata): self.calldata=calldata

class Stub:
    def __init__(self):
        self.public=Identity()
        self.message=types.SimpleNamespace(sender_address='0xAlice')
        self.vm=types.SimpleNamespace(UserError=ValueError,Return=Return,run_nondet_unsafe=self.run_nondet)
        self.nondet=types.SimpleNamespace(exec_prompt=self.exec_prompt)
        self.last_validator=None
        self.queued=[]
    def queue(self,*values): self.queued=list(values)
    def exec_prompt(self,prompt,response_format='json'):
        if not self.queued: raise ValueError('NO_MOCK_FOR_SEMANTIC_PROMPT')
        return self.queued.pop(0)
    def run_nondet(self,leader,validator):
        value=leader()
        self.last_validator=validator
        return value
    def independently_validate(self,*values):
        self.queue(*values)
        return self.last_validator(Return(self._proposed))
    def under(self,actor): self.message.sender_address=actor
    def capture(self,value): self._proposed=value


@pytest.fixture
def ctx():
    genlayer=types.ModuleType('genlayer')
    stub=Stub()
    genlayer.gl=stub
    genlayer.Address=str
    genlayer.u256=int
    genlayer.u32=int
    genlayer.u8=int
    genlayer.DynArray=GenericType
    genlayer.TreeMap=GenericType
    genlayer.allow_storage=Identity()
    genlayer.Keccak256=lambda raw: hashlib.sha3_256(raw)  # offline only
    stub.Contract=object
    stub.Event=Emitter
    stub.contract_interface=Identity()
    old=sys.modules.get('genlayer')
    sys.modules['genlayer']=genlayer
    try:
        path=Path(__file__).resolve().parents[1] / 'contracts' / 'sever.py'
        spec=importlib.util.spec_from_file_location('sever_offline',path)
        mod=importlib.util.module_from_spec(spec)
        sys.modules['sever_offline']=mod
        spec.loader.exec_module(mod)
        c=mod.Sever()
        for name,cls in [('agreements',mod.Agreement),('clauses',mod.Clause),('failures',mod.Failure)]:
            setattr(c,name,StorageMap(cls))
        for name in ['agreement_votes','failure_votes','edges']:
            setattr(c,name,StorageMap(int))
        yield mod,c,stub
    finally:
        if old is None: sys.modules.pop('genlayer',None)
        else: sys.modules['genlayer']=old
        sys.modules.pop('sever_offline',None)


@pytest.fixture
def active(ctx):
    m,c,stub=ctx
    a=c.create_agreement('Launch', 'Delivery and post-delivery support contract.')
    c.add_party(a,'0xBob')
    delivery=c.add_clause(a,'Delivery','Provider delivers five reports to customer on Friday.',False)
    payment=c.add_clause(a,'Payment','Customer pays provider on acceptance of the five delivered reports.',False)
    support=c.add_clause(a,'Support','Provider answers support questions about the accepted reports for 30 days.',False)
    unrelated=c.add_clause(a,'Training','Provider delivers an independent training course unrelated to the report delivery.',False)
    g=c.seal_agreement(a)
    c.ratify_agreement(a,g)
    stub.under('0xBob')
    c.ratify_agreement(a,g)
    stub.under('0xAlice')
    c.activate_agreement(a)
    ids=[delivery,payment,support,unrelated]
    pairs=m.expected_pairs(ids)
    depends={(payment,delivery),(support,delivery)}
    matrix={'edges':[[x,y,'REQUIRES' if (x,y) in depends else 'INDEPENDENT'] for x,y in pairs]}
    for batch_index in range(len(m.expected_pairs(ids))):
        row_pairs=m.batch_pairs(ids,batch_index)
        row={'edges':[edge[:] for edge in matrix['edges'] if edge[:2] in row_pairs]}
        stub.queue(row)
        c.certify_dependency_batch(a,g,batch_index)
        stub.capture({'edges':[[x,y,{'INDEPENDENT':m.REL_INDEPENDENT,
            'REQUIRES':m.REL_REQUIRES,'UNCERTAIN':m.REL_UNCERTAIN}[r]]
            for x,y,r in row['edges']]})
        stub.queue(row,{'ok':True})
        assert stub.last_validator(stub.vm.Return(stub._proposed)) is True
    graph=c.finalize_dependency_certification(a,g)
    return m,c,stub,a,ids,g,graph
