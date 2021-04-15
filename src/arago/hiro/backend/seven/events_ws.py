import asyncio
import json
from asyncio import AbstractEventLoop
from asyncio.tasks import Task
from collections import Coroutine
from datetime import timedelta, datetime
from typing import Optional, Callable

import websockets
from urllib3.util import parse_url
from websockets import Subprotocol

from arago.hiro.client.client import HiroClient as HiroRestClient
from arago.hiro.model.auth import ConstantAccessToken, PasswordAccessToken
# https://websockets.readthedocs.io/en/stable/intro.html
from arago.hiro.model.ws import EventsOffset, Filter


class HiroWebSocketClient:
    rest_client: HiroRestClient
    socket: Optional[websockets.WebSocketClientProtocol] = None
    loop: AbstractEventLoop = asyncio.get_event_loop()

    def __init__(self, rest_client: HiroRestClient) -> None:
        super().__init__()
        self.rest_client = rest_client

    def connect(self,
                group_id: Optional[str] = None,
                offset: Optional[EventsOffset] = None,
                all_scopes: Optional[bool] = None,
                delta: Optional[bool] = None) -> None:
        token = self.rest_client.authenticator.get_new_token()
        if isinstance(token, PasswordAccessToken):
            self.schedule_renew_ws_token(token)
        elif not isinstance(token, ConstantAccessToken):
            raise TypeError(token)
        netloc = parse_url(self.rest_client.endpoint).netloc
        endpoint = self.rest_client.model.meta.version()['events-ws'].endpoint
        future = websockets.connect(
            uri='wss://%s%s' % (netloc, endpoint),
            subprotocols=(
                Subprotocol('events-%s' % '1.0.0'),
                Subprotocol('token-%s' % token.value)
            ))
        # not supported by server extra_headers=(('Authorization', 'Bearer %s' % token.value),)
        self.socket = self.loop.run_until_complete(future)

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
        future = self.socket.send(json.dumps({
            'type': 'token',
            'args': {
                '_TOKEN': token
            }
        }))
        self.loop.run_until_complete(future)

    def run_forever(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()

    def listen(self, handler: Callable[[str], Coroutine[[], None, None]]) -> Task:
        task = self.loop.create_task(self.handle_event(handler))
        return task

    def register_filter(self, event_filter: Filter):
        future = self.socket.send(json.dumps({
            'type': 'register',
            'args': {
                'filter-id': str(event_filter.id),
                'filter-type': 'jfilter',
                'filter-content': event_filter.expression
            }
        }))
        self.loop.run_until_complete(future)

    def deregister_filter(self, event_filter: Filter):
        future = self.socket.send(json.dumps({
            'type': 'unregister',
            'args': {
                'filter-id': event_filter.id
            }
        }))
        self.loop.run_until_complete(future)

    def clear_filters(self):
        future = self.socket.send(json.dumps({
            'type': 'clear',
            'args': {}
        }))
        self.loop.run_until_complete(future)

    async def handle_event(self, handler: Callable[[str], Coroutine[[], None, None]]):
        while True:
            message = await self.socket.recv()
            if message == b'':
                continue
            elif isinstance(message, bytes):
                print('skipping binary message')
                continue
            await handler(message)
