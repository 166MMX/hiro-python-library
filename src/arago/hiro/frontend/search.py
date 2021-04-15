from typing import TYPE_CHECKING, Mapping, Any, Generator, Dict, Optional, Union, Type, Final, Iterable, Tuple, \
    Literal

from requests.models import Response

from arago.hiro.abc.search import AbcSearchRest, AbcSearchData, AbcSearchModel, T
from arago.hiro.model.graph.attribute import ATTRIBUTE_T
from arago.hiro.model.graph.edge import EDGE_TYPE_T
from arago.hiro.model.graph.vertex import Vertex, VERTEX_ID_T, VERTEX_XID_T_co, VERTEX_T_co, VERTEX_XID_T, \
    VERTEX_TYPE_T
from arago.hiro.model.probe import Version
from arago.hiro.model.search import Order

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class SearchRest(AbcSearchRest):
    __client: Final['AbcSearchRest']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.search import Hiro6SearchRest as ImplSearchRest
        elif version == Version.HIRO_7:
            raise NotImplementedError()
            # from arago.hiro.backend.seven.graph import Hiro7SearchRest as ImplSearchRest
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplSearchRest(client)

    def connected(
            self,
            vertex_id: str,
            edge_type: str,
            params: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        return self.__client.connected(vertex_id, edge_type, params, headers, stream)

    def external_id(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        return self.__client.external_id(req_data, headers, stream)

    def get_by_ids(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        return self.__client.get_by_ids(req_data, headers, stream)

    def index(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        return self.__client.index(req_data, headers, stream)

    def graph(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        return self.__client.graph(req_data, headers, stream)


class SearchData(AbcSearchData):
    __client: Final['AbcSearchData']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.search import Hiro6SearchData as ImplSearchData
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.search import Hiro7SearchData as ImplSearchData
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplSearchData(client)

    def connected(
            self,
            vertex_id: str,
            edge_type: str,
            direction: Optional[str] = None,
            fields: Optional[Iterable[str]] = None,
            vertex_types: Optional[Iterable[str]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        return self.__client.connected(
            vertex_id, edge_type, direction, fields, vertex_types, offset, limit, params, headers
        )

    def external_id(
            self,
            external_id: str,
            fields: Optional[Iterable[str]] = None,
            order: Optional[Tuple[str, str]] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        return self.__client.external_id(external_id, fields, order, req_data, headers)

    def get_by_ids(
            self,
            *vertex_ids: str,
            fields: Optional[Iterable[str]] = None,
            order: Optional[Tuple[str, str]] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        return self.__client.get_by_ids(*vertex_ids, fields=fields, order=order, req_data=req_data, headers=headers)

    def index(
            self,
            query: str,
            fields: Optional[Iterable[str]] = None,
            order: Optional[Tuple[str, str]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        return self.__client.index(query, fields, order, offset, limit, req_data, headers)

    def graph(
            self,
            root: str,
            query: str,
            fields: Optional[Iterable[str]] = None,
            order: Optional[Tuple[str, str]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        return self.__client.graph(root, query, fields, order, offset, limit, req_data, headers)


class SearchModel(AbcSearchModel):
    __client: Final['AbcSearchModel']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.search import Hiro6SearchModel as ImplSearchModel
        elif version == Version.HIRO_7:
            raise NotImplementedError()
            # from arago.hiro.backend.seven.search import Hiro7SearchModel as ImplSearchModel
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplSearchModel(client)

    def connected(
            self,
            vertex_id: VERTEX_ID_T,
            edge_type: EDGE_TYPE_T,
            direction: Optional[Literal['in', 'out', 'both']] = None,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None,
            vertex_types: Optional[Iterable[VERTEX_TYPE_T]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        return self.__client.connected(vertex_id, edge_type, direction, fields, vertex_types, offset, limit)

    def external_id(
            self,
            external_id: VERTEX_XID_T,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None,
            order: Optional[Order] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        return self.__client.external_id(external_id, fields, order)

    def get_by_ids(
            self,
            *vertex_ids: VERTEX_ID_T,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None,
            order: Optional[Order] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        return self.__client.get_by_ids(*vertex_ids, fields=fields, order=order)

    def index(
            self,
            query: str,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None,
            order: Optional[Order] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        # https://www.elastic.co/guide/en/elasticsearch/reference/1.7/query-dsl-query-string-query.html#query-string-syntax

        # search         search for vertices

        # usage: hiro [<general options>] vertex search  [<specific options>]
        #             [<attr:value> [<attr:value> ...]]
        # Options
        #  -c,--count                 retrieve only count of matching nodes
        #     --fields <arg>          comma separated list of field names to show in
        #                             result
        #  -l,--list                  retrieve only ids (or some specific fields) of
        #                             matching nodes
        #     --limit <arg>           limit size of result set
        #     --offset <arg>          skip first <offset> results
        #  -Q,--query <arg>           enter (ready to use) vertex query. To be used
        #                             if query is more complex than ANDed
        #                             <attr:value> pairs
        #     --show-list-meta        If a vertex attribute is a list value show it
        #                             as list even if only one element is contained
        #                             (default: show one-element list as scalar)

        return self.__client.index(query, fields, order, offset, limit)

    def graph(
            self,
            root: Union[VERTEX_ID_T, VERTEX_XID_T_co],
            query: str,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None,
            order: Optional[Order] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            result_type: Type[T] = Vertex
    ) -> Generator[T, None, None]:
        #             count: Optional[bool] = None,
        #             list_meta: Optional[bool] = None,
        #             include_deleted: Optional[bool] = None

        # https://github.com/spmallette/GremlinDocs

        # graph          more graph operations
        # query          run gremlin query

        # usage: hiro [<general options>] graph query  [<specific options>]
        # Options
        #  -Q,--query <arg>           gremlin query
        #  -R,--root <arg>            start node (root) for gremlin
        #     --show-list-meta        If a vertex attribute is a list value show it
        #                             as list even if only one element is contained
        #                             (default: show one-element list as scalar)

        return self.__client.graph(root, query, fields, order, offset, limit, result_type)
