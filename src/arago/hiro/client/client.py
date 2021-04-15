from functools import cached_property, lru_cache
from typing import TypeVar, Optional

import requests
from requests.auth import AuthBase

from arago.extension.requests import HiroPasswordAuth
from arago.hiro.client.model_client import HiroRestClient, HiroDataClient, HiroModelClient
from arago.hiro.client.rest_base_client import HiroRestBaseClient
from arago.hiro.model.auth import ClientCredentials, AccountCredentials, SessionCredentials
from arago.hiro.model.graph.attribute import SystemAttribute
from arago.hiro.model.graph.vertex import VERTEX_XID_T_co, VERTEX_ID_T_co, VERTEX_T_co, \
    resolve_vertex_id, resolve_vertex_xid
from arago.hiro.utils.user_agent import build_user_agent

_AUTH_BASE_T_co = TypeVar('_AUTH_BASE_T_co', bound=AuthBase, covariant=True)


class HiroClient(HiroRestBaseClient):
    def __init__(self, parent: Optional['HiroRestBaseClient'] = None) -> None:
        super().__init__(parent)
        if parent is None:
            self.root = self

    def configure(self, endpoint: str, auth: _AUTH_BASE_T_co) -> None:
        self.endpoint = endpoint
        self.base_url = endpoint

        s = requests.Session()
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
        s.headers.update({
            'User-Agent': build_user_agent('HiroClient'),
            'Cache-Control': 'no-store',
        })
        s.auth = auth

        self.session, self.authenticator = s, auth

    @staticmethod
    def create_stringly(
            endpoint: str,
            client_id: str,
            client_secret: str,
            username: str,
            password: str
    ) -> 'HiroClient':
        credentials = SessionCredentials(
            ClientCredentials(client_id, client_secret),
            AccountCredentials(username, password)
        )
        client = HiroClient()
        auth = HiroPasswordAuth(client, credentials)
        client.configure(endpoint, auth)
        return client

    @cached_property
    def rest(self) -> HiroRestClient:
        return HiroRestClient(self)

    @cached_property
    def data(self) -> HiroDataClient:
        return HiroDataClient(self)

    @cached_property
    def model(self) -> HiroModelClient:
        return HiroModelClient(self)

    def resolve_vertex_id(
            self,
            vertex: VERTEX_T_co,
            vertex_id: VERTEX_ID_T_co,
            vertex_xid: VERTEX_XID_T_co
    ) -> VERTEX_ID_T_co:
        e_vertex_id = resolve_vertex_id(vertex, vertex_id)
        if e_vertex_id:
            return e_vertex_id

        e_vertex_xid = resolve_vertex_xid(vertex, vertex_xid)
        if e_vertex_xid:
            e_vertex_id = self.resolve_xid(e_vertex_xid)
            if e_vertex_id:
                return e_vertex_id

        raise RuntimeError()

    @lru_cache(maxsize=None, typed=True)
    def resolve_xid(self, vertex_xid: VERTEX_XID_T_co) -> VERTEX_ID_T_co:
        gen = self.model.search.external_id(vertex_xid, fields={
            SystemAttribute.OGIT__ID
        })
        vertex = next(gen)
        try:
            next(gen)
            raise RuntimeError(f'''External ID '{vertex_xid}' is ambiguous and is associated with multiple vertices''')
        except StopIteration:
            return vertex.id
