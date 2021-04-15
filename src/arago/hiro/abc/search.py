from abc import abstractmethod
from typing import TYPE_CHECKING, Generator, Union, Dict, Any, Mapping, Optional, Type, TypeVar, Iterable, Tuple, \
    Literal

from requests import Response

from arago.hiro.model.graph.edge import Edge, EDGE_TYPE_T
from arago.hiro.model.graph.vertex import Vertex, VERTEX_ID_T, VERTEX_TYPE_T, VERTEX_T_co, VERTEX_XID_T, \
    VERTEX_XID_T_co
from arago.hiro.model.search import Order
from .common import AbcRest, AbcData, AbcModel
from ..model.graph.attribute import ATTRIBUTE_T

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


# noinspection PyUnusedLocal
class AbcSearchRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def connected(
            self,
            vertex_id: str,
            edge_type: str,
            params: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        ...

    @abstractmethod
    def external_id(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        ...

    @abstractmethod
    def get_by_ids(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        ...

    @abstractmethod
    def index(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        ...

    @abstractmethod
    def graph(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        ...


# noinspection PyUnusedLocal
class AbcSearchData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def external_id(
            self,
            external_id: str,
            fields: Optional[Iterable[str]] = None,
            order: Optional[Tuple[str, str]] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        ...

    @abstractmethod
    def get_by_ids(
            self,
            *vertex_ids: str,
            fields: Optional[Iterable[str]] = None,
            order: Optional[Tuple[str, str]] = None,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...


T = TypeVar('T', bool, int, str, Vertex, Edge)


# noinspection PyUnusedLocal
class AbcSearchModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def external_id(
            self,
            external_id: VERTEX_XID_T,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None,
            order: Optional[Order] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        ...

    @abstractmethod
    def get_by_ids(
            self,
            *vertex_ids: VERTEX_ID_T,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None,
            order: Optional[Order] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        ...

    @abstractmethod
    def index(
            self,
            query: str,
            fields: Optional[Iterable[ATTRIBUTE_T]] = None,
            order: Optional[Order] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Generator[VERTEX_T_co, None, None]:
        ...

    @abstractmethod
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
        ...
