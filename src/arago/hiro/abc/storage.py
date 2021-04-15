from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Any, ContextManager, Dict, Generator, IO, Iterator, Mapping, Optional, Union, Iterable

from requests import Response

from arago.hiro.model.storage import TimeSeriesId, BlobId, TimeSeriesValue
from .common import AbcRest, AbcData, AbcModel
from ..utils.datetime import timestamp_ms_to_datetime, datetime_to_timestamp_ms

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


# noinspection PyUnusedLocal
class AbcStorageBlobRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def get(
            self,
            blob_id: str,
            params: Optional[Mapping[str, str]],
            headers: Optional[Mapping[str, str]]
    ) -> Response:
        ...

    @abstractmethod
    def set(
            self,
            blob_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            headers: Optional[Mapping[str, str]]
    ) -> Response:
        ...


# noinspection PyUnusedLocal
class AbcStorageBlobData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def get(
            self,
            blob_id: str,
            content_id: Optional[str],
            include_deleted: Optional[bool]
    ) -> ContextManager[Generator[bytes, None, None]]:
        """
        content_id: since HIRO 7 (param)
        include_deleted: since HIRO 7 (param)
        """
        ...

    @abstractmethod
    def set(
            self,
            blob_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            content_type: Optional[str]
    ) -> None:
        """
        content_type: since HIRO 7 (header)
        """
        ...


# noinspection PyUnusedLocal
class AbcStorageBlobModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def get(
            self,
            blob_id: BlobId,
            content_id: Optional[str],
            include_deleted: Optional[bool]
    ) -> ContextManager[Generator[bytes, None, None]]:
        ...

    @abstractmethod
    def set(
            self,
            blob_id: BlobId,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            content_type: Optional[str]
    ) -> None:
        ...


# noinspection PyUnusedLocal
class AbcStorageLogRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...


# noinspection PyUnusedLocal
class AbcStorageLogData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...


# noinspection PyUnusedLocal
class AbcStorageLogModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...


def model_to_data(item_iter: Iterator[TimeSeriesValue]) -> Generator[Dict[str, Any], None, None]:
    for item in item_iter:
        yield {
            'value': item.value,
            'timestamp': datetime_to_timestamp_ms(item.timestamp),
        }


def data_to_model(item_iter: Iterator[Mapping[str, Any]]) -> Generator[TimeSeriesValue, None, None]:
    for item in item_iter:
        yield TimeSeriesValue(
            value=item['value'],
            timestamp=timestamp_ms_to_datetime(item['timestamp'])
        )


# noinspection PyUnusedLocal
class AbcStorageTimeSeriesRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def add(
            self,
            ts_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            headers: Optional[Mapping[str, str]]
    ) -> Response:
        """
        https://docs.hiro.arago.co/hiro/5.4.5/developer/hiro-graph-api/rest-api.html#_id_values_get
        https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/rest-api.html#_id_values_get
        https://pod1159.saasarago.com/_api/index.html#!/[Storage]_Timeseries/get_id_values
        https://core.arago.co/help/specs/?url=definitions/graph.yaml#/[Query]_Timeseries/get__id__values
        """
        ...

    @abstractmethod
    def get(
            self,
            ts_id: str,
            params: Optional[Mapping[str, Any]],
            headers: Optional[Mapping[str, str]]
    ) -> Response:
        """
        https://docs.hiro.arago.co/hiro/5.4.5/developer/hiro-graph-api/rest-api.html#_id_values_post
        https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/rest-api.html#_id_values_post
        https://pod1159.saasarago.com/_api/index.html#!/%5BStorage%5D_Timeseries/post_id_values
        https://core.arago.co/help/specs/?url=definitions/graph.yaml#operations-%5BStorage%5D_Timeseries-get__id__values
        """
        ...


# noinspection PyUnusedLocal
class AbcStorageTimeSeriesData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def add(
            self,
            ts_id: str,
            values: Iterator[Mapping[str, Any]]
    ) -> None:
        ...

    @abstractmethod
    def get(
            self,
            ts_id: str,
            start: Optional[int],
            end: Optional[int]
    ) -> Generator[Dict[str, Any], None, None]:
        ...


# noinspection PyUnusedLocal
class AbcStorageTimeSeriesModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def add(
            self,
            ts_id: TimeSeriesId,
            values: Iterator[TimeSeriesValue]
    ) -> None:
        ...

    @abstractmethod
    def get(
            self,
            ts_id: TimeSeriesId,
            start: Optional[datetime],
            end: Optional[datetime]
    ) -> Generator[TimeSeriesValue, None, None]:
        ...


# noinspection PyUnusedLocal
class AbcStorageRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @property
    @abstractmethod
    def blob(self) -> AbcStorageBlobRest:
        ...

    @property
    @abstractmethod
    def log(self) -> AbcStorageLogRest:
        ...

    @property
    @abstractmethod
    def ts(self) -> AbcStorageTimeSeriesRest:
        ...


# noinspection PyUnusedLocal
class AbcStorageData(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @property
    @abstractmethod
    def blob(self) -> AbcStorageBlobData:
        ...

    @property
    @abstractmethod
    def log(self) -> AbcStorageLogData:
        ...

    @property
    @abstractmethod
    def ts(self) -> AbcStorageTimeSeriesData:
        ...


# noinspection PyUnusedLocal
class AbcStorageModel(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @property
    @abstractmethod
    def blob(self) -> AbcStorageBlobModel:
        ...

    @property
    @abstractmethod
    def log(self) -> AbcStorageLogModel:
        ...

    @property
    @abstractmethod
    def ts(self) -> AbcStorageTimeSeriesModel:
        ...
