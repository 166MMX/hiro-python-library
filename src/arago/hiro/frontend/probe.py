from typing import TYPE_CHECKING, Any, Dict, Final, Mapping, Optional

from requests import Response

from arago.hiro.abc.probe import AbcProbeRest, AbcProbeData, AbcProbeModel
from arago.hiro.model.probe import Version

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class ProbeRest(AbcProbeRest):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)

    def probe(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        raise NotImplementedError()


class ProbeData(AbcProbeData):
    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)

    def probe(self) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()


class ProbeModel(AbcProbeModel):
    __client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__client = client

    def probe(self) -> Optional[Version]:
        from arago.hiro.backend.six.probe import Hiro6ProbeModel
        if Hiro6ProbeModel(self.__client).probe():
            return Version.HIRO_6
        from arago.hiro.backend.seven.probe import Hiro7ProbeModel
        if Hiro7ProbeModel(self.__client).probe():
            return Version.HIRO_7
        from arago.hiro.backend.five.probe import Hiro5ProbeModel
        if Hiro5ProbeModel(self.__client).probe():
            return Version.HIRO_5
        return None
