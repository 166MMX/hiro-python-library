from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional

from requests import Response

from arago.hiro.model.probe import Version
from .common import AbcRest, AbcData, AbcModel

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient

# virtual endpoint implemented for version query


# noinspection PyUnusedLocal
class AbcProbeRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def probe(self, headers: Optional[Mapping[str, str]]) -> Response:
        ...


# noinspection PyUnusedLocal
class AbcProbeData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def probe(self) -> Optional[Dict[str, Any]]:
        ...


# noinspection PyUnusedLocal
class AbcProbeModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def probe(self) -> Optional[Version]:
        ...
