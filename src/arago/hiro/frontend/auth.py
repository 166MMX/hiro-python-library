from typing import TYPE_CHECKING, Dict, Any, Mapping, Optional, Final

from requests import Response

from arago.hiro.abc.auth import AbcAuthRest, AbcAuthData, AbcAuthModel
from arago.hiro.model.auth import SessionCredentials, AccessToken, ClientCredentials
from arago.hiro.model.probe import Version

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class AuthRest(AbcAuthRest):
    __client: Final[AbcAuthRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.auth import Hiro6AuthRest as ImplAuthRest
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.auth import Hiro7AuthRest as ImplAuthRest
        else:
            raise RuntimeError('IllegalState')
        self.__client = ImplAuthRest(client)

    def password(self, req_data: Mapping[str, Any], headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__client.password(req_data, headers)

    def revoke(self, req_data: Mapping[str, Any], headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__client.revoke(req_data, headers)


class AuthData(AbcAuthData):
    __client: Final[AbcAuthData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.auth import Hiro6AuthData as ImplAuthData
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.auth import Hiro7AuthData as ImplAuthData
        else:
            raise RuntimeError('IllegalState')
        self.__client = ImplAuthData(client)

    def password(self, client_id: str, client_secret: str, username: str, password: str) -> Dict[str, Any]:
        return self.__client.password(client_id, client_secret, username, password)

    def revoke(self, client_id: str) -> Dict[str, Any]:
        return self.__client.revoke(client_id)


class AuthModel(AbcAuthModel):
    __client: Final[AbcAuthModel]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.auth import Hiro6AuthModel as ImplAuthModel
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.auth import Hiro7AuthModel as ImplAuthModel
        else:
            raise RuntimeError('IllegalState')
        self.__client = ImplAuthModel(client)

    def password(self, credentials: SessionCredentials) -> AccessToken:
        return self.__client.password(credentials)

    def revoke(self, client_cred: ClientCredentials) -> None:
        return self.__client.revoke(client_cred)
