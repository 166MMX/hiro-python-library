from typing import TYPE_CHECKING, Any, Dict, Final, Mapping, Optional

from requests import Response

from arago.hiro.abc.probe import AbcProbeRest, AbcProbeData, AbcProbeModel
from arago.hiro.client.exception import HiroClientError
from arago.hiro.model.probe import Version

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro6ProbeRest(AbcProbeRest):
    __base_client: Final['HiroRestBaseClient']

    PATH_INFO: Final[str] = '/info'

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        fork = client.fork()
        fork.authenticator.exclude_path(literal=Hiro6ProbeRest.PATH_INFO)
        self.__base_client = fork

    def probe(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__base_client.request(
            'GET', Hiro6ProbeRest.PATH_INFO, headers=headers
        )


class Hiro6ProbeData(AbcProbeData):
    __rest_client: Final[Hiro6ProbeRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6ProbeRest(client)

    def probe(self) -> Optional[Dict[str, Any]]:
        try:
            response = self.__rest_client.probe(
                headers={'Accept': 'application/json'}
            )
        except HiroClientError:
            return None
        with response:
            res_data = response.json()
            return res_data


class Hiro6ProbeModel(AbcProbeModel):
    __data_client: Final[Hiro6ProbeData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro6ProbeData(client)

    def probe(self) -> Optional[Version]:
        res_data = self.__data_client.probe()
        if res_data is None or 'api-version' not in res_data:
            return None
        version: str = res_data['api-version']
        if version.startswith('6.'):
            return Version.HIRO_6
        return None
