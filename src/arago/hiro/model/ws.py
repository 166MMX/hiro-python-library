import asyncio
from abc import ABC
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Final, Mapping, Any, Dict, Optional, Union, Literal

from cuid import cuid

from arago.hiro.model.graph.vertex import Vertex


class EventsOffset(Enum):
    value: str
    SMALLEST = 'smallest'
    LARGEST = 'largest'


class FilterType(Enum):
    value: str
    J_FILTER = 'jfilter'


class Filter(ABC):
    id: Final[str]
    type: Final[FilterType]
    expression: str

    def __init__(self, filter_type: FilterType, expression: str) -> None:
        super().__init__()
        self.id = cuid()
        self.type = filter_type
        self.expression = expression


class JFilter(Filter):
    def __init__(self, expression: str) -> None:
        super().__init__(FilterType.J_FILTER, expression)


class State(Enum):
    value: int
    MISSING = -1
    NEW = 1
    PROCESSING = 2
    WAITING = 3
    STOPPED = 4
    RESOLVED = 5
    TERMINATED = 6
    RESOLVED_EXTERNALLY = 7


@dataclass(frozen=True)
class Event:
    id: str
    nanotime: int
    timestamp: int
    body: Vertex
    type: str
    metadata: dict


class GraphEvent:
    identity: str
    action: str
    element: Mapping[str, Any]
    # Events contain the originator of the event, the action taken, and the contents.
    #
    # Example: An Event
    # {
    #   "identity":"id of the identity",
    #   "action":"type, e.g. CREATE",
    #   "element":{
    #     /* properties like ogit/_id*/
    #   }
    # }


# noinspection SpellCheckingInspection
class RequestType(Enum):
    value: str
    VERTEX_CREATE = 'create'
    VERTEX_GET = 'get'
    VERTEX_UPDATE = 'update'
    VERTEX_REPLACE = 'replace'
    VERTEX_HISTORY = 'history'
    EDGE_CREATE = 'connect'
    DELETE = 'delete'
    QUERY = 'query'
    TS_VALUES_ADD = 'writets'
    TS_VALUES_GET = 'streamts'
    BLOB_CONTENT_GET = 'getcontent'
    IDENTITY = 'me'
    TOKEN = 'token'


# <editor-fold desc="res message">
@dataclass(frozen=True)
class ResponseEnvelope:
    id: str


@dataclass(frozen=True)
class ErrorEnvelope(ResponseEnvelope):
    error: Dict[str, Any]
    more: bool = field(default=False)  # more == !last


@dataclass(frozen=True)
class SuccessEnvelope(ResponseEnvelope):
    more: bool  # more = !last
    body: Any
    multi: bool = field(default=False)  # multi == !single response // chunked


# </editor-fold>

# <editor-fold desc="req message">
@dataclass
class RequestMessage:
    id: Final[str] = field(default_factory=cuid, init=False)
    type: RequestType = field(init=False)


@dataclass
class RequestHttpLikeMessage(RequestMessage):
    headers: Dict[str, str] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UpdateTokenRequest(RequestHttpLikeMessage):
    _TOKEN: Optional[str] = field(default=None)
    type: Final[RequestType] = field(default=RequestType.TOKEN)
    # {
    #   "id": "1",
    #   "type": "token",
    #   "_TOKEN": ""
    # }


@dataclass
class VertexCreateRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.VERTEX_CREATE)
    # {
    #   "id":   "request id",
    #   "type": "create",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_type": "type of the node"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }


@dataclass
class VertexGetRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.VERTEX_GET, init=False)
    # {
    #   "id":   "request id",
    #   "type": "get",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_id": "id of the node"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }


@dataclass
class VertexUpdateRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.VERTEX_UPDATE)
    # {
    #   "id":   "request id",
    #   "type": "update",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_id": "id of the node"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }


@dataclass
class VertexReplaceRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.VERTEX_REPLACE)
    # {
    #   "id":   "request id",
    #   "type": "replace",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_id": "id of the node"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }


@dataclass
class EdgeCreateRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.EDGE_CREATE)
    # {
    #   "id":   "request id",
    #   "type": "connect",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_type": "type of the verb"
    #   },
    #   "body":
    #   {
    #     "out": "id of the outgoing node",
    #     "in": "id of the ingoing node"
    #   }
    # }


@dataclass
class QueryRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.QUERY)
    # {
    #   "id":   "request id",
    #   "type": "query",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "type": "type of the query, e.g. vertices"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }

    # {,…}
    #   body: {,…}
    #     limit: 10
    #     offset: 0
    #     order: "/teaching_is_handedover desc, ogit/_modified-on desc"
    #     query: "(+ogit\/_type:"ogit/Knowledge/AcquisitionSession") AND (((-\/teaching_ownerId:*) \/teaching_is_handedover:"true" \/teaching_ownerId:ck693o0rbotelcm02mec84ryz) -ogit\/Knowledge\/archived:"true")"
    #   headers: {type: "vertices"}
    #     type: "vertices"
    #   id: "0"
    #   type: "query"
    #   _TOKEN: ""


@dataclass
class TimeSeriesAddValuesRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.TS_VALUES_ADD)
    # {
    #   "id":   "request id",
    #   "type": "writets",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_id": "id of the node"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }


@dataclass
class TimeSeriesGetValuesRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.TS_VALUES_GET)
    # {
    #   "id":   "request id",
    #   "type": "streamts",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_id": "id of the node"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }


@dataclass
class VertexHistoryRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.VERTEX_HISTORY)
    # {
    #   "id":   "request id",
    #   "type": "history",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_id": "id of the node"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }


# </editor-fold>


class QueueMarker(Enum):
    END = auto()


# <editor-fold desc="req message">

@dataclass
class VertexReplaceRequest(RequestHttpLikeMessage):
    type: Final[RequestType] = field(default=RequestType.VERTEX_REPLACE)
    # {
    #   "id":   "request id",
    #   "type": "replace",
    #   /* other optional properties */
    #   "headers":
    #   {
    #     "ogit/_id": "id of the node"
    #   },
    #   "body":
    #   {
    #     // all parameters for the corresponding REST request are available here
    #   }
    # }


# </editor-fold>

@dataclass
class WebSocketRequest:
    req_message: RequestMessage
    future: asyncio.Future
    res_queue: asyncio.Queue[Union[Exception, Literal[QueueMarker.END], Any]]
