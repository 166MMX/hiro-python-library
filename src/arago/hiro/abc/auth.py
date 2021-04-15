from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional

from requests import Response

from arago.hiro.model.auth import SessionCredentials, AccessToken, ClientCredentials
from .common import AbcRest, AbcData, AbcModel

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


# noinspection PyUnusedLocal
class AbcAuthRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def password(self, req_data: Mapping[str, Any], headers: Optional[Mapping[str, str]]) -> Response:
        ...

    @abstractmethod
    def revoke(self, req_data: Mapping[str, Any], headers: Optional[Mapping[str, str]]) -> Response:
        ...


# noinspection PyUnusedLocal
class AbcAuthData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def password(self, client_id: str, client_secret: str, username: str, password: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def revoke(self, client_id: str) -> Dict[str, Any]:
        ...


# noinspection PyUnusedLocal
class AbcAuthModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def password(self, credentials: SessionCredentials) -> AccessToken:
        ...

    @abstractmethod
    def revoke(self, client_cred: ClientCredentials) -> None:
        ...
