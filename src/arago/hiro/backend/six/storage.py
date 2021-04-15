from codecs import iterencode
from contextlib import contextmanager
from datetime import datetime
from functools import cached_property
from typing import Final, Generator, Dict, Any, Mapping, Optional, ContextManager, IO, TYPE_CHECKING, Iterable, Union, \
    Iterator
from urllib.parse import quote

from requests.models import Response

from arago.extension import json
from arago.hiro.abc.common import AbcData
from arago.hiro.abc.storage import AbcStorageBlobRest, AbcStorageBlobData, AbcStorageBlobModel, data_to_model, \
    model_to_data
from arago.hiro.abc.storage import AbcStorageLogRest, AbcStorageLogData, AbcStorageLogModel
from arago.hiro.abc.storage import AbcStorageRest, AbcStorageData, AbcStorageModel
from arago.hiro.abc.storage import AbcStorageTimeSeriesRest, AbcStorageTimeSeriesData, AbcStorageTimeSeriesModel
from arago.hiro.model.storage import TimeSeriesValue, BlobVertex, TimeSeriesVertex, \
    TIME_SERIES_ID_T, BLOB_ID_T, TimeSeriesId, BlobId
from arago.hiro.utils.datetime import datetime_to_timestamp_ms

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro6StorageBlobRest(AbcStorageBlobRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__base_client = client

    def get(
            self,
            blob_id: str,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        """
        https://requests.readthedocs.io/en/master/user/quickstart/#binary-response-content
        https://requests.readthedocs.io/en/master/user/quickstart/#raw-response-content
        https://requests.readthedocs.io/en/master/user/advanced/#streaming-requests
        https://requests.readthedocs.io/en/master/user/advanced/#blocking-or-non-blocking
        """
        uri = '/%s/content' % (
            quote(blob_id, safe=''),
        )
        e_headers = {'Accept': 'application/octet-stream'}
        if headers:
            e_headers.update(headers)
        return self.__base_client.request(
            'GET', uri, params=params, headers=e_headers, stream=True
        )

    # TODO test content_type support
    def set(
            self,
            blob_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        """
        https://requests.readthedocs.io/en/master/user/advanced/#body-content-workflow
        https://requests.readthedocs.io/en/master/user/advanced/#streaming-uploads
        https://requests.readthedocs.io/en/master/user/advanced/#chunk-encoded-requests
        https://requests.readthedocs.io/en/master/user/advanced/#post-multiple-multipart-encoded-files
        https://requests.readthedocs.io/en/master/user/advanced/#blocking-or-non-blocking
        """
        uri = '/%s/content' % (
            quote(blob_id, safe=''),
        )
        e_headers = {'Accept': 'application/json'}
        if headers:
            e_headers.update(headers)
        return self.__base_client.request(
            'POST', uri, headers=e_headers, data=content
        )


class Hiro6StorageBlobData(AbcStorageBlobData):
    __rest_client: Final[Hiro6StorageBlobRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6StorageBlobRest(client)

    # TODO test support of content_id
    # TODO test support of include_deleted
    @contextmanager
    def get(
            self,
            blob_id: str,
            content_id: Optional[str] = None,
            include_deleted: Optional[bool] = False
    ) -> ContextManager[Generator[bytes, None, None]]:
        params = {}
        if content_id is not None:
            params['contentId'] = content_id
        if include_deleted:
            params['includeDeleted'] = include_deleted
        with self.__rest_client.get(blob_id, params) as response:
            yield response.iter_content(chunk_size=None)

    def set(
            self,
            blob_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            content_type: Optional[str] = None
    ) -> None:
        if content_type is not None:
            headers = {'Content-Type': content_type}
        else:
            headers = None
        self.__rest_client.set(blob_id, content, headers)


class Hiro6StorageBlobModel(AbcStorageBlobModel):
    __data_client: Final[Hiro6StorageBlobData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro6StorageBlobData(client)

    def get(
            self,
            blob_id: Union[BlobVertex, BLOB_ID_T],
            content_id: Optional[str] = None,
            include_deleted: Optional[bool] = False
    ) -> ContextManager[Generator[bytes, None, None]]:
        e_blob_id: str
        if isinstance(blob_id, BlobVertex):
            e_blob_id = str(blob_id.id)
        elif isinstance(blob_id, BlobId):
            e_blob_id = str(blob_id)
        elif isinstance(blob_id, str):
            e_blob_id = blob_id
        else:
            raise TypeError(type(blob_id))
        return self.__data_client.get(e_blob_id, content_id, include_deleted)

    def set(
            self,
            blob_id: Union[BlobVertex, BLOB_ID_T],
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            content_type: Optional[str] = None
    ) -> None:
        e_blob_id: str
        if isinstance(blob_id, BlobVertex):
            e_blob_id = str(blob_id.id)
        elif isinstance(blob_id, BlobId):
            e_blob_id = str(blob_id)
        elif isinstance(blob_id, str):
            e_blob_id = blob_id
        else:
            raise TypeError(type(blob_id))
        self.__data_client.set(e_blob_id, content, content_type)


class Hiro6StorageLogRest(AbcStorageLogRest):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)


class Hiro6StorageLogData(AbcStorageLogData):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)


class Hiro6StorageLogModel(AbcStorageLogModel):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)


class Hiro6StorageTimeSeriesRest(AbcStorageTimeSeriesRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__base_client = client

    def add(
            self,
            ts_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/%s/values' % (
            quote(ts_id, safe=''),
        )
        # To stream and upload, simply provide a file-like object for your body
        return self.__base_client.request(
            'POST', uri, headers=headers, data=content
        )

    def get(
            self,
            ts_id: str,
            params: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/%s/values' % (
            quote(ts_id, safe=''),
        )
        return self.__base_client.request(
            'GET', uri, params=params, headers=headers, stream=True
        )


class Hiro6StorageTimeSeriesData(AbcStorageTimeSeriesData):
    __rest_client: Final[Hiro6StorageTimeSeriesRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6StorageTimeSeriesRest(client)

    def add(
            self,
            ts_id: str,
            values: Iterator[Mapping[str, Any]]
    ) -> None:
        json_generator = json.GeneratorAwareJSONEncoder().iterencode(values)
        payload_generator = iterencode(json_generator, 'utf8')
        headers = {'Content-Type': 'application/json'}
        self.__rest_client.add(ts_id, payload_generator, headers)

    def get(
            self,
            ts_id: str,
            start: Optional[int] = None,
            end: Optional[int] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """

        :param ts_id: time series vertex id
        :param start: unix timestamp in seconds
        :param end: unix timestamp in seconds
        """
        params = {
            'from': '%011i' % (0 if start is None else start),
        }
        if end is not None:
            params['to'] = '%011i' % end
        headers = {'Accept': 'application/json'}
        response = self.__rest_client.get(ts_id, params, headers)
        items = AbcData.items_generator(response)
        yield from items


class Hiro6StorageTimeSeriesModel(AbcStorageTimeSeriesModel):
    __data_client: Final[Hiro6StorageTimeSeriesData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro6StorageTimeSeriesData(client)

    def add(
            self,
            ts_id: Union[TimeSeriesVertex, TIME_SERIES_ID_T],
            values: Iterator[TimeSeriesValue]
    ) -> None:
        e_ts_id: str
        if isinstance(ts_id, TimeSeriesVertex):
            e_ts_id = ts_id.id
        elif isinstance(ts_id, TimeSeriesId):
            e_ts_id = str(ts_id)
        elif isinstance(ts_id, str):
            e_ts_id = ts_id
        else:
            raise TypeError(type(ts_id))
        transformer = model_to_data(values)
        self.__data_client.add(e_ts_id, transformer)

    def get(
            self,
            ts_id: Union[TimeSeriesVertex, TIME_SERIES_ID_T],
            start: Optional[datetime] = None,
            end: Optional[datetime] = None
    ) -> Generator[TimeSeriesValue, None, None]:
        e_ts_id: str
        if isinstance(ts_id, TimeSeriesVertex):
            e_ts_id = ts_id.id
        elif isinstance(ts_id, TimeSeriesId):
            e_ts_id = str(ts_id)
        elif isinstance(ts_id, str):
            e_ts_id = ts_id
        else:
            raise TypeError(type(ts_id))
        items = self.__data_client.get(
            e_ts_id,
            datetime_to_timestamp_ms(start),
            datetime_to_timestamp_ms(end)
        )
        transformer = data_to_model(items)
        yield from transformer


class Hiro6StorageRest(AbcStorageRest):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def blob(self) -> Hiro6StorageBlobRest:
        return Hiro6StorageBlobRest(self.__client)

    @cached_property
    def log(self) -> AbcStorageLogRest:
        raise NotImplementedError()

    @cached_property
    def ts(self) -> Hiro6StorageTimeSeriesRest:
        return Hiro6StorageTimeSeriesRest(self.__client)


class Hiro6StorageData(AbcStorageData):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def blob(self) -> Hiro6StorageBlobData:
        return Hiro6StorageBlobData(self.__client)

    @cached_property
    def log(self) -> AbcStorageLogData:
        raise NotImplementedError()

    @cached_property
    def ts(self) -> Hiro6StorageTimeSeriesData:
        return Hiro6StorageTimeSeriesData(self.__client)


class Hiro6StorageModel(AbcStorageModel):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def blob(self) -> Hiro6StorageBlobModel:
        return Hiro6StorageBlobModel(self.__client)

    @cached_property
    def log(self) -> AbcStorageLogModel:
        raise NotImplementedError()

    @cached_property
    def ts(self) -> Hiro6StorageTimeSeriesModel:
        return Hiro6StorageTimeSeriesModel(self.__client)
