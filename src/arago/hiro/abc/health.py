from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional

from requests import Response

from .common import AbcRest, AbcData, AbcModel

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


# https://tools.ietf.org/html/draft-inadarei-api-health-check-05

# noinspection PyUnusedLocal
class AbcHealthRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def check(self, headers: Optional[Mapping[str, str]]) -> Response:
        ...


# noinspection PyUnusedLocal
class AbcHealthData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def check(self) -> Dict[str, Any]:
        ...


# noinspection PyUnusedLocal
class AbcHealthModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def check(self) -> Dict[str, Any]:
        ...
