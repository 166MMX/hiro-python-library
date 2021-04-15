import asyncio
import json
import logging
import re
from asyncio import Future
from asyncio.events import AbstractEventLoop
from asyncio.tasks import Task
from dataclasses import asdict
from datetime import timedelta, datetime
from types import coroutine
from typing import Optional, Dict, Any, Union, Generator, TypeVar, Iterator, AsyncIterable, \
    AsyncGenerator, Iterable, Mapping, Tuple, Literal

import websockets
from urllib3.util import parse_url
from websockets import Subprotocol, WebSocketException
# noinspection PyProtectedMember
from websockets.protocol import State

from arago.hiro.client.client import HiroClient as HiroRestClient
from arago.hiro.model.auth import ConstantAccessToken, PasswordAccessToken
from arago.hiro.model.graph.attribute import SystemAttribute, VirtualAttribute, attribute_to_str, ReadOnlyAttribute, \
    FinalAttribute
# https://websockets.readthedocs.io/en/stable/intro.html
from arago.hiro.model.graph.edge import EDGE_TYPE_T
from arago.hiro.model.graph.vertex import VERTEX_TYPE_T, VERTEX_ID_T_co
from arago.hiro.model.storage import TimeSeriesValue
from arago.hiro.model.ws import ResponseEnvelope, ErrorEnvelope, SuccessEnvelope, WebSocketRequest, QueueMarker, \
    RequestMessage, QueryRequest, VertexGetRequest, UpdateTokenRequest, TimeSeriesGetValuesRequest
from arago.hiro.utils.datetime import datetime_to_timestamp_ms
from arago.ogit import OgitEntity, OgitAttribute
from arago.ontology import OntologyEntity, Attribute

logger = logging.getLogger(__name__)

_T_co = TypeVar('_T_co', covariant=True)

escape_es_literal_re = re.compile(r'([+-=!&|(){}[\]^"~*?:\\/ ])')


def esc_es(literal: Any) -> str:
    return escape_es_literal_re.sub(r'\\\1', str(literal))


def iter_over_async(source: AsyncIterable[_T_co], loop: AbstractEventLoop) -> Generator[_T_co, None, None]:
    # https://stackoverflow.com/questions/63587660/
    iterator = source.__aiter__()
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

    async def connect(self) -> None:
        token = self.rest_client.authenticator.get_new_token()
        if isinstance(token, PasswordAccessToken):
            self.schedule_renew_ws_token(token)
        elif not isinstance(token, ConstantAccessToken):
            raise TypeError(token)
        netloc = parse_url(self.rest_client.endpoint).netloc
        endpoint = self.rest_client.model.meta.version()['graph-ws'].endpoint
        # noinspection PyTypeChecker
        self.socket = await websockets.connect(
            uri='wss://%s%s' % (netloc, endpoint),
            subprotocols=(
                Subprotocol('graph-%s' % '2.0.0'),
                Subprotocol('token-%s' % token.value)
            ),
            max_size=None,
        )

        self.rx_task = asyncio.create_task(self.handle_rx_message())

        def done(result: Future):
            if result.cancelled():
                return
            e = result.exception()
            if e is not None:
                raise e

        self.rx_task.add_done_callback(done)

        pass

    def close(self):
        self.socket.close()

    def schedule_renew_ws_token(self,
                                token: PasswordAccessToken,
                                advance: timedelta = timedelta(minutes=2)):
        expires = token.expires_at_datetime
        now = datetime.now(expires.tzinfo)
        delta = expires - now - advance
        scheduled_time = self.loop.time() + delta.total_seconds()
        timer_handle = self.loop.call_at(scheduled_time, self.renew_ws_token)
        return timer_handle

    def renew_ws_token(self):
        token = self.rest_client.authenticator.get_new_token()
        if not isinstance(token, PasswordAccessToken):
            raise TypeError()
        self.schedule_renew_ws_token(token)
        self.update_token(token.value)

    def update_token(self, token: str):
        request = UpdateTokenRequest(_TOKEN=token)
        async_generator = self.submit_request(request)
        generator = iter_over_async(async_generator, self.loop)
        return next(generator)

    async def submit_request(
            self, message: RequestMessage
    ) -> AsyncGenerator[Dict[str, Any], None]:
        if self.socket is None:
            await self.connect()
        if self.socket.state is not State.OPEN:
            raise RuntimeError('not open')
        request = WebSocketRequest(message, self.loop.create_future(), asyncio.Queue())
        self.pending[message.id] = request
        data = asdict(message)
        data['type'] = message.type.value
        json_str = json.dumps(data)
        # print(f'submitting request {message.id!r} {json_str!r}')
        if isinstance(json_str, (str, bytes)):
            logger.debug(f'TX < {json_str!r}')
        await self.socket.send(json_str)
        while True:
            message = await request.res_queue.get()
            if isinstance(message, Exception):
                raise message
            if message is QueueMarker.END:
                break
            yield message

    def send(self, message: Union[str, bytes, Iterable[Union[str, bytes]], AsyncIterable[Union[str, bytes]]]):
        if isinstance(message, (str, bytes)):
            logger.debug(f'TX < {message!r}')
        self.socket.send(message)

    async def handle_rx_message(self):
        message: str
        while True:
            try:
                message = await self.socket.recv()
                # logger.debug(f'RX > {message!r}')
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
                # logger.debug(f'revived complete response {envelope.id!r} {envelope.body!r}')
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
                # logger.debug(f'received chunked response {envelope.id!r} {envelope.body!r}')
                if envelope.body is not None:
                    await request.res_queue.put(envelope.body)
                if not envelope.more:  # last response
                    del self.pending[envelope.id]
                    await request.res_queue.put(QueueMarker.END)
                    request.future.set_result(None)

    def search_index(
            self,
            query: str,
            include_deleted: Optional[bool] = None,  # TODO undocumented # server default: False
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            count: Optional[bool] = None,  # server default: False
            req_data: Optional[Mapping[str, Any]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        async_generator = self.search_async_index(
            query,
            include_deleted, order, offset, limit,
            fields, list_meta, count, req_data, )
        generator = iter_over_async(async_generator, self.loop)
        yield from generator

    async def search_async_index(
            self,
            query: str,
            include_deleted: Optional[bool] = None,  # TODO undocumented # server default: False
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            count: Optional[bool] = None,  # server default: False
            req_data: Optional[Mapping[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        # <editor-fold name="effective request data">
        e_req_body = {
            'query': query
        }

        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_req_body['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if order is not None:
            if isinstance(order, Tuple):
                e_req_body['order'] = ' '.join(order)
            elif isinstance(order, Iterable):
                e_req_body['order'] = ','.join(' '.join(pair) for pair in order)
            else:
                raise TypeError(type(order))

        if offset is not None:
            if isinstance(offset, int):
                if offset > 0:
                    e_req_body['offset'] = '%i' % offset
                else:
                    raise ValueError('Offset must be an integer greater zero')
            else:
                raise TypeError(type(offset))
        else:
            e_req_body['offset'] = 0

        if limit is not None:
            if isinstance(limit, int):
                if limit > 0:
                    e_req_body['limit'] = '%i' % limit
                else:
                    raise ValueError('Limit must be an integer greater zero')
            else:
                raise TypeError(type(limit))
        else:
            e_req_body['limit'] = -1

        if fields is not None:
            if isinstance(fields, str):
                e_req_body['fields'] = fields
            elif isinstance(fields, Iterable):
                e_fields = [attribute_to_str(field) for field in fields] if fields else None
                e_req_body['fields'] = ','.join(e_fields)
            elif isinstance(fields, (
                    Attribute, OgitAttribute, VirtualAttribute, SystemAttribute, ReadOnlyAttribute, FinalAttribute)):
                e_req_body['fields'] = attribute_to_str(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_req_body['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if count is not None:
            if isinstance(count, bool):
                e_req_body['count'] = str(count).lower()
            else:
                raise TypeError(type(count))

        if req_data is not None:
            if isinstance(req_data, Mapping):
                e_req_body.update(req_data)
            else:
                raise TypeError(type(req_data))
        # </editor-fold>

        logger.debug('ES Query >> %s <<', query)

        request = QueryRequest(headers={
            'type': 'vertices',
        }, body=e_req_body)

        async for v in self.submit_request(request):
            yield v

    def search_index_by_type(
            self,
            query: Union[OgitEntity, OntologyEntity, str],
            include_deleted: Optional[bool] = None,  # TODO undocumented # server default: False
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            count: Optional[bool] = None,  # server default: False
            req_data: Optional[Mapping[str, Any]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        return self.search_index(
            query=f'+{esc_es(OgitAttribute.OGIT__TYPE)}:"{query!s}"',
            include_deleted=include_deleted,
            order=order,
            offset=offset,
            limit=limit,
            fields=fields,
            list_meta=list_meta,
            count=count,
            req_data=req_data
        )

    def search_graph(
            self,
            root_id: str,  # VERTEX_ID_T
            query: str,
            fields: Optional[Union[str, Iterable[str]]] = None,  # ATTRIBUTE_T_co  # TODO TEST
            list_meta: Optional[bool] = None,  # TODO TEST
            include_deleted: Optional[bool] = None,  # TODO TEST
            headers: Optional[Mapping[str, str]] = None,
            req_body: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:  # VERTEX_T_co
        async_generator = self.search_async_graph(
            root_id, query, fields, list_meta, include_deleted, headers, req_body, )
        generator = iter_over_async(async_generator, self.loop)
        yield from generator

    async def search_async_graph(
            self,
            root_id: str,  # VERTEX_ID_T
            query: str,
            fields: Optional[Union[str, Iterable[str]]] = None,  # ATTRIBUTE_T_co  # TODO TEST
            list_meta: Optional[bool] = None,  # TODO TEST
            include_deleted: Optional[bool] = None,  # TODO TEST
            headers: Optional[Mapping[str, str]] = None,
            req_body: Optional[Mapping[str, str]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:  # VERTEX_T_co
        # Gremlin Graph Query: g.V({vertex_id}).outE({edge_type}).has('ogit/_in-type',within({vertex_types})).inV().range({offset}, {limit}})
        # Gremlin Graph Query: g.V({vertex_id}).inE({edge_type}).has('ogit/_out-type',within({vertex_types})).outV().range({offset}, {limit}})
        # Gremlin Graph Query: g.V({vertex_id}).{direction}({edge_type}).hasLabel(within({vertex_types})).range({offset}, {limit}})
        # .order().by('age', asc)
        # .count()

        # <editor-fold name="effective headers">
        e_headers = {
            'type': 'gremlin',
        }
        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_headers['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if fields is not None:
            if isinstance(fields, str):
                e_headers['fields'] = fields
            elif isinstance(fields, Iterable):
                e_headers['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_headers['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        # <editor-fold name="effective request data">
        e_req_body = {
            'root': root_id,
            'query': query
        }

        if req_body is not None:
            if isinstance(req_body, Mapping):
                e_req_body.update(req_body)
            else:
                raise TypeError(type(req_body))
        # </editor-fold>

        request = QueryRequest(headers=e_headers, body=e_req_body)

        async_generator = self.submit_request(request)
        async for v in async_generator:
            yield v

    def search_connected(
            self,
            vertex_id: str,  # VERTEX_ID_T
            edge_type: EDGE_TYPE_T,  # EDGE_TYPE_T
            direction: Optional[Literal['in', 'out', 'both']] = None,
            fields: Optional[Union[str, Iterable[str]]] = None,  # ATTRIBUTE_T_co  # TODO TEST
            vertex_types: Optional[Union[Iterable[VERTEX_TYPE_T], VERTEX_TYPE_T]] = None,  # VERTEX_TYPE_T
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            order: Optional[Tuple[str, str]] = None,
            count: Optional[bool] = None,
            list_meta: Optional[bool] = None,  # TODO TEST
            include_deleted: Optional[bool] = None,  # TODO TEST
            headers: Optional[Mapping[str, str]] = None,
            req_body: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:  # VERTEX_T_co
        # Gremlin Graph Query: g.V({vertex_id}).outE({edge_type}).has('ogit/_in-type',within({vertex_types})).inV().range({offset}, {limit}})
        # Gremlin Graph Query: g.V({vertex_id}).inE({edge_type}).has('ogit/_out-type',within({vertex_types})).outV().range({offset}, {limit}})
        # Gremlin Graph Query: g.V({vertex_id}).{direction}({edge_type}).hasLabel(within({vertex_types})).range({offset}, {limit}})
        # .order().by('age', asc)
        # .count()

        stmt = ''

        # <editor-fold name="request query">
        if isinstance(direction, str):
            # .outE({edge_type})..inV()
            # .inE({edge_type})..outV()
            # .bothE({edge_type})..bothV()
            if direction == 'out':
                edge_dir_stmt = 'outE'
                vertex_dir_stmt = '.inV()'
            elif direction == 'in':
                edge_dir_stmt = 'inE'
                vertex_dir_stmt = '.outV()'
            elif direction == 'both':
                edge_dir_stmt = 'bothE'
                vertex_dir_stmt = '.otherV()'
            else:
                raise RuntimeError()
        elif direction is None:
            edge_dir_stmt = 'bothE'
            vertex_dir_stmt = 'bothV'
        else:
            raise RuntimeError()

        stmt += edge_dir_stmt

        if isinstance(edge_type, str):
            stmt += f"('{edge_type!s}')"
        else:
            stmt += '()'

        if vertex_types is None:
            pass
        else:
            # .has('ogit/_in-type',within({vertex_types}))
            # .has('ogit/_out-type',within({vertex_types}))
            # .hasLabel(within({vertex_types}))

            if direction in ('out', 'in'):
                stmt += '.has'
            elif direction == 'both':
                stmt += '.hasLabel'
            else:
                raise RuntimeError()

            if isinstance(vertex_types, Iterable) and not isinstance(vertex_types, str):
                args = ','.join(f"'{vertex_type}'" for vertex_type in vertex_types)
                predicate = f'within({args})'
            elif isinstance(vertex_types, str):
                predicate = f"'{vertex_types}'"
            elif isinstance(vertex_types, OgitEntity):
                predicate = f"'{vertex_types!s}'"
            elif isinstance(vertex_types, OntologyEntity):
                predicate = f"'{vertex_types!s}'"
            else:
                raise RuntimeError()

            if direction == 'out':
                stmt += f"('{str(VirtualAttribute.OGIT__IN_TYPE)}',{predicate})"
            elif direction == 'in':
                stmt += f"('{str(VirtualAttribute.OGIT__OUT_TYPE)}',{predicate})"
            elif direction == 'both':
                stmt += f"({predicate})"
            else:
                raise RuntimeError()

        stmt += vertex_dir_stmt

        if count is True:
            stmt += '.count()'

        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {
            'type': 'gremlin',
        }
        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_headers['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if fields is not None:
            if isinstance(fields, str):
                e_headers['fields'] = fields
            elif isinstance(fields, Iterable):
                e_headers['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_headers['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        # <editor-fold name="effective request data">
        e_req_body = {
            'root': vertex_id,
            'query': stmt
        }

        if req_body is not None:
            if isinstance(req_body, Mapping):
                e_req_body.update(req_body)
            else:
                raise TypeError(type(req_body))
        # </editor-fold>

        request = QueryRequest(headers=e_headers, body=e_req_body)

        async_generator = self.submit_request(request)
        generator = iter_over_async(async_generator, self.loop)
        yield from generator

        # e_fields = [attribute_to_str(field) for field in fields] if fields else None
        # e_vertex_types = (vertex_type_to_str(vertex_type) for vertex_type in vertex_types) if vertex_types else None
        #
        # #             if count is True:
        # #                 return next(items)
        # items = self.__data_client.connected(vertex_id, edge_type, direction, e_fields, e_vertex_types, offset, limit)
        # vertices = to_vertices(items, self.__base_client)
        # yield from vertices

    def get_vertex(
            self,
            vertex_id: str,
            include_deleted: Optional[bool] = None,  # server default: False
            v_id: Optional[str] = None,
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        # <editor-fold name="effective headers">
        e_headers = {
            str(SystemAttribute.OGIT__ID): vertex_id
        }
        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_headers['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if v_id is not None:
            if isinstance(v_id, str):
                e_headers['vid'] = v_id
            else:
                raise TypeError(type(v_id))

        if fields is not None:
            if isinstance(fields, str):
                e_headers['fields'] = fields
            elif isinstance(fields, Iterable):
                e_headers['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_headers['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        request = VertexGetRequest(headers=e_headers, body={})

        async_generator = self.submit_request(request)
        generator = iter_over_async(async_generator, self.loop)
        return next(generator)

    def get_ts_values(
            self,
            vertex_id: VERTEX_ID_T_co,
            start: datetime,
            end: datetime,
            include_deleted: Optional[bool] = None,
            headers: Optional[Mapping[str, str]] = None,
    ) -> Generator[TimeSeriesValue, None, None]:
        async_generator = self.get_async_ts_values(vertex_id, start, end, include_deleted, headers)
        generator = iter_over_async(async_generator, self.loop)
        yield from generator

    async def get_async_ts_values(
            self,
            vertex_id: VERTEX_ID_T_co,
            start: datetime,
            end: datetime,
            include_deleted: Optional[bool] = None,
            headers: Optional[Mapping[str, str]] = None,
    ) -> AsyncGenerator[TimeSeriesValue, None]:
        # <editor-fold name="effective headers">
        e_headers = {
            str(SystemAttribute.OGIT__ID): vertex_id
        }
        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_headers['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if start is not None:
            if isinstance(start, datetime):
                e_headers['from'] = datetime_to_timestamp_ms(start)
            else:
                raise TypeError(type(include_deleted))

        if end is not None:
            if isinstance(start, datetime):
                e_headers['to'] = datetime_to_timestamp_ms(end)
            else:
                raise TypeError(type(include_deleted))

        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        request = TimeSeriesGetValuesRequest(headers=e_headers, body={})

        async_generator = self.submit_request(request)
        async for value in async_generator:
            yield TimeSeriesValue(**value)


'''
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
