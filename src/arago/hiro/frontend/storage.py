from datetime import datetime
from functools import cached_property
from typing import Optional, ContextManager, Generator, Mapping, Any, Dict, IO, Final, Iterator, Union, Iterable

from requests.models import Response

from arago.hiro.abc.storage import AbcStorageModel, AbcStorageBlobModel, AbcStorageTimeSeriesModel, \
    AbcStorageLogModel, AbcStorageRest, AbcStorageBlobRest, AbcStorageLogRest, AbcStorageTimeSeriesRest, AbcStorageData, \
    AbcStorageBlobData, AbcStorageLogData, AbcStorageTimeSeriesData
from arago.hiro.client.rest_base_client import HiroRestBaseClient
from arago.hiro.model.probe import Version
from arago.hiro.model.storage import BlobId, TimeSeriesId, TimeSeriesValue


# TODO fix requests to have headers and params for Rest
class StorageBlobRest(AbcStorageBlobRest):
    __client: Final[AbcStorageBlobRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.storage import Hiro6StorageBlobRest as ImplStorageBlobRest
        elif version == Version.HIRO_7:
            raise NotImplementedError()
            # from arago.hiro.backend.seven.storage import Hiro7StorageBlobRest as ImplStorageBlobRest
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplStorageBlobRest(client)

    def get(
            self,
            blob_id: str,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        return self.__client.get(blob_id, params, headers)

    def set(
            self,
            blob_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        return self.__client.set(blob_id, content, headers)


class StorageBlobData(AbcStorageBlobData):
    __client: Final[AbcStorageBlobData]

    # TODO error message 'Unreachable'
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.storage import Hiro6StorageBlobData as ImplStorageBlobData
        elif version == Version.HIRO_7:
            raise NotImplementedError()
            # from arago.hiro.backend.seven.storage import Hiro7StorageBlobData as ImplStorageBlobData
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplStorageBlobData(client)

    def get(
            self,
            blob_id: str,
            content_id: Optional[str] = None,
            include_deleted: Optional[bool] = False
    ) -> ContextManager[Generator[bytes, None, None]]:
        return self.__client.get(blob_id, content_id, include_deleted)

    def set(
            self,
            blob_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            content_type: Optional[str] = None
    ) -> None:
        return self.__client.set(blob_id, content, content_type)


class StorageBlobModel(AbcStorageBlobModel):
    __client: Final[AbcStorageBlobModel]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.storage import Hiro6StorageBlobModel as ImplStorageBlobModel
        elif version == Version.HIRO_7:
            raise NotImplementedError()
            # from arago.hiro.backend.seven.storage import Hiro7StorageBlobModel as ImplStorageBlobModel
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplStorageBlobModel(client)

    def get(
            self,
            blob_id: BlobId,
            content_id: Optional[str] = None,
            include_deleted: Optional[bool] = False
    ) -> ContextManager[Generator[bytes, None, None]]:
        return self.__client.get(blob_id, content_id, include_deleted)

    def set(
            self,
            blob_id: BlobId,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            content_type: Optional[str] = None
    ) -> None:
        return self.__client.set(blob_id, content, content_type)


class StorageLogRest(AbcStorageLogRest):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)


class StorageLogData(AbcStorageLogData):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)


class StorageLogModel(AbcStorageLogModel):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)


# TODO fix requests to have headers and params for Rest
class StorageTimeSeriesRest(AbcStorageTimeSeriesRest):
    __client: Final[AbcStorageTimeSeriesRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.storage import Hiro6StorageTimeSeriesRest as ImplStorageTimeSeriesRest
        elif version == Version.HIRO_7:
            raise NotImplementedError()
            # from arago.hiro.backend.seven.storage import Hiro6StorageTimeSeriesRest as ImplStorageTimeSeriesRest
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplStorageTimeSeriesRest(client)

    def add(
            self,
            ts_id: str,
            content: Union[bytes, bytearray, Iterable[bytes], IO[bytes]],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        return self.__client.add(ts_id, content, headers)

    def get(
            self,
            ts_id: str,
            params: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        return self.__client.get(ts_id, params, headers)


class StorageTimeSeriesData(AbcStorageTimeSeriesData):
    __client: Final[AbcStorageTimeSeriesData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.storage import Hiro6StorageTimeSeriesData as ImplStorageTimeSeriesData
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.storage import Hiro7StorageTimeSeriesData as ImplStorageTimeSeriesData
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplStorageTimeSeriesData(client)

    def add(
            self,
            ts_id: str,
            values: Iterator[Mapping[str, Any]]
    ) -> None:
        return self.__client.add(ts_id, values)

    def get(
            self,
            ts_id: str,
            start: Optional[int] = None,
            end: Optional[int] = None
    ) -> Generator[Dict[str, Any], None, None]:
        return self.__client.get(ts_id, start, end)


class StorageTimeSeriesModel(AbcStorageTimeSeriesModel):
    __client: Final[AbcStorageTimeSeriesModel]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.storage import Hiro6StorageTimeSeriesModel as ImplStorageTimeSeriesModel
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.storage import Hiro7StorageTimeSeriesModel as ImplStorageTimeSeriesModel
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplStorageTimeSeriesModel(client)

    def add(
            self,
            ts_id: TimeSeriesId,
            values: Iterator[TimeSeriesValue]
    ) -> None:
        return self.__client.add(ts_id, values)

    def get(
            self,
            ts_id: TimeSeriesId,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None
    ) -> Generator[TimeSeriesValue, None, None]:
        return self.__client.get(ts_id, start, end)


class StorageRest(AbcStorageRest):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def blob(self) -> StorageBlobRest:
        return StorageBlobRest(self.__client)

    @cached_property
    def log(self) -> StorageLogRest:
        return StorageLogRest(self.__client)

    @cached_property
    def ts(self) -> StorageTimeSeriesRest:
        return StorageTimeSeriesRest(self.__client)


class StorageData(AbcStorageData):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def blob(self) -> StorageBlobData:
        return StorageBlobData(self.__client)

    @cached_property
    def log(self) -> StorageLogData:
        return StorageLogData(self.__client)

    @cached_property
    def ts(self) -> StorageTimeSeriesData:
        return StorageTimeSeriesData(self.__client)


class StorageModel(AbcStorageModel):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    @cached_property
    def blob(self) -> StorageBlobModel:
        return StorageBlobModel(self.__client)

    @cached_property
    def log(self) -> StorageLogModel:
        return StorageLogModel(self.__client)

    @cached_property
    def ts(self) -> StorageTimeSeriesModel:
        return StorageTimeSeriesModel(self.__client)
