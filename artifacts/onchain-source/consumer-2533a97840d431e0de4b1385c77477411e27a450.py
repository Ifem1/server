# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Standalone example consumer. No frontend or payment dependency.
The user-supplied agreement/clause identifiers and genesis are pinned at deploy.
"""
from genlayer import *
from typing import Callable, Protocol, cast


class _PublicAPI(Protocol):
    @property
    def view(self) -> Callable[[Callable[..., object]], Callable[..., object]]: ...


_public: _PublicAPI = cast(_PublicAPI, gl.public)


class _TypedSeverRead(Protocol):
    def is_clause_operative(self, agreement_id: u256, clause_id: u256,
                            expected_genesis_hash: str) -> bool: ...


class _TypedSeverProxy(Protocol):
    def view(self) -> _TypedSeverRead: ...


@gl.contract_interface
class ISever:
    class View:
        def is_clause_operative(self, agreement_id: u256, clause_id: u256,
                                expected_genesis_hash: str) -> bool: ...


class SeverGatedConsumer(gl.Contract):
    sever_address: Address
    agreement_id: u256
    clause_id: u256
    genesis_hash: str
    actions: u256

    def __init__(self, sever_address: Address, agreement_id: u256,
                 clause_id: u256, genesis_hash: str):
        self.sever_address=sever_address
        self.agreement_id=agreement_id
        self.clause_id=clause_id
        self.genesis_hash=genesis_hash
        self.actions=u256(0)

    @gl.public.write
    def do_clause_bound_action(self) -> None:
        provider=cast(_TypedSeverProxy, ISever(self.sever_address))
        if not provider.view().is_clause_operative(
            self.agreement_id, self.clause_id, self.genesis_hash
        ):
            raise gl.vm.UserError('SEVER_CLAUSE_NOT_OPERATIVE')
        self.actions=u256(int(self.actions)+1)

    @_public.view
    def action_count(self) -> u256:
        return self.actions
