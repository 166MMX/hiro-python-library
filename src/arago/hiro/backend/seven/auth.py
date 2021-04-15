from typing import TYPE_CHECKING, Any, Dict, Final, Mapping, Optional

from requests import Response

from arago.hiro.abc.auth import AbcAuthRest, AbcAuthData, AbcAuthModel
from arago.hiro.model.auth import SessionCredentials, AccessToken, ClientCredentials, PasswordAccessToken

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro7AuthRest(AbcAuthRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        path = client.root.model.meta.version()['auth'].endpoint
        fork = client.fork(path)
        fork.authenticator.exclude_path(literal=f'{path}/app')
        self.__base_client = fork

    def password(self, req_data: Mapping[str, Any], headers: Optional[Mapping[str, str]] = None) -> Response:
        uri = '/app'
        return self.__base_client.request(
            'POST', uri, json=req_data, headers=headers
        )

    def revoke(self, req_data: Mapping[str, Any], headers: Optional[Mapping[str, str]] = None) -> Response:
        uri = '/revoke'
        return self.__base_client.request(
            'POST', uri, json=req_data, headers=headers
        )


class Hiro7AuthData(AbcAuthData):
    __rest_client: Final[Hiro7AuthRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro7AuthRest(client)

    def password(self, client_id: str, client_secret: str, username: str, password: str) -> Dict[str, Any]:
        req_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password,
        }
        with self.__rest_client.password(
                req_data, headers={'Accept': 'application/json'}
        ) as response:
            res_data = response.json()
            return res_data

    def revoke(self, client_id: str) -> Dict[str, Any]:
        req_data = {
            'client_id': client_id,
        }
        with self.__rest_client.revoke(
                req_data, headers={'Accept': 'application/json'}
        ) as response:
            res_data = response.json()
            return res_data


class Hiro7AuthModel(AbcAuthModel):
    __data_client: Final[Hiro7AuthData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro7AuthData(client)

    def password(self, credentials: SessionCredentials) -> AccessToken:
        res_data = self.__data_client.password(
            credentials.client.id,
            credentials.client.secret,
            credentials.account.username,
            credentials.account.password,
        )
        token = PasswordAccessToken.from_data(res_data)
        return token

    def revoke(self, client_cred: ClientCredentials) -> None:
        res_data = self.__data_client.revoke(client_cred.id)
        if len(res_data) != 0:
            raise RuntimeError(f'Assert error: Unexpected result "{res_data}"')
