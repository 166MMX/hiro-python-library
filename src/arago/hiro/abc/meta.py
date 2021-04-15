from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Tuple

from requests import Response

from arago.hiro.model.meta import Api, Support, Lifecycle
from .common import AbcRest, AbcData, AbcModel

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient

# undocumented


# noinspection PyUnusedLocal
class AbcMetaRest(AbcRest):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def info(self, headers: Optional[Mapping[str, str]]) -> Response:
        ...

    @abstractmethod
    def version(self, headers: Optional[Mapping[str, str]]) -> Response:
        ...

    @abstractmethod
    def versions(self, headers: Optional[Mapping[str, str]]) -> Response:
        ...


# noinspection PyUnusedLocal
class AbcMetaData(AbcData):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    @abstractmethod
    def info(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def version(self) -> Mapping[str, Mapping[str, Optional[str]]]:
        ...

    @abstractmethod
    def versions(self) -> Mapping[str, Tuple[Mapping[str, Optional[str]]]]:
        ...


# noinspection PyUnusedLocal
class AbcMetaModel(AbcModel):
    __slots__ = ()

    @abstractmethod
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        ...

    # TODO declare concrete return type
    @abstractmethod
    def info(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def version(self) -> Dict[str, Api]:
        ...

    @abstractmethod
    def versions(self) -> Dict[str, List[Api]]:
        ...

    # TODO maybe move
    @staticmethod
    def _transform(value: Mapping[str, Any]) -> Api:
        value = dict(value)
        if 'lifecycle' in value:
            value['lifecycle'] = Lifecycle[str(value['lifecycle']).upper()]
        if 'support' in value:
            value['support'] = Support[str(value['support']).upper()]
        return Api(**value)
