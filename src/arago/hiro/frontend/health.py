from typing import TYPE_CHECKING, Dict, Any, Final, Optional, Mapping

from requests.models import Response

from arago.hiro.abc.health import AbcHealthRest, AbcHealthData, AbcHealthModel
from arago.hiro.model.probe import Version

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class HealthRest(AbcHealthRest):
    __client: Final[AbcHealthRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.health import Hiro6HealthRest as ImplHealthRest
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.health import Hiro7HealthRest as ImplHealthRest
        else:
            raise RuntimeError('IllegalState')
        self.__client = ImplHealthRest(client)

    def check(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__client.check(headers)


class HealthData(AbcHealthData):
    __client: Final[AbcHealthData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.health import Hiro6HealthData as ImplHealthData
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.health import Hiro7HealthData as ImplHealthData
        else:
            raise RuntimeError('IllegalState')
        self.__client = ImplHealthData(client)

    def check(self) -> Dict[str, Any]:
        return self.__client.check()


class HealthModel(AbcHealthModel):
    __client: Final[AbcHealthModel]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.health import Hiro6HealthModel as ImplHealthModel
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.health import Hiro7HealthModel as ImplHealthModel
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplHealthModel(client)

    def check(self) -> Dict[str, Any]:
        return self.__client.check()
