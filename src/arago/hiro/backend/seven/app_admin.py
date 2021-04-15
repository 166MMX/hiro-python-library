from typing import TYPE_CHECKING, Final
from urllib.parse import quote

from arago.hiro.model.graph.vertex import Vertex
from arago.hiro.utils.cast_b import to_vertex

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro7AppAdminModel:
    _base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__()
        # TODO Bug https://itautopilot.zendesk.com/agent/tickets/7933
        # path = client.root.model.meta.version()['app-admin'].endpoint
        # if path.endswith('/'):
        #    path = path[:-1]
        path = '/api/app-admin/1.2'
        fork = client.fork(path)
        self._base_client = fork

    def deactivate(self, app_id: str) -> dict:
        # DELETE /$id
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/app-rest-api.html#_id_delete
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/graph-applications.html#deactivate
        # TODO result strange json vs Vertex
        # {'ogit/Auth/Application/status': 'inactive'}
        uri = '/%s' % quote(app_id, '')
        with self._base_client.request(
                'DELETE', uri, headers={'Accept': 'application/json'}
        ) as response:
            res_data = response.json()
            # vertex = to_vertex(res_data, self.__base_client)
            # return vertex[OgitAttribute.OGIT_AUTH_APPLICATION_STATUS] == 'inactive'
            return res_data


class Hiro7GraphAppAdminModel(Hiro7AppAdminModel):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)

    def create(self, name: str, description: str) -> Vertex:
        # returns ogit/Auth/Application Vertex
        # POST /$type
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/app-rest-api.html#_type_post
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/graph-applications.html#create
        uri = '/graph'
        req_data = {
            'ogit/name': name,
            'ogit/description': description,
        }
        with self._base_client.request(
                'POST', uri, headers={'Accept': 'application/json'}, json=req_data
        ) as response:
            res_data = response.json()
            vertex = to_vertex(res_data, self._base_client)
            return vertex

    def activate(self, app_id: str) -> dict:
        # PATCH /$id
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/app-rest-api.html#_id_patch
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/graph-applications.html#activate
        uri = '/%s' % quote(app_id, '')
        req_data = {}
        with self._base_client.request(
                'PATCH', uri, headers={'Accept': 'application/json'}, json=req_data
        ) as response:
            res_data = response.json()
            # TODO define model
            return res_data
