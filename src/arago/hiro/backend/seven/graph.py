from functools import cached_property
from typing import Final, TYPE_CHECKING, Mapping, Any, Optional, Dict, Union, Iterable, Generator, overload, Literal
from urllib.parse import quote

from requests import Response

from arago.hiro.abc.common import AbcData
from arago.hiro.abc.graph import AbcGraphEdgeRest, AbcGraphEdgeData, AbcGraphEdgeModel, AbcGraphVertexRest, \
    AbcGraphVertexData, AbcGraphVertexModel, AbcGraphRest, AbcGraphData, AbcGraphModel
from arago.hiro.model.graph.attribute import ATTRIBUTE_T_co
from arago.hiro.model.graph.edge import EDGE_TYPE_T, Edge, EDGE_ID_T, EdgeId
from arago.hiro.model.graph.history import HistoryFormat, HistoryEntry, HistoryDiff
from arago.hiro.model.graph.vertex import Vertex, VertexId, VERTEX_T_co, VERTEX_TYPE_T, \
    VERTEX_XID_T_co, VersionId, VERTEX_ID_T_co
from arago.hiro.model.storage import BLOB_VERTEX_T_co, TIME_SERIES_VERTEX_T_co
from arago.hiro.utils import datetime
from arago.ogit import OgitVerb, OgitEntity
from arago.ontology import OntologyVerb

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro7GraphEdgeRest(AbcGraphEdgeRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        path = client.root.model.meta.version()['graph'].endpoint
        fork = client.fork(path)
        self.__base_client = fork

    def create(
            self,
            edge_type: str,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/connect/%s' % quote(edge_type, safe='')
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data
        )

    def delete(
            self,
            edge_id: str,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/%s' % quote(edge_id, safe='')
        return self.__base_client.request(
            'DELETE', uri, headers=headers
        )


class Hiro7GraphEdgeData(AbcGraphEdgeData):
    __rest_client: Final[Hiro7GraphEdgeRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro7GraphEdgeRest(client)

    def create(
            self,
            out_vertex_id: str,
            edge_type: str,
            in_vertex_id: str,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        # <editor-fold name="effective request data">
        e_req_data = {
            'out': out_vertex_id,
            'in': in_vertex_id,
        }
        if req_data is not None:
            if isinstance(req_data, Mapping):
                e_req_data.update(req_data)
            else:
                raise TypeError(type(req_data))
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        with self.__rest_client.create(edge_type, e_req_data, e_headers) as response:
            res_data = response.json()
            return res_data

    def delete(
            self,
            edge_id: str,
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

        with self.__rest_client.delete(edge_id, e_headers) as response:
            res_data = response.json()
            return res_data


class Hiro7GraphEdgeModel(AbcGraphEdgeModel):
    __data_client: Final[Hiro7GraphEdgeData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro7GraphEdgeData(client)

    def create(
            self,
            out_vertex_id: Union[Vertex, VERTEX_ID_T_co],
            edge_type: EDGE_TYPE_T,
            in_vertex_id: Union[Vertex, VERTEX_ID_T_co]
    ) -> Edge:
        if isinstance(out_vertex_id, Vertex):
            out_vertex_id = out_vertex_id.id
        elif isinstance(out_vertex_id, VertexId):
            out_vertex_id = str(out_vertex_id)
        elif isinstance(out_vertex_id, str):
            pass
        else:
            raise TypeError()

        if isinstance(edge_type, OntologyVerb):
            verb: OntologyVerb = edge_type
            edge_type = verb.name.uri
        elif isinstance(edge_type, OgitVerb):
            verb: OntologyVerb = edge_type.value
            edge_type = verb.name.uri
            del verb
        elif isinstance(edge_type, str):
            pass
        else:
            raise TypeError()

        if isinstance(in_vertex_id, Vertex):
            in_vertex_id = in_vertex_id.id
        elif isinstance(in_vertex_id, VertexId):
            in_vertex_id = str(in_vertex_id)
        elif isinstance(in_vertex_id, str):
            pass
        else:
            raise TypeError()

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
        elif isinstance(edge_id, EdgeId):
            edge_id = str(edge_id)
        elif isinstance(edge_id, str):
            pass
        else:
            raise TypeError()

        res_data = self.__data_client.delete(edge_id)
        edge = Edge(res_data)
        return edge


class Hiro7GraphVertexRest(AbcGraphVertexRest):
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
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/%s' % quote(vertex_id, safe='')
        return self.__base_client.request(
            'POST', uri, params=params, headers=headers, json=req_data
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


class Hiro7GraphVertexData(AbcGraphVertexData):
    __rest_client: Final[Hiro7GraphVertexRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro7GraphVertexRest(client)

    def create(
            self,
            vertex_type: str,
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

        with self.__rest_client.create(vertex_type, e_req_data, e_headers) as response:
            res_data = response.json()
            return res_data

    def get(
            self,
            vertex_id: str,
            include_deleted: Optional[bool] = None,  # server default: False
            v_id: Optional[str] = None,
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        # <editor-fold name="effective parameters">
        e_params = {}
        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_params['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if v_id is not None:
            if isinstance(v_id, str):
                e_params['vid'] = v_id
            else:
                raise TypeError(type(v_id))

        if fields is not None:
            if isinstance(fields, str):
                e_params['fields'] = fields
            elif isinstance(fields, Iterable):
                e_params['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_params['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

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
            include_deleted: Optional[bool] = None,  # server default: False
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective parameters">
        e_params = {}
        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_params['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if fields is not None:
            if isinstance(fields, str):
                e_params['fields'] = fields
            elif isinstance(fields, Iterable):
                e_params['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_params['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

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
            full_response: Optional[bool] = None,  # server default: False
            list_meta: Optional[bool] = None,  # server default: False
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        # <editor-fold name="effective parameters">
        e_params = {}
        if full_response is not None:
            if isinstance(list_meta, bool):
                e_params['fullResponse'] = str(full_response).lower()
            else:
                raise TypeError(type(full_response))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_params['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if params is not None:
            if isinstance(params, Mapping):
                e_params.update(params)
            else:
                raise TypeError(type(params))
        # </editor-fold>

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

        with self.__rest_client.update(vertex_id, e_req_data, e_params, e_headers) as response:
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
            include_deleted: Optional[bool] = False,  # server default: false
            version: Optional[int] = None,
            v_id: Optional[str] = None,
            start: Optional[int] = None,  # server default: 0
            end: Optional[int] = None,  # server default: now
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            res_format: Optional[str] = None,  # server default: element
            list_meta: Optional[bool] = False,  # server default: false
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective parameters">
        e_params = {}
        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_params['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if version is not None:
            if isinstance(version, int):
                e_params['version'] = '%i' % version
            else:
                raise TypeError(type(version))
        if v_id is not None:
            if isinstance(v_id, str):
                e_params['vid'] = v_id
            else:
                raise TypeError(type(v_id))

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

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_params['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

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

        with self.__rest_client.history(vertex_id, e_params, e_headers) as response:
            items = AbcData.items_generator(response)
            yield from items


class Hiro7GraphVertexModel(AbcGraphVertexModel):
    __base_client: Final['HiroRestBaseClient']
    __data_client: Final[Hiro7GraphVertexData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__base_client = client
        self.__data_client = Hiro7GraphVertexData(client)

    @overload
    def create(
            self,
            vertex: VERTEX_T_co
    ) -> VERTEX_T_co:
        ...

    @overload
    def create(
            self,
            vertex_type: Union[Literal['ogit/Attachment'], Literal[OgitEntity.OGIT_ATTACHMENT]],
            vertex: Optional[VERTEX_T_co] = None
    ) -> BLOB_VERTEX_T_co:
        ...

    @overload
    def create(
            self,
            vertex_type: Union[Literal['ogit/Timeseries'], Literal[OgitEntity.OGIT_TIME_SERIES]],
            vertex: Optional[VERTEX_T_co] = None
    ) -> TIME_SERIES_VERTEX_T_co:
        ...

    @overload
    def create(
            self,
            vertex_type: VERTEX_TYPE_T,
            vertex: Optional[VERTEX_T_co] = None
    ) -> VERTEX_T_co:
        ...

    def create(self, *args, **kwargs) -> VERTEX_T_co:
        raise NotImplementedError()

    @overload
    def get(
            self,
            vertex: VERTEX_T_co,
            include_deleted: Optional[bool] = None,  # server default: False
            v_id: Optional[VersionId] = None,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            list_meta: Optional[bool] = None  # server default: False
    ) -> VERTEX_T_co:
        ...

    @overload
    def get(
            self,
            vertex_id: VERTEX_ID_T_co,
            include_deleted: Optional[bool] = None,  # server default: False
            v_id: Optional[VersionId] = None,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            list_meta: Optional[bool] = None  # server default: False
    ) -> VERTEX_T_co:
        ...

    @overload
    def get(
            self,
            vertex_xid: VERTEX_XID_T_co,
            include_deleted: Optional[bool] = None,  # server default: False
            v_id: Optional[VersionId] = None,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            list_meta: Optional[bool] = None  # server default: False
    ) -> Generator[VERTEX_T_co, None, None]:
        ...

    def get(
            self, *args, **kwargs
    ) -> Union[VERTEX_T_co, Generator[VERTEX_T_co, None, None]]:
        raise NotImplementedError()

    def get_external(
            self,
            vertex_xid: VERTEX_XID_T_co,
            include_deleted: Optional[bool] = None,  # server default: False
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            list_meta: Optional[bool] = None  # server default: False
    ) -> Generator[VERTEX_T_co, None, None]:
        raise NotImplementedError()

    @overload
    def update(
            self,
            vertex: VERTEX_T_co,
            full_response: Optional[bool] = False,  # server default: false
            list_meta: Optional[bool] = False  # server default: false
    ) -> VERTEX_T_co:
        ...

    @overload
    def update(
            self,
            vertex_id: Union[VERTEX_ID_T_co, VERTEX_XID_T_co],
            vertex: VERTEX_T_co,
            full_response: Optional[bool] = False,  # server default: false
            list_meta: Optional[bool] = False  # server default: false
    ) -> VERTEX_T_co:
        ...

    @overload
    def update(
            self,
            vertex: VERTEX_T_co,
            source_vertex: VERTEX_T_co,
            full_response: Optional[bool] = False,  # server default: false
            list_meta: Optional[bool] = False  # server default: false
    ) -> VERTEX_T_co:
        ...

    def update(self, *args, **kwargs) -> Vertex:
        pass

    @overload
    def delete(
            self,
            vertex_id: Union[VERTEX_ID_T_co, VERTEX_XID_T_co]
    ) -> VERTEX_T_co:
        ...

    @overload
    def delete(
            self,
            vertex: VERTEX_T_co
    ) -> VERTEX_T_co:
        ...

    def delete(self, *args, **kwargs) -> Vertex:
        raise NotImplementedError()

    @overload
    def history(
            self,
            vertex_id: Union[VERTEX_T_co, VERTEX_ID_T_co, VERTEX_XID_T_co],
            res_format: Literal[HistoryFormat.DIFF],  # server default: element
            include_deleted: Optional[bool] = False,  # server default: false
            version: Optional[int] = None,
            v_id: Optional[VersionId] = None,
            start: Optional[datetime.datetime] = None,  # server default: 1970-01-01 00:00:00 Z
            end: Optional[datetime.datetime] = None,  # server default: now
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            list_meta: Optional[bool] = False  # server default: false
    ) -> Generator[HistoryDiff, None, None]:
        ...

    @overload
    def history(
            self,
            vertex_id: Union[VERTEX_T_co, VERTEX_ID_T_co, VERTEX_XID_T_co],
            res_format: Literal[HistoryFormat.FULL],  # server default: element
            include_deleted: Optional[bool] = False,  # server default: false
            version: Optional[int] = None,
            v_id: Optional[VersionId] = None,
            start: Optional[datetime.datetime] = None,  # server default: 1970-01-01 00:00:00 Z
            end: Optional[datetime.datetime] = None,  # server default: now
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            list_meta: Optional[bool] = False  # server default: false
    ) -> Generator[HistoryEntry, None, None]:
        ...

    @overload
    def history(
            self,
            vertex_id: Union[VERTEX_T_co, VERTEX_ID_T_co, VERTEX_XID_T_co],
            res_format: Optional[Literal[HistoryFormat.ELEMENT]],  # server default: element
            include_deleted: Optional[bool] = False,  # server default: false
            version: Optional[int] = None,
            v_id: Optional[VersionId] = None,
            start: Optional[datetime.datetime] = None,  # server default: 1970-01-01 00:00:00 Z
            end: Optional[datetime.datetime] = None,  # server default: now
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            list_meta: Optional[bool] = False  # server default: false
    ) -> Generator[Vertex, None, None]:
        ...

    def history(
            self, *args, **kwargs
    ) -> Generator[Union[HistoryEntry, HistoryDiff, Vertex], None, None]:
        raise NotImplementedError()


class Hiro7GraphRest(AbcGraphRest):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def edge(self) -> Hiro7GraphEdgeRest:
        return Hiro7GraphEdgeRest(self.__client)

    @cached_property
    def vertex(self) -> Hiro7GraphVertexRest:
        return Hiro7GraphVertexRest(self.__client)


class Hiro7GraphData(AbcGraphData):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def edge(self) -> Hiro7GraphEdgeData:
        return Hiro7GraphEdgeData(self.__client)

    @cached_property
    def vertex(self) -> Hiro7GraphVertexData:
        return Hiro7GraphVertexData(self.__client)


class Hiro7GraphModel(AbcGraphModel):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def edge(self) -> Hiro7GraphEdgeModel:
        return Hiro7GraphEdgeModel(self.__client)

    @cached_property
    def vertex(self) -> Hiro7GraphVertexModel:
        return Hiro7GraphVertexModel(self.__client)
