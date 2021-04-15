from datetime import datetime
from typing import NamedTuple, Optional, Union, TypeVar

from arago.hiro.model.graph.vertex import VertexId, Vertex


class BlobId(VertexId):
    pass


BLOB_ID_T_co = TypeVar('BLOB_ID_T_co', bound=BlobId, covariant=True)
BLOB_ID_T = Union[
    BLOB_ID_T_co,
    str
]


class TimeSeriesId(VertexId):
    pass


TIME_SERIES_ID_T_co = TypeVar('TIME_SERIES_ID_T_co', bound=TimeSeriesId, covariant=True)
TIME_SERIES_ID_T = Union[
    TIME_SERIES_ID_T_co,
    str
]


class LogId(VertexId):
    pass


class TimeSeriesValue(NamedTuple):
    value: Optional[Union[str, int, float, bool]]
    timestamp: datetime


class TimeSeriesVertex(Vertex):
    id: Optional[TimeSeriesId]

    def add_values(self):
        raise NotImplementedError()

    def get_values(self):
        raise NotImplementedError()


TIME_SERIES_VERTEX_T_co = TypeVar('TIME_SERIES_VERTEX_T_co', bound=TimeSeriesVertex, covariant=True)


class BlobContent(NamedTuple):
    pass


class BlobVertex(Vertex):
    id: Optional[BlobId]

    def set_content(self):
        raise NotImplementedError()

    def get_content(self):
        raise NotImplementedError()


BLOB_VERTEX_T_co = TypeVar('BLOB_VERTEX_T_co', bound=BlobVertex, covariant=True)
