import asyncio
import json
import logging
from asyncio.events import AbstractEventLoop
from asyncio.tasks import Task
from dataclasses import asdict
from types import coroutine
from typing import Optional, Dict, Any, Union, Generator, TypeVar, Iterator, AsyncIterable, \
    AsyncGenerator, Iterable

import websockets
from urllib3.util import parse_url
from websockets import Subprotocol, WebSocketException

from arago.hiro.client.client import HiroClient as HiroRestClient
from arago.hiro.model.auth import ConstantAccessToken, PasswordAccessToken
from arago.hiro.model.graph.attribute import SystemAttribute
# https://websockets.readthedocs.io/en/stable/intro.html
from arago.hiro.model.ws import ResponseEnvelope, ErrorEnvelope, SuccessEnvelope, WebSocketRequest, QueueMarker, \
    RequestMessage, QueryRequest, VertexGetRequest

_T_co = TypeVar('_T_co', covariant=True)

logger = logging.getLogger(__name__)
logger.propagate = True


def iter_over_async(iterable: AsyncIterable[_T_co], loop: AbstractEventLoop) -> Generator[_T_co, None, None]:
    # https://stackoverflow.com/questions/63587660/
    iterator = iterable.__aiter__()
    while True:
        try:
            yield loop.run_until_complete(iterator.__anext__())
        except StopAsyncIteration:
            break


RESPONSE_ENVELOPE_T_co = TypeVar('RESPONSE_ENVELOPE_T_co', bound=ResponseEnvelope, covariant=True)


@coroutine
def ws_message_to_envelope(messages: Iterator[str]) -> Generator[RESPONSE_ENVELOPE_T_co, None, None]:
    for message in messages:
        data = json.loads(message)
        envelope: Union[SuccessEnvelope, ErrorEnvelope]
        if ('error', 'id') in data:
            envelope = ErrorEnvelope(**data)
        else:
            envelope = SuccessEnvelope(**data)
        yield envelope


class HiroWebSocketClient:
    rx_task: Task
    rest_client: HiroRestClient
    pending: Dict[str, WebSocketRequest] = dict()
    socket: Optional[websockets.WebSocketClientProtocol] = None
    loop: AbstractEventLoop = asyncio.get_event_loop()

    def __init__(self, rest_client: HiroRestClient) -> None:
        super().__init__()
        self.rest_client = rest_client

    def connect(self) -> None:
        token = self.rest_client.authenticator.get_new_token()
        if isinstance(token, PasswordAccessToken):
            pass  # renew token unsupported
        elif not isinstance(token, ConstantAccessToken):
            raise TypeError(token)
        netloc = parse_url(self.rest_client.endpoint).netloc
        endpoint = self.rest_client.model.meta.version()['graph-ws'].endpoint
        future = websockets.connect(
            uri='wss://%s%s' % (netloc, endpoint),
            subprotocols=(
                Subprotocol('graph-%s' % '2.0.0'),
                Subprotocol('token-%s' % token.value)
            ))
        self.socket = self.loop.run_until_complete(future)
        self.rx_task = self.loop.create_task(self.handle_rx_message())

    def send(self, message: Union[str, bytes, Iterable[Union[str, bytes]], AsyncIterable[Union[str, bytes]]]):
        if isinstance(message, (str, bytes)):
            logger.debug(f'TX < {message!r}')
        self.socket.send(message)

    async def handle_rx_message(self):
        message: str
        while True:
            try:
                message = await self.socket.recv()
                logger.debug(f'RX > {message!r}')
            except WebSocketException as e:
                for req in self.pending.values():
                    await req.res_queue.put(e)
                break
            data = json.loads(message)
            envelope: Union[SuccessEnvelope, ErrorEnvelope]
            if 'id' in data:
                if 'error' in data:
                    envelope = ErrorEnvelope(**data)
                else:
                    envelope = SuccessEnvelope(**data)
            elif 'error' in data:
                raise RuntimeError('%s: %s' % (data['error']['code'], data['error']['message']))
            else:
                raise RuntimeError('Unreachable')

            if envelope.id not in self.pending:
                raise RuntimeError(f'No pending request found for id {envelope.id!r}')

            request = self.pending[envelope.id]

            if isinstance(envelope, ErrorEnvelope):
                del self.pending[envelope.id]
                await request.res_queue.put(RuntimeError(envelope.error))
            elif not envelope.multi:  # single response
                print(f'revived complete response {envelope.id!r} {envelope.body!r}')
                if envelope.more:  # not last response
                    raise RuntimeError(
                        f'Received invalid response with {envelope.id!r}.'
                        f' A single response can not have additional pending responses.'
                    )
                else:  # last response
                    await request.res_queue.put(envelope.body)
                    del self.pending[envelope.id]
                    await request.res_queue.put(QueueMarker.END)
                    request.future.set_result(None)
            else:  # chunked response
                # print(f'received chunked response {envelope.id!r} {envelope.body!r}')
                if envelope.body is not None:
                    await request.res_queue.put(envelope.body)
                if not envelope.more:  # last response
                    del self.pending[envelope.id]
                    await request.res_queue.put(QueueMarker.END)
                    request.future.set_result(None)

    async def submit_request(
            self, message: RequestMessage
    ) -> AsyncGenerator[Dict[str, Any], None]:
        request = WebSocketRequest(message, self.loop.create_future(), asyncio.Queue())
        self.pending[message.id] = request
        data = asdict(message)
        data['type'] = message.type.value
        json_str = json.dumps(data)
        # print(f'submitting request {message.id!r} {json_str!r}')
        await self.socket.send(json_str)
        while True:
            message = await request.res_queue.get()
            if isinstance(message, Exception):
                raise message
            if message is QueueMarker.END:
                break
            yield message

    def close(self):
        self.socket.close()

    def search_index(self, query: str) -> Generator[Dict[str, Any], None, None]:
        e_req_body = {
            'limit': -1,
            'offset': 0,
            'query': query
        }

        request = QueryRequest(headers={
            'type': 'vertices',
        }, body=e_req_body)

        async_generator = self.submit_request(request)
        generator = iter_over_async(async_generator, self.loop)
        yield from generator

    def get_vertex(self, vertex_id: str) -> Dict[str, Any]:
        request = VertexGetRequest(headers={
            SystemAttribute.OGIT__ID.value.name.uri: vertex_id
        }, body={
        })

        async_generator = self.submit_request(request)
        generator = iter_over_async(async_generator, self.loop)
        return next(generator)


'''
var request =
    {
        'id': 'mandatory id for matching the reply',
        'type': 'the type of the request, e.g. get, create, replace, connect, ...',
        '_TOKEN': 'optional, if none specified, the one from the establishing the websocket will be used',
        'headers':
            {
                // headers for the request
            },
        'body':
            {
                // body for the request
            }
    };

var response_envelope = {
    "id": "id of the request",
    "more": true, // `false` if this is the last message for the response
    "multi": false, // `true` if this response is fragmented, the stream of messages represents an array as the final result
    "body": '[]|{}|...' // for responses with `multi=true` the body should be put to an array [] and when `more=false` the result should be the array with the assembled parts
}


var ws = new WebSocket('wss://$url/_g/', ['graph-2.0.0', 'token-' + '$token']);
ws.addEventListener("open", function () {
    if (ws.protocol !== "graph-2.0.0") {
        throw new Error("Expecting WebSocket protocol 'graph-2.0.0', got " + ws.protocol);
    }
    ws.send(JSON.stringify(request));

    //do something with connection
});

var requests = {}; // holds all responses

ws.onmessage = function (msg) {
    var payload = JSON.parse(msg);

    var request = requests[payload.id];
    if (!request) throw new Error("request could not be found " + req.id);

    if (payload.error) {
        // an error must always be delivered
        request.cb(payload);
        delete (requests[payload.id]);
    } else if (!payload.multi && payload.more) {
        throw new Error("non-multi messages cannot be fragmented");
    } else if (!payload.multi) {
        // that's a single response message
        request.cb(payload);
        delete (requests[payload.id]);
    } else {
        // that's a fragmented response, buffer up everything until payload.more = false
        if (payload.body !== null) request.buf.push(payload.body);

        if (!payload.more) {
            request.cb(request.buf);
            delete (requests[payload.id]);
        }
    }
}

var storage_blob_get_content = {
  "id":   "request id",
  "type": "getcontent",
  '_TOKEN': 'optional, if none specified, the one from the establishing the websocket will be used',
  "headers":
  {
    "ogit/_id": "id of the node"
  },
  "body":
  {
    // all parameters for the corresponding REST request are available here
  }
}

var storage_blob_get_content_res = {
  "id":   "request id",
  "multi": true,
  "last": false,
  "body":
  {
    "data": "chunk of blob data",
    "encoding": "base64" // base64 is currently the only encoding possible
  }
}

var identity_me = {
  "id":   "request id",
  "type": "me",
  '_TOKEN': 'optional, if none specified, the one from the establishing the websocket will be used',
  "headers":
  {
  },
  "body":
  {
    // all parameters for the corresponding REST request are available here
  }
}

'''
