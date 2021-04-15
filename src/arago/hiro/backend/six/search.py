import logging
from typing import Dict, Any, Generator, Tuple, Union, TYPE_CHECKING, Mapping, Type, Optional, Final, Iterable, \
    Literal
from urllib.parse import quote

from requests.models import Response

from arago.hiro.abc.common import AbcData
from arago.hiro.abc.search import AbcSearchRest, AbcSearchData, AbcSearchModel, T
from arago.hiro.model.graph.attribute import attribute_to_str, ATTRIBUTE_T_co
from arago.hiro.model.graph.edge import EDGE_TYPE_T
from arago.hiro.model.graph.vertex import Vertex, VERTEX_XID_T, external_id_to_str, VERTEX_ID_T, \
    VERTEX_TYPE_T, VERTEX_T_co, vertex_type_to_str, VERTEX_XID_T_co, ExternalVertexId, vertex_id_to_str
from arago.hiro.model.search import Order
from arago.hiro.utils.cast_c import to_vertices

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro6SearchRest(AbcSearchRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__base_client = client

    def connected(
            self,
            vertex_id: str,
            edge_type: str,
            params: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/%s/%s' % (
            quote(vertex_id, safe=''),
            quote(edge_type, safe='')
        )
        return self.__base_client.request(
            'GET', uri, headers=headers, params=params, stream=stream
        )

    def external_id(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/query/xid'
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data, stream=stream
        )

    def get_by_ids(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/query/ids'
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data, stream=stream
        )

    def index(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/query/vertices'
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data, stream=stream
        )

    def graph(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/query/gremlin'
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data, stream=stream
        )


class Hiro6SearchData(AbcSearchData):
    __rest_client: Final[Hiro6SearchRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6SearchRest(client)

    def connected(
            self,
            vertex_id: str,
            edge_type: str,
            direction: Optional[str] = None,
            vertex_types: Optional[Union[str, Iterable[str]]] = None,
            fields: Optional[Union[str, Iterable[str]]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective params">
        e_params = {}

        if direction is not None:
            if isinstance(direction, str):
                e_params['direction'] = direction
            else:
                raise TypeError(type(direction))

        if vertex_types is not None:
            if isinstance(vertex_types, str):
                e_params['types'] = vertex_types
            elif isinstance(vertex_types, Iterable):
                e_params['types'] = ','.join(vertex_types)
            else:
                raise TypeError(type(vertex_types))

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

        response = self.__rest_client.connected(vertex_id, edge_type, e_params, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items

    # TODO file bug HTTP 200 internal json message error 404
    def external_id(
            self,
            external_id: str,
            fields: Optional[Union[str, Iterable[str]]] = None,
            order: Optional[Tuple[str, str]] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # https://pod1159.saasarago.com/_api/specs/api.yaml
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/get_query_type
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/post_query_type
        # <editor-fold name="effective request data">
        e_req_data = {
            'query': external_id
        }

        if fields is not None:
            if isinstance(fields, str):
                e_req_data['fields'] = fields
            elif isinstance(fields, Iterable):
                e_req_data['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

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

        response = self.__rest_client.external_id(e_req_data, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items

    def get_by_ids(
            self,
            *vertex_ids: str,
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,
            fields: Optional[Union[str, Iterable[str]]] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # https://pod1159.saasarago.com/_api/specs/api.yaml
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/get_query_type
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/post_query_type

        # <editor-fold name="effective request data">
        e_req_data = {
            'query': ','.join(vertex_ids)
        }

        if order is not None:
            if isinstance(order, Tuple):
                e_req_data['order'] = ' '.join(order)
            elif isinstance(order, Iterable):
                e_req_data['order'] = ','.join(' '.join(pair) for pair in order)
            else:
                raise TypeError(type(order))

        if fields is not None:
            if isinstance(fields, str):
                e_req_data['fields'] = fields
            elif isinstance(fields, Iterable):
                e_req_data['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

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

        response = self.__rest_client.get_by_ids(e_req_data, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items

    def index(
            self,
            query: str,
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            fields: Optional[Union[str, Iterable[str]]] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # https://pod1159.saasarago.com/_api/specs/api.yaml
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/get_query_type
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/post_query_type
        # <editor-fold name="effective request data">
        e_req_data = {
            'query': query
        }

        if order is not None:
            if isinstance(order, Tuple):
                e_req_data['order'] = ' '.join(order)
            elif isinstance(order, Iterable):
                e_req_data['order'] = ','.join(' '.join(pair) for pair in order)
            else:
                raise TypeError(type(order))

        if offset is not None:
            if isinstance(offset, int):
                if offset > 0:
                    e_req_data['offset'] = '%i' % offset
                else:
                    raise ValueError('Offset must be an integer greater zero')
            else:
                raise TypeError(type(offset))
        else:
            e_req_data['offset'] = 0

        if limit is not None:
            if isinstance(limit, int):
                if limit > 0:
                    e_req_data['limit'] = '%i' % limit
                else:
                    raise ValueError('Limit must be an integer greater zero')
            else:
                raise TypeError(type(limit))
        else:
            e_req_data['limit'] = -1

        if fields is not None:
            if isinstance(fields, str):
                e_req_data['fields'] = fields
            elif isinstance(fields, Iterable):
                e_req_data['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

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

        response = self.__rest_client.index(e_req_data, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items

    def graph(
            self,
            root: str,
            query: str,
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,  # virtual
            offset: Optional[int] = None,  # virtual
            limit: Optional[int] = None,  # virtual
            fields: Optional[Union[str, Iterable[str]]] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # https://pod1159.saasarago.com/_api/specs/api.yaml
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/get_query_type
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/post_query_type
        # <editor-fold name="effective request data">
        e_req_data = {
            'root': root,
            'query': query
        }
        if offset is not None and offset < 0:
            raise ValueError(offset)
        if limit is not None and (limit == 0 or limit < -1):
            raise ValueError(limit)

        if order:
            # https://tinkerpop.apache.org/docs/3.4.3/reference/#order-step
            e_req_data['order'] = ' '.join(order)

        if offset is not None and limit is None:
            # https://tinkerpop.apache.org/docs/current/reference/#skip-step
            # https://tinkerpop.apache.org/docs/current/reference/#_range_queries deprecated performance reflection
            stmt = f'.skip({offset})'
            e_req_data['query'] += stmt
            logging.debug(f'''appending {stmt!r} to query; resulting query {e_req_data['query']!r}''')
        elif offset is None and limit is not None:
            # https://tinkerpop.apache.org/docs/current/reference/#limit-step
            # https://tinkerpop.apache.org/docs/current/reference/#_range_queries deprecated performance reflection
            stmt = f'.limit({limit})'
            e_req_data['query'] += stmt
            logging.debug(f'''appending {stmt!r} to query; resulting query {e_req_data['query']!r}''')
        elif offset is not None and limit is not None:
            # https://tinkerpop.apache.org/docs/current/reference/#range-step
            # https://tinkerpop.apache.org/docs/current/reference/#_range_queries deprecated performance reflection
            if limit == -1:
                stmt = f'.skip({offset})'
            else:
                stmt = f'.range({offset},{offset + limit})'
            e_req_data['query'] += stmt
            logging.debug(f'''appending {stmt!r} to query; resulting query {e_req_data['query']!r}''')

        if fields:
            e_req_data['fields'] = ','.join(fields)

        if False and 'count' is not None:
            # https://tinkerpop.apache.org/docs/current/reference/#count-step
            e_req_data['query'] += '.count()'
            # TODO impl count hint
            raise RuntimeError('count()')

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

        response = self.__rest_client.graph(e_req_data, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items


class Hiro6SearchModel(AbcSearchModel):
    __base_client: Final['HiroRestBaseClient']
    __data_client: Final[Hiro6SearchData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__base_client = client
        self.__data_client = Hiro6SearchData(client)

    # TODO add vertex_id VERTEX_T
    def connected(
            self,
            vertex_id: VERTEX_ID_T,
            edge_type: EDGE_TYPE_T,
            direction: Optional[Literal['in', 'out', 'both']] = None,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            vertex_types: Optional[Iterable[VERTEX_TYPE_T]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        # order: Tuple[str, str] = None,  # not documented
        # count: bool = None,  # not documented
        # list_meta: bool = None,  # not documented
        # include_deleted: bool = None,  # found HIRO 7

        # Gremlin Graph Query: g.V({vertex_id}).outE({edge_type}).has('ogit/_in-type',within({vertex_types})).inV().range({offset}, {limit}})
        # Gremlin Graph Query: g.V({vertex_id}).inE({edge_type}).has('ogit/_out-type',within({vertex_types})).outV().range({offset}, {limit}})
        # Gremlin Graph Query: g.V({vertex_id}).{direction}({edge_type}).hasLabel(within({vertex_types})).range({offset}, {limit}})
        e_fields = [attribute_to_str(field) for field in fields] if fields else None
        e_vertex_types = (vertex_type_to_str(vertex_type) for vertex_type in vertex_types) if vertex_types else None

        #             if count is True:
        #                 return next(items)
        items = self.__data_client.connected(vertex_id, edge_type, direction, e_fields, e_vertex_types, offset, limit)
        vertices = to_vertices(items, self.__base_client)
        yield from vertices

    # TODO add external_id VERTEX_T
    def external_id(
            self,
            external_id: VERTEX_XID_T,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            order: Optional[Order] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        # list_meta: bool = None,
        # include_deleted: bool = None,

        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/post_query_type
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/get_query_type

        # Elasticsearch Query DSL Query String Query: +ogit\/_xid:"{external_id}"
        e_external_id = external_id_to_str(external_id)
        e_fields = [attribute_to_str(field) for field in fields] if fields else None
        e_order = (attribute_to_str(order.field), order.dir) if order else None

        items = self.__data_client.external_id(e_external_id, e_fields, e_order)
        vertices = to_vertices(items, self.__base_client)
        yield from vertices

    # TODO add vertex_ids VERTEX_T
    def get_by_ids(
            self,
            *vertex_ids: VERTEX_ID_T,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            order: Optional[Order] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        # Elasticsearch Query DSL Query String Query: +ogit\/_id:({vertex_ids})
        e_vertex_ids = tuple(vertex_id_to_str(vertex_id) for vertex_id in vertex_ids)
        e_fields = [attribute_to_str(field) for field in fields] if fields else None
        e_order = (attribute_to_str(order.field), order.dir) if order else None

        items = self.__data_client.get_by_ids(*e_vertex_ids, fields=e_fields, order=e_order)
        vertices = to_vertices(items, self.__base_client)
        yield from vertices

    def index(
            self,
            query: str,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            order: Optional[Order] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        #  Union[int, Generator[VERTEX_T, None, None]]:
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/post_query_type
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/get_query_type

        # TODO impl --show-list-meta
        # TODO maybe impl --list
        e_fields = [attribute_to_str(field) for field in fields] if fields else None
        e_order = (attribute_to_str(order.field), order.dir) if order else None

        items = self.__data_client.index(query, e_order, offset, limit, e_fields)
        # if count is True:
        #     return next(gen)
        vertices = to_vertices(items, self.__base_client)
        yield from vertices

    def graph(
            self,
            root: Union[VERTEX_ID_T, VERTEX_XID_T_co],
            query: str,
            fields: Optional[Union[ATTRIBUTE_T_co, Iterable[ATTRIBUTE_T_co]]] = None,
            order: Optional[Order] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            result_type: Type[T] = Vertex
    ) -> Generator[T, None, None]:
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/post_query_type
        # https://pod1159.saasarago.com/_api/index.html#!/%5BQuery%5D_Search/get_query_type

        if isinstance(root, ExternalVertexId):
            vertex_id = self.__base_client.root.resolve_xid(root)
            e_root = vertex_id_to_str(vertex_id)
        else:
            e_root = vertex_id_to_str(root)

        e_fields = [attribute_to_str(field) for field in fields] if fields else None
        e_order = (attribute_to_str(order.field), order.dir) if order else None

        items = self.__data_client.graph(e_root, query, e_fields, e_order, offset, limit)

        if isinstance(result_type, Vertex):
            vertices = to_vertices(items, self.__base_client)
            yield from vertices
        else:
            for item in items:
                instance = result_type(item, client=self.__base_client.root, draft=False)
                yield instance
