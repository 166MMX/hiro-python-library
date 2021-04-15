import base64
from typing import Dict, Generator

import pytest

from arago.hiro.client.client import HiroClient
from arago.hiro.client.model_client import HiroRestClient, HiroDataClient, HiroModelClient
from arago.hiro.model.auth import SessionCredentials, ClientCredentials, AccountCredentials


@pytest.fixture(scope='module')
def data() -> Dict[str, str]:
    # noinspection SpellCheckingInspection
    return {
        'endpoint': 'https://pod1159.saasarago.com',
        'client_id': '',
        'client_secret': ''
                         ''
                         ''
                         '',
        'username': '',
        'password': r''''''
    }


@pytest.fixture(scope='module')
def client(data: Dict[str, str]) -> HiroClient:
    return HiroClient.create_stringly(**data)


@pytest.fixture(scope='module')
def rest_client(client: HiroClient) -> Generator[HiroRestClient, None, None]:
    yield HiroRestClient(client)


@pytest.fixture(scope='module')
def data_client(client: HiroClient) -> Generator[HiroDataClient, None, None]:
    yield HiroDataClient(client)


@pytest.fixture(scope='module')
def model_client(client: HiroClient) -> Generator[HiroModelClient, None, None]:
    yield HiroModelClient(client)


@pytest.fixture(scope='module')
def user_agent(client: HiroClient) -> str:
    return client.session.headers['User-Agent']


@pytest.fixture(scope='module')
def credentials(data: Dict[str, str]) -> SessionCredentials:
    return SessionCredentials(
        ClientCredentials(data['client_id'], data['client_secret']),
        AccountCredentials(data['username'], data['password'])
    )


@pytest.fixture(scope='module')
def png_img() -> bytes:
    # https://www.flaticon.com/free-icon/small-bookmark_84510
    # https://pngcrush.com/
    # https://onlinepngtools.com/convert-png-to-base64
    # noinspection SpellCheckingInspection
    return base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQ''CAQAAAC1+jfqAAAAcElEQVQoz2P4z/Cf'
        'geEkwwos8CRYDkys+M+ACSGiI1MBAyMD''Ix4FDGwMS4CQDYcCBk6GVQx2QLiKgROL'
        'AgYehvUM5mCeOZDFg6aAQYBhM4MR3HYj''IE8AWcEuhu0MOig+0AGK7EIoOMagjuFJ'
        'dUh0AwBCS9yY0MHerQAAAABJRU5ErkJg''gg=='
    )
