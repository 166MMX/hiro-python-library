from datetime import datetime
from functools import cached_property
from types import MappingProxyType
from typing import Dict, Any, overload, Optional, TYPE_CHECKING, Union, Mapping, Final, Generator, Literal, \
    Iterable
from urllib.parse import quote

from requests.models import Response

from arago.hiro.abc.auth import AbcData
from arago.hiro.abc.graph import AbcGraphEdgeRest, AbcGraphEdgeData, AbcGraphEdgeModel
from arago.hiro.abc.graph import AbcGraphRest, AbcGraphData, AbcGraphModel
from arago.hiro.abc.graph import AbcGraphVertexRest, AbcGraphVertexData, AbcGraphVertexModel
from arago.hiro.model.graph.attribute import ReadOnlyAttribute, FinalAttribute, SystemAttribute, to_attribute, \
    attribute_to_str, ATTRIBUTE_T_co
from arago.hiro.model.graph.dict import GraphDict
from arago.hiro.model.graph.edge import EdgeId, Edge, EDGE_ID_T, EDGE_TYPE_T
from arago.hiro.model.graph.history import HistoryFormat, HistoryEntry, HistoryDiff, HistoryMeta, HistoryAction
from arago.hiro.model.graph.vertex import VertexId, Vertex, resolve_vertex_id, VERTEX_T, VERTEX_ID_T, VERTEX_TYPE_T, \
    VERTEX_T_co, ExternalVertexId, VERTEX_XID_T_co, resolve_vertex_type, VERTEX_ID_T_co, to_vertex_id, to_vertex_xid, \
    vertex_id_to_str
from arago.hiro.model.storage import BLOB_VERTEX_T_co, TIME_SERIES_VERTEX_T_co
from arago.hiro.utils.cast_c import to_vertex
from arago.hiro.utils.datetime import datetime_to_timestamp_ms
from arago.ogit import OgitAttribute
from arago.ogit import OgitEntity
from arago.ogit import OgitVerb
from arago.ontology import OntologyEntity, OntologyVerb, Attribute

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


# https://pod1159.saasarago.com/_api/index.html
# https://pod1159.saasarago.com/_api/specs/api.yaml
# https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/rest-api.html


class Hiro6GraphEdgeRest(AbcGraphEdgeRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        path = client.root.model.meta.version()['graph'].endpoint
        fork = client.fork(path)
        self.__base_client = fork

    def create(self, edge_type: str, req_data: Mapping[str, Any]) -> Response:
        uri = '/connect/%s' % quote(edge_type, safe='')
        return self.__base_client.request(
            'POST', uri, headers={'Accept': 'application/json'}, json=req_data
        )

    def delete(self, edge_id: str) -> Response:
        uri = '/%s' % quote(edge_id, safe='')
        return self.__base_client.request(
            'DELETE', uri, headers={'Accept': 'application/json'}
        )


class Hiro6GraphEdgeData(AbcGraphEdgeData):
    __rest_client: Final[Hiro6GraphEdgeRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6GraphEdgeRest(client)

    def create(self, out_vertex_id: str, edge_type: str, in_vertex_id: str) -> Dict[str, Any]:
        req_data = {
            'out': out_vertex_id,
            'in': in_vertex_id,
        }
        with self.__rest_client.create(edge_type, req_data) as response:
            res_data = response.json()
            return res_data

    def delete(self, edge_id: str) -> Dict[str, Any]:
        with self.__rest_client.delete(edge_id) as response:
            res_data = response.json()
            return res_data


class Hiro6GraphEdgeModel(AbcGraphEdgeModel):
    __data_client: Final[Hiro6GraphEdgeData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro6GraphEdgeData(client)

    def create(
            self,
            out_vertex_id: Union[Vertex, VERTEX_ID_T],
            edge_type: EDGE_TYPE_T,
            in_vertex_id: Union[Vertex, VERTEX_ID_T]
    ) -> Edge:
        if isinstance(out_vertex_id, Vertex):
            out_vertex_id = out_vertex_id.id
        if isinstance(out_vertex_id, VertexId):
            out_vertex_id = str(out_vertex_id)
        if isinstance(edge_type, OntologyVerb):
            verb: OntologyVerb = edge_type
            edge_type = verb.name.uri
        elif isinstance(edge_type, OgitVerb):
            verb: OntologyVerb = edge_type.value
            edge_type = verb.name.uri
            del verb
        if isinstance(in_vertex_id, Vertex):
            in_vertex_id = in_vertex_id.id
        if isinstance(in_vertex_id, VertexId):
            in_vertex_id = str(in_vertex_id)
        res_data = self.__data_client.create(
            out_vertex_id, edge_type, in_vertex_id
        )
        edge = Edge(res_data)
        return edge

    def delete(
            self,
            edge_id: Union[Edge, EDGE_ID_T]
    ) -> Edge:
        if isinstance(edge_id, Edge):
            edge_id = edge_id.id
        if isinstance(edge_id, EdgeId):
            edge_id = str(edge_id)
        res_data = self.__data_client.delete(edge_id)
        edge = Edge(res_data)
        return edge


class Hiro6GraphVertexRest(AbcGraphVertexRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        path = client.root.model.meta.version()['graph'].endpoint
        fork = client.fork(path)
        self.__base_client = fork

    def create(
            self,
            vertex_type: str,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/new/%s' % quote(vertex_type, safe='')
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data
        )

    def get(
            self,
            vertex_id: str,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/%s' % quote(vertex_id, safe='')
        return self.__base_client.request(
            'GET', uri, params=params, headers=headers
        )

    # TODO remove - move to search?!?
    def get_external(
            self,
            vertex_xid: str,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/xid/%s' % quote(vertex_xid, safe='')
        return self.__base_client.request(
            'GET', uri, params=params, headers=headers
        )

    def update(
            self,
            vertex_id: str,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/%s' % quote(vertex_id, safe='')
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data
        )

    def delete(
            self,
            vertex_id: str,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/%s' % quote(vertex_id, safe='')
        return self.__base_client.request(
            'DELETE', uri, headers=headers
        )

    def history(
            self,
            vertex_id: str,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/%s/history' % quote(vertex_id, safe='')
        return self.__base_client.request(
            'GET', uri, params=params, headers=headers, stream=True
        )


class Hiro6GraphVertexData(AbcGraphVertexData):
    __rest_client: Final[Hiro6GraphVertexRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6GraphVertexRest(client)

    def create(
            self,
            vertex_type: str,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        e_req_data = req_data if req_data else {}

        e_headers = {'Accept': 'application/json'}
        if isinstance(headers, Mapping):
            e_headers.update(headers)

        with self.__rest_client.create(vertex_type, e_req_data, e_headers) as response:
            res_data = response.json()
            return res_data

    def get(
            self,
            vertex_id: str,
            fields: Optional[Union[str, Iterable[str]]] = None,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        # <editor-fold name="effective parameters">
        e_params = {}
        if fields is not None:
            if isinstance(fields, str):
                e_params['fields'] = fields
            elif isinstance(fields, Iterable):
                e_params['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if params is not None:
            if isinstance(params, Mapping):
                e_params.update(params)
            else:
                raise TypeError(type(params))
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        with self.__rest_client.get(vertex_id, e_params, e_headers) as response:
            res_data = response.json()
            return res_data

    def get_external(
            self,
            vertex_xid: str,
            fields: Optional[Union[str, Iterable[str]]] = None,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective parameters">
        e_params = {}
        if fields is not None:
            if isinstance(fields, str):
                e_params['fields'] = fields
            elif isinstance(fields, Iterable):
                e_params['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if params is not None:
            if isinstance(params, Mapping):
                e_params.update(params)
            else:
                raise TypeError(type(params))
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        with self.__rest_client.get_external(vertex_xid, e_params, e_headers) as response:
            items = AbcData.items_generator(response)
            yield from items

    def update(
            self,
            vertex_id: str,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        # <editor-fold name="effective request data">
        e_req_data = req_data if req_data else {}
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        with self.__rest_client.update(vertex_id, e_req_data, e_headers) as response:
            res_data = response.json()
            return res_data

    def delete(
            self,
            vertex_id: str,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        with self.__rest_client.delete(vertex_id, e_headers) as response:
            res_data = response.json()
            return res_data

    def history(
            self,
            vertex_id: str,
            start: Optional[int] = None,
            end: Optional[int] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            res_format: Optional[str] = None,
            version: Optional[int] = None,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective parameters">
        e_params = {}
        # TODO add support for undocumented includeDeleted value must be lowercase literal string 'true'
        # e_params['includeDeleted'] = 'true'

        if version is not None:
            if isinstance(version, int):
                e_params['version'] = '%i' % version
            else:
                raise TypeError(type(version))

        if start is not None:
            if isinstance(start, int):
                e_params['from'] = '%011i' % start
            else:
                raise TypeError(type(start))
        if end is not None:
            if isinstance(end, int):
                e_params['to'] = '%011i' % end
            else:
                raise TypeError(type(end))

        if offset is not None:
            if isinstance(offset, int):
                if offset > 0:
                    e_params['offset'] = '%i' % offset
                else:
                    raise ValueError('Offset must be an integer greater zero')
            else:
                raise TypeError(type(offset))
        else:
            e_params['offset'] = 0
        if limit is not None:
            if isinstance(limit, int):
                if limit > 0:
                    e_params['limit'] = '%i' % limit
                else:
                    raise ValueError('Limit must be an integer greater zero')
            else:
                raise TypeError(type(limit))
        else:
            e_params['limit'] = -1

        if res_format is not None:
            if isinstance(res_format, str):
                e_params['type'] = res_format
            else:
                raise TypeError(type(res_format))

        if params is not None:
            if isinstance(params, Mapping):
                e_params.update(params)
            else:
                raise TypeError(type(params))
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        response = self.__rest_client.history(vertex_id, e_params, e_headers)
        items = AbcData.items_generator(response)
        yield from items


class Hiro6GraphVertexModel(AbcGraphVertexModel):
    __base_client: Final['HiroRestBaseClient']
    __data_client: Final[Hiro6GraphVertexData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__base_client = client
        self.__data_client = Hiro6GraphVertexData(client)

    @overload
    def create(self, vertex: VERTEX_T) -> VERTEX_T_co:
        ...

    @overload
    def create(
            self,
            vertex_type: Union[Literal['ogit/Attachment'], Literal[OgitEntity.OGIT_ATTACHMENT]],
            vertex: Optional[VERTEX_T] = None
    ) -> BLOB_VERTEX_T_co:
        ...

    @overload
    def create(
            self,
            vertex_type: Union[Literal['ogit/Timeseries'], Literal[OgitEntity.OGIT_TIME_SERIES]],
            vertex: Optional[VERTEX_T] = None
    ) -> TIME_SERIES_VERTEX_T_co:
        ...

    @overload
    def create(
            self,
            vertex_type: VERTEX_TYPE_T,
            vertex: Optional[VERTEX_T] = None
    ) -> VERTEX_T_co:
        ...

    # @overload
    # def create(
    #         self,
    #         vertex_type: Literal[OgitEntity.OGIT_DATA_LOG, 'ogit/Data/Log'],
    #         vertex: Optional[VERTEX_T] = None
    # ) -> LogVertex:
    #     ...

    def create(self, *args, **kwargs) -> VERTEX_T_co:
        if not args and not kwargs:
            raise RuntimeError('Missing args and or kwargs')
        vertex: Optional[VERTEX_T] = None
        vertex_type: Optional[VERTEX_TYPE_T] = None
        if len(args) == 1:
            v = args[0]
            if isinstance(v, Vertex):
                vertex = v
                vertex_type = v.type
            elif isinstance(v, Mapping):
                vertex = GraphDict(v)
                if OgitAttribute.OGIT__TYPE in vertex:
                    vertex_type = vertex[OgitAttribute.OGIT__TYPE]
                else:
                    raise KeyError(f'Missing {OgitAttribute.OGIT__TYPE} key in mapping')
            elif isinstance(v, OgitEntity):
                vertex_type = v.value.name.uri
                vertex = None
            elif isinstance(v, OntologyEntity):
                vertex_type = v.name.uri
                vertex = None
            elif isinstance(v, str):
                vertex_type = v
                vertex = None
            else:
                raise TypeError(
                    f'type(args[0]): {type(v)}; expected: Union[str, Entity, Vertex, Mapping[Union[str, Attribute], Any]]')
            del v
        elif len(args) == 2:
            for i, v in enumerate(args):
                if i == 0:
                    if isinstance(v, OgitEntity):
                        vertex_type = v.value.name.uri
                    elif isinstance(v, OntologyEntity):
                        vertex_type = v.name.uri
                    elif isinstance(v, str):
                        vertex_type = v
                    else:
                        raise TypeError(f'args[0]: expected: Union[str, Entity]; got: {type(v)}')
                elif i == 1:
                    if isinstance(v, (Vertex, Mapping)):
                        vertex = v
                    else:
                        raise TypeError(
                            f'args[1]: expected: Union[Vertex, Mapping[Union[str, Attribute], Any]]; got: {type(v)}')
                else:
                    raise RuntimeError('Unreachable')
            del i, v
        else:
            raise RuntimeError('Too much args; max 2')
        if kwargs:
            for k, v in kwargs.items():
                if k == 'vertex_type':
                    if isinstance(v, OgitEntity):
                        vertex_type = v.value.name.uri
                    elif isinstance(v, OntologyEntity):
                        vertex_type = v.name.uri
                    elif isinstance(v, str):
                        vertex_type = v
                    else:
                        raise TypeError(f'kwargs[\'{k}\']: expected: Union[str, Entity]; got: {type(v)}')
                elif k == 'vertex':
                    if isinstance(v, (Vertex, Mapping)):
                        vertex = v
                    else:
                        raise TypeError(
                            f'kwargs[\'{k}\']: expected: Union[Vertex, Mapping[Union[str, Attribute], Any]]; got: {type(v)}')
                else:
                    raise KeyError(f'''Unexpected key '{k}' found''')
            del k, v

        e_vertex_type = resolve_vertex_type(vertex, vertex_type)

        if vertex is None:
            req_data = {}
        elif isinstance(vertex, Vertex):
            req_data = vertex.to_dict()
        elif isinstance(vertex, Mapping):
            req_data = GraphDict(vertex).to_dict()
        else:
            raise RuntimeError('unreachable')  # has to be caught earlier

        for k, v in req_data.items():
            if isinstance(v, OgitEntity):
                req_data[k] = v.value.name.uri
            elif isinstance(v, OntologyEntity):
                req_data[k] = v.name.uri

        # TODO if 'ogit/_owner' not in vertex:  logging.warn() HIRO 6

        res_data = self.__data_client.create(e_vertex_type.name.uri, req_data)
        vertex = to_vertex(res_data, self.__base_client)
        return vertex

    @overload
    def get(
            self,
            vertex: VERTEX_T,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None
    ) -> VERTEX_T_co:
        ...

    @overload
    def get(
            self,
            vertex_id: VERTEX_ID_T,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None
    ) -> VERTEX_T_co:
        ...

    @overload
    def get(
            self,
            vertex_xid: VERTEX_XID_T_co,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None
    ) -> VERTEX_T_co:
        ...

    def get(self, *args, **kwargs) -> VERTEX_T_co:
        if not args and not kwargs:
            raise RuntimeError('Missing args and or kwargs')
        vertex: Optional[VERTEX_T] = None
        vertex_id: Optional[VERTEX_ID_T] = None
        vertex_xid: Optional[VERTEX_XID_T_co] = None
        fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None
        if len(args) == 1:
            v = args[0]
            if isinstance(v, ExternalVertexId):
                vertex_xid = v
            elif isinstance(v, (VertexId, str)):
                vertex_id = to_vertex_id(v)
            elif isinstance(v, (Vertex, Mapping)):
                vertex = v
            else:
                raise TypeError(type(v))
            del v
        elif len(args) == 2:
            for i, v in enumerate(args):
                if i == 0:
                    if isinstance(v, ExternalVertexId):
                        vertex_xid = v
                    elif isinstance(v, (VertexId, str)):
                        vertex_id = to_vertex_id(v)
                    elif isinstance(v, (Vertex, Mapping)):
                        vertex = v
                    else:
                        raise TypeError(type(v))
                elif i == 1:
                    if isinstance(v, Attribute):
                        fields = v
                    elif isinstance(v, Iterable):
                        fields = v
                    else:
                        raise TypeError(type(v))
                else:
                    raise RuntimeError('Unreachable')
            del i, v
        else:
            raise RuntimeError('Too much args; max 2')
        if kwargs:
            for k, v in kwargs.items():
                if k == 'vertex_id':
                    if isinstance(v, (VertexId, str)):
                        vertex_id = to_vertex_id(v)
                    else:
                        raise TypeError(type(v))
                elif k == 'vertex_xid':
                    if isinstance(v, (ExternalVertexId, str)):
                        vertex_xid = to_vertex_xid(v)
                    else:
                        raise TypeError(type(v))
                elif k == 'fields':
                    if isinstance(v, Iterable):
                        fields = v
                    else:
                        raise TypeError(type(v))
                elif k == 'vertex':
                    if isinstance(v, (Vertex, Mapping)):
                        vertex = v
                    else:
                        raise TypeError(type(v))
                else:
                    raise KeyError(k)
            del k, v

        e_vertex_id = self.__base_client.root.resolve_vertex_id(vertex, vertex_id, vertex_xid)
        e_fields = (attribute_to_str(field) for field in fields) if fields else None

        res_data = self.__data_client.get(str(e_vertex_id), e_fields)
        vertex = to_vertex(res_data, self.__base_client)
        return vertex

    def get_external(
            self,
            vertex_xid: VERTEX_XID_T_co,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        e_fields = (attribute_to_str(field) for field in fields) if fields else None

        items = self.__data_client.get_external(str(vertex_xid), e_fields)
        for item in items:
            vertex = to_vertex(item, self.__base_client)
            yield vertex

    @overload
    def update(self, vertex: VERTEX_T) -> VERTEX_T_co:
        """
        Update graph vertex with local updated vertex
        """
        ...

    @overload
    def update(self, vertex_id: Union[VERTEX_ID_T, VERTEX_XID_T_co], vertex: VERTEX_T) -> VERTEX_T_co:
        """
        Update vertex id with attributes defined in vertex
        """
        ...

    @overload
    def update(self, vertex: VERTEX_T, source_vertex: VERTEX_T) -> VERTEX_T_co:
        """
        Update (target) vertex with attributes defined in source vertex
        """
        ...

    def update(self, *args, **kwargs) -> Vertex:
        if not args and not kwargs:
            raise RuntimeError('Missing args and or kwargs')
        vertex: Optional[VERTEX_T] = None
        vertex_id: Optional[Union[VERTEX_ID_T, VERTEX_XID_T_co]] = None
        source_vertex: Optional[VERTEX_T] = None
        if len(args) == 1:
            v = args[0]
            if isinstance(v, Vertex):
                vertex = v
                if v.id:
                    vertex_id = v.id
                elif v.xid:
                    vertex_id = v.xid
            elif isinstance(v, Mapping):
                vertex = GraphDict(v)
                if OgitAttribute.OGIT__ID in vertex:
                    vertex_id = vertex[OgitAttribute.OGIT__ID]
                elif OgitAttribute.OGIT__XID in vertex:
                    vertex_id = vertex[OgitAttribute.OGIT__XID]
                else:
                    raise KeyError(f'Missing {OgitAttribute.OGIT__ID} or {OgitAttribute.OGIT__XID} key in mapping')
            else:
                raise TypeError(type(v))
            del v
        elif len(args) == 2:
            for i, v in enumerate(args):
                if i == 0:
                    if isinstance(v, (VertexId, ExternalVertexId, str)):
                        vertex_id = v
                    elif isinstance(v, (Vertex, Mapping)):
                        vertex_id = resolve_vertex_id(v, None)
                    else:
                        raise TypeError(type(v))
                elif i == 1:
                    if isinstance(v, (Vertex, Mapping)):
                        vertex = v
                    else:
                        raise TypeError(type(v))
                else:
                    raise RuntimeError('Unreachable')
            del i, v
        else:
            raise TypeError('Too much args; max 2')
        if kwargs:
            for k, v in kwargs.items():
                if k == 'vertex_id':
                    if isinstance(v, (VertexId, ExternalVertexId, str)):
                        vertex_id = v
                    else:
                        raise TypeError(type(v))
                elif k in ('vertex', 'source_vertex'):
                    if isinstance(v, (Vertex, Mapping)):
                        if k == 'vertex':
                            vertex = v
                        elif k == 'source_vertex':
                            source_vertex = v
                        else:
                            raise TypeError(type(v))
                    else:
                        raise TypeError(type(v))
                else:
                    raise KeyError(k)
            del k, v

        e_vertex_id = resolve_vertex_id(vertex, vertex_id)

        if isinstance(e_vertex_id, ExternalVertexId):
            e_vertex_id = self.get(e_vertex_id, (OgitAttribute.OGIT__ID,)).id

        if isinstance(source_vertex, Vertex):
            req_data = source_vertex.to_dict()
        elif isinstance(vertex, Vertex):
            req_data = vertex.to_dict()
        elif isinstance(source_vertex, Mapping):
            req_data = GraphDict(source_vertex).to_dict()
        elif isinstance(vertex, Mapping):
            req_data = GraphDict(vertex).to_dict()
        else:
            raise RuntimeError('unreachable')  # has to be caught earlier

        m: ReadOnlyAttribute
        for m in tuple(ReadOnlyAttribute):
            k = m.value.name.uri
            if k in req_data:
                del req_data[k]

        m: FinalAttribute
        for m in tuple(FinalAttribute):
            k = m.value.name.uri
            if k is SystemAttribute.OGIT__XID.value:
                if isinstance(vertex, Vertex) \
                        and not vertex._draft \
                        and vertex._orig_xid is None:
                    # only update(set) xid if xid was not set before
                    continue
                else:
                    # we have a map and don't know about the graph state
                    continue
            if k in req_data:
                del req_data[k]
        del m, k

        res_data = self.__data_client.update(e_vertex_id, req_data)
        vertex = to_vertex(res_data, self.__base_client)
        return vertex

    @overload
    def delete(self, vertex: VERTEX_T_co) -> VERTEX_T_co:
        ...

    @overload
    def delete(self, vertex_id: Union[VERTEX_ID_T_co, VERTEX_XID_T_co]) -> VERTEX_T_co:
        ...

    def delete(self, *args, **kwargs) -> Vertex:
        if not args and not kwargs:
            raise RuntimeError('Missing args and or kwargs')
        vertex: Optional[VERTEX_T] = None
        vertex_id: Optional[Union[VERTEX_ID_T, VERTEX_XID_T_co]] = None
        if len(args) == 1:
            v = args[0]
            if isinstance(v, (VertexId, ExternalVertexId, str)):
                vertex_id = v
            elif isinstance(v, (Vertex, Mapping)):
                vertex = v
            else:
                raise TypeError(type(v))
            del v
        else:
            raise TypeError('Too much args; max 1')
        if kwargs:
            for k, v in kwargs.items():
                if k == 'vertex_id':
                    if isinstance(v, (VertexId, ExternalVertexId, str)):
                        vertex_id = v
                    else:
                        raise TypeError(type(v))
                elif k == 'vertex':
                    if isinstance(v, (Vertex, Mapping)):
                        vertex = v
                    else:
                        raise TypeError(type(v))
                else:
                    raise KeyError(k)
            del k, v

        e_vertex_id = resolve_vertex_id(vertex, vertex_id)

        if isinstance(e_vertex_id, ExternalVertexId):
            e_vertex_id = self.get(e_vertex_id, (OgitAttribute.OGIT__ID,)).id

        res_data = self.__data_client.delete(e_vertex_id)
        vertex = to_vertex(res_data, self.__base_client)
        return vertex

    def history(
            self,
            vertex_id: Union[VERTEX_T_co, VERTEX_ID_T_co, VERTEX_XID_T_co],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            res_format: Optional[HistoryFormat] = None,
            version: Optional[int] = None,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Union[HistoryEntry, HistoryDiff, Vertex], None, None]:
        e_vertex_id = vertex_id_to_str(vertex_id)
        e_start = datetime_to_timestamp_ms(start) if isinstance(start, datetime) else None
        e_end = datetime_to_timestamp_ms(end) if isinstance(end, datetime) else None
        e_format = res_format.value if isinstance(res_format, HistoryFormat) else None
        if res_format is None or res_format is HistoryFormat.ELEMENT:
            def transform(src_item: Dict[str, Any]) -> Vertex:
                return Vertex(src_item, self.__base_client, False)  # frozen=True
        elif res_format is HistoryFormat.DIFF:
            def transform_map(mapping: Mapping[str, Any]) -> Dict[Attribute, Any]:
                result = {}
                for k, v in mapping.items():
                    a = to_attribute(k)
                    result[a] = v
                return result

            def transform(src_item: Dict[str, Any]) -> HistoryDiff:
                return HistoryDiff(
                    added=MappingProxyType(transform_map(src_item['add'])),
                    replaced=MappingProxyType(transform_map(src_item['replace'])),
                    removed=MappingProxyType(transform_map(src_item['remove']))
                )
        elif res_format is HistoryFormat.FULL:
            def transform(src_item: Dict[str, Any]) -> HistoryEntry:
                data_id = VertexId(src_item['identity'])
                action = HistoryAction[src_item['action']]
                data = to_vertex(src_item['data'], self.__base_client)
                meta = HistoryMeta(**src_item['meta'])
                return HistoryEntry(data_id, action, data, meta)
        elif not isinstance(res_format, HistoryFormat):
            raise TypeError(type(res_format))
        else:
            raise RuntimeError('Unreachable')

        for item in self.__data_client.history(
                e_vertex_id, start=e_start, end=e_end,
                offset=offset, limit=limit,
                res_format=e_format,
                version=version,
                params=params, headers=headers):
            yield transform(item)


class Hiro6GraphRest(AbcGraphRest):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def edge(self) -> Hiro6GraphEdgeRest:
        return Hiro6GraphEdgeRest(self.__client)

    @cached_property
    def vertex(self) -> Hiro6GraphVertexRest:
        return Hiro6GraphVertexRest(self.__client)


class Hiro6GraphData(AbcGraphData):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def edge(self) -> Hiro6GraphEdgeData:
        return Hiro6GraphEdgeData(self.__client)

    @cached_property
    def vertex(self) -> Hiro6GraphVertexData:
        return Hiro6GraphVertexData(self.__client)


class Hiro6GraphModel(AbcGraphModel):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def edge(self) -> Hiro6GraphEdgeModel:
        return Hiro6GraphEdgeModel(self.__client)

    @cached_property
    def vertex(self) -> Hiro6GraphVertexModel:
        return Hiro6GraphVertexModel(self.__client)
