from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Mapping, Union, overload, Literal, Optional, Iterable, Generator

from requests import Response

from arago.hiro.model.graph.attribute import ATTRIBUTE_T
from arago.hiro.model.graph.edge import EdgeId, Edge
from arago.hiro.model.graph.history import HistoryFormat, HistoryDiff, HistoryEntry
from arago.hiro.model.graph.vertex import VertexId, Vertex, VERTEX_T, VERTEX_T_co, VERTEX_TYPE_T, VERTEX_XID_T_co, \
    VERTEX_ID_T, VERTEX_XID_T
from arago.hiro.model.storage import BLOB_VERTEX_T_co, TIME_SERIES_VERTEX_T_co
from arago.ogit import OgitEntity
from arago.ogit import OgitVerb
from .common import AbcRest, AbcData, AbcModel

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


# noinspection PyUnusedLocal
class AbcGraphEdgeRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def create(self, edge_type: str, req_data: Mapping[str, Any]) -> Response:
        ...

    @abstractmethod
    def delete(self, edge_id: str) -> Response:
        ...


# noinspection PyUnusedLocal
class AbcGraphEdgeData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    # https://pod1159.saasarago.com/_api/index.html#!/%5BGraph%5D_Verb/post_connect_type

    # create         add connection

    # usage: hiro [<general options>] edge create  [<specific options>]
    #             <from/out-vertex> <edge-type> <to/in-vertex>
    @abstractmethod
    def create(self, out_vertex_id: str, edge_type: str, in_vertex_id: str) -> Dict[str, Any]:
        ...

    # https://pod1159.saasarago.com/_api/index.html#!/%5BGraph%5D_Verb/delete_id

    # delete         remove connection

    # usage: hiro [<general options>] edge delete  [<specific options>]
    #             <from/out-vertex> <edge-type> <to/in-vertex>
    @abstractmethod
    def delete(self, edge_id: str) -> Dict[str, Any]:
        ...


# noinspection PyUnusedLocal
class AbcGraphEdgeModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def create(
            self,
            out_vertex_id: Union[Vertex, VertexId, str],
            edge_type: Union[OgitVerb, str],
            in_vertex_id: Union[Vertex, VertexId, str]
    ) -> Edge:
        ...

    @abstractmethod
    def delete(
            self,
            edge_id: Union[Edge, EdgeId, str]
    ) -> Edge:
        ...


# noinspection PyUnusedLocal
class AbcGraphVertexRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def create(
            self,
            vertex_type: str,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        ...

    @abstractmethod
    def get(
            self,
            vertex_id: str,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        ...

    @abstractmethod
    def update(
            self,
            vertex_id: str,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        ...

    @abstractmethod
    def delete(
            self,
            vertex_id: str,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        ...

    @abstractmethod
    def history(
            self,
            vertex_id: str,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        ...


# noinspection PyUnusedLocal
class AbcGraphVertexData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    # https://pod1159.saasarago.com/_api/index.html#!/%5BGraph%5D_Entity/post_new_type

    # create         create new vertices

    # usage: hiro [<general options>] vertex create  [<specific options>] <files
    #             containing vertex definitions (JSON)>
    # Options
    #  -t,--type <vertexType>   vertex type to create (only used for files not
    #                           containing ogit/_type)
    @abstractmethod
    def create(
            self,
            vertex_type: str,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        ...

    # https://pod1159.saasarago.com/_api/index.html#!/%5BGraph%5D_Entity/get_id
    # TODO impl --show-list-meta

    # usage: hiro [<general options>] vertex get  [<specific options>] <vertices
    #             to retrieve>
    # Options
    #     --show-list-meta          Expand meta data for attributes containing a
    #                               list value. This will suppress the behavior
    #                               that lists with only one element are shown
    #                               as scalar value. (default: do not expand
    #                               meta data)
    #     --use-xids                Any given IDs are taken as external IDs
    @abstractmethod
    def get(
            self,
            vertex_id: str,
            fields: Optional[Iterable[str]] = None,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        ...

    # https://pod1159.saasarago.com/_api/index.html#!/%5BGraph%5D_Entity/post_id

    # update         update one or more vertices from JSON input
    # usage: hiro vertex update [<options>]
    #             [<update JSON files>]>
    # Options
    #  -f,--file <fileName>   file that contains update JSON (requires -i/--id)
    #  -i,--id <vertexId>     vertex ID to update (requires -f/--file)

    # put            update existing vertex/creates missing. requires ogit/_xid in data
    # usage: hiro vertex put [<options>] <files
    #             containing vertex definitions (JSON) with ogit/_xid>
    # Options
    #  -t,--type <vertexType>   vertex type to create (only used for files not
    #                           containing ogit/_type)
    @abstractmethod
    def update(
            self,
            vertex_id: str,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        ...

    # https://pod1159.saasarago.com/_api/index.html#!/%5BGraph%5D_Entity/delete_id

    # delete         delete specific vertices

    # usage: hiro [<general options>] vertex delete [<specific options>]
    #             <vertices to delete>
    @abstractmethod
    def delete(
            self,
            vertex_id: str,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        ...

    # usage: hiro [<general options>] vertex history  [<specific options>]
    #             <vertex IDs to retrieve history for>
    # Options
    #     --use-xids                specified ID(s) is(are) taken as external ID(s)
    #     --detail-level <arg>      "element": (full) vertex content for each
    #                               history version. "full": vertex content plus
    #                               history meta data. "diff": show only changes
    #                               from previous version. Default: element.
    #     --show-list-meta          Expand meta data for attributes containing a
    #                               list value. This will suppress the behavior
    #                               that lists with only one element are shown
    #                               as scalar value. (default: do not expand
    #                               meta data)
    #     --version <arg>           retrieve a specific incarnation (based on
    #                               ogit/_v attribute) of the vertex. This
    #                               option will disable most of the other
    #                               restricting options.
    #     --from <from-ts>          only history entries with timestamps greater
    #                               or equal the specified one will be returned.
    #                               Value must be specified in msecs after
    #                               epoch.
    #     --to <to-ts>              only history entries with timestamps smaller
    #                               or equal the specified one will be returned.
    #                               Value must be specified in msecs after
    #                               epoch.
    #     --offset <arg>            skip first <offset> results of history
    #     --limit <arg>             retrieve at most the specified number of
    #                               history entries
    @abstractmethod
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
        ...

    # set-attribute  (bulk) update of a single vertex attribute
    # usage: hiro [<general options>] vertex set-attribute  [<specific options>]
    #             <vertices to update>
    # Options
    #  -a,--attribute <attrName>   attribute name to set
    #  -h,--help                   show usage
    #     --threads <arg>          number of parallel executions
    #  -v,--value <value>          value to set attribute <attrName> to

    # search         search for vertices
    # put-edges      create edges from input file using ogit/_xid
    # del-edges      create edges from input file using ogit/_xid


# noinspection PyUnusedLocal
class AbcGraphVertexModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @overload
    @abstractmethod
    def create(
            self,
            vertex: VERTEX_T
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def create(
            self,
            vertex_type: VERTEX_TYPE_T,
            vertex: Optional[VERTEX_T] = None
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def create(
            self,
            vertex_type: Union[Literal['ogit/Attachment'], Literal[OgitEntity.OGIT_ATTACHMENT]],
            vertex: Optional[VERTEX_T] = None
    ) -> BLOB_VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def create(
            self,
            vertex_type: Union[Literal['ogit/Timeseries'], Literal[OgitEntity.OGIT_TIME_SERIES]],
            vertex: Optional[VERTEX_T] = None
    ) -> TIME_SERIES_VERTEX_T_co:
        ...

    @abstractmethod
    def create(self, *args, **kwargs) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def get(
            self,
            vertex: VERTEX_T,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def get(
            self,
            vertex_id: VERTEX_ID_T,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def get(
            self,
            vertex_xid: VERTEX_XID_T,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None
    ) -> VERTEX_T_co:
        ...

    @abstractmethod
    def get(self, *args, **kwargs) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def update(
            self,
            vertex: VERTEX_T
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def update(
            self,
            vertex_id: VERTEX_ID_T,
            vertex: VERTEX_T
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def update(
            self,
            vertex_xid: VERTEX_XID_T,
            vertex: VERTEX_T
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def update(
            self,
            vertex: VERTEX_T,
            source_vertex: VERTEX_T
    ) -> VERTEX_T_co:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def delete(
            self,
            vertex: VERTEX_T
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def delete(
            self,
            vertex_id: VERTEX_ID_T
    ) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def delete(
            self,
            vertex_xid: VERTEX_XID_T
    ) -> VERTEX_T_co:
        ...

    @abstractmethod
    def delete(self, *args, **kwargs) -> VERTEX_T_co:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex: VERTEX_T,
            res_format: Literal[HistoryFormat.ELEMENT],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex_id: VERTEX_ID_T,
            res_format: Literal[HistoryFormat.ELEMENT],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex_id: VERTEX_XID_T_co,
            res_format: Literal[HistoryFormat.ELEMENT],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex: VERTEX_T,
            res_format: Literal[HistoryFormat.DIFF],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[HistoryDiff, None, None]:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex_id: VERTEX_ID_T,
            res_format: Literal[HistoryFormat.DIFF],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[HistoryDiff, None, None]:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex_id: VERTEX_XID_T_co,
            res_format: Literal[HistoryFormat.DIFF],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[HistoryDiff, None, None]:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex: VERTEX_T,
            res_format: Literal[HistoryFormat.FULL],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[HistoryEntry, None, None]:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex_id: VERTEX_ID_T,
            res_format: Literal[HistoryFormat.FULL],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[HistoryEntry, None, None]:
        ...

    @overload
    @abstractmethod
    def history(
            self,
            vertex_id: VERTEX_XID_T_co,
            res_format: Literal[HistoryFormat.FULL],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            version: Optional[int] = None
    ) -> Generator[HistoryEntry, None, None]:
        ...

    @abstractmethod
    def history(self, *args, **kwargs) -> Generator[Union[HistoryEntry, HistoryDiff, Vertex], None, None]:
        ...


# noinspection PyUnusedLocal
class AbcGraphRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @property
    @abstractmethod
    def edge(self) -> AbcGraphEdgeRest:
        ...

    @property
    @abstractmethod
    def vertex(self) -> AbcGraphVertexRest:
        ...


# noinspection PyUnusedLocal
class AbcGraphData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @property
    @abstractmethod
    def edge(self) -> AbcGraphEdgeData:
        ...

    @property
    @abstractmethod
    def vertex(self) -> AbcGraphVertexData:
        ...


# noinspection PyUnusedLocal
class AbcGraphModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @property
    @abstractmethod
    def edge(self) -> AbcGraphEdgeModel:
        ...

    @property
    @abstractmethod
    def vertex(self) -> AbcGraphVertexModel:
        ...
