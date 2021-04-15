from typing import TYPE_CHECKING, Any, Dict, Final, Mapping, Optional

from requests import Response

from arago.hiro.abc.auth import AbcAuthRest, AbcAuthData, AbcAuthModel
from arago.hiro.model.auth import SessionCredentials, AccessToken, ClientCredentials, PasswordAccessToken

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient

# https://pod1159.saasarago.com/_api/index.html
# https://pod1159.saasarago.com/_api/specs/auth.yaml
# https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/auth-rest-api.html
# https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/authentication.html

# OAuth 2.0 Password Grant
# https://oauth.net/2/grant-types/password/
# https://tools.ietf.org/html/rfc6749#section-1.3.3

# OAuth 2.0 Token Revocation
# https://oauth.net/2/token-revocation/
# https://tools.ietf.org/html/rfc7009


class Hiro6AuthRest(AbcAuthRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        path = client.root.model.meta.version()['auth'].endpoint
        fork = client.fork(path)
        fork.authenticator.exclude_path(literal=f'{path}/app')
        self.__base_client = fork

    def password(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/app'
        return self.__base_client.request(
            'POST', uri, json=req_data, headers=headers
        )

    def revoke(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None
    ) -> Response:
        uri = '/revoke'
        return self.__base_client.request(
            'POST', uri, json=req_data, headers=headers
        )
        # TODO class only responsible 4 rest
        # self.__base_client.authenticator.invalidate_token()


class Hiro6AuthData(AbcAuthData):
    __rest_client: Final[Hiro6AuthRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6AuthRest(client)

    def password(
            self,
            client_id: str,
            client_secret: str,
            username: str,
            password: str,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        e_req_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password,
        }
        if isinstance(req_data, Mapping):
            e_req_data.update(req_data)

        e_headers = {'Accept': 'application/json'}
        if isinstance(headers, Mapping):
            e_headers.update(headers)

        with self.__rest_client.password(
                e_req_data, headers=e_headers
        ) as response:
            res_data = response.json()
            return res_data

    def revoke(
            self,
            client_id: str,
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Dict[str, Any]:
        e_req_data = {
            'client_id': client_id,
        }
        if isinstance(req_data, Mapping):
            e_req_data.update(req_data)

        e_headers = {'Accept': 'application/json'}
        if isinstance(headers, Mapping):
            e_headers.update(headers)

        with self.__rest_client.revoke(
                e_req_data, headers=e_headers
        ) as response:
            res_data = response.json()
            return res_data


class Hiro6AuthModel(AbcAuthModel):
    __data_client: Final[Hiro6AuthData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro6AuthData(client)

    def password(
            self,
            credentials: SessionCredentials
    ) -> AccessToken:
        res_data = self.__data_client.password(
            credentials.client.id,
            credentials.client.secret,
            credentials.account.username,
            credentials.account.password
        )
        # TODO refactor PasswordAccessToken to be like Vertex
        token = PasswordAccessToken.from_data(res_data)
        return token

    def revoke(
            self,
            credentials: ClientCredentials
    ) -> None:
        self.__data_client.revoke(
            credentials.id
        )
