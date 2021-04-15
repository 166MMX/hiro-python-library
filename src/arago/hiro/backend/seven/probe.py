from typing import TYPE_CHECKING, Any, Dict, Final, Mapping, Optional

from requests import Response

from arago.hiro.abc.probe import AbcProbeRest, AbcProbeData, AbcProbeModel
from arago.hiro.client.exception import HiroClientError
from arago.hiro.model.probe import Version

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro7ProbeRest(AbcProbeRest):
    __base_client: Final['HiroRestBaseClient']

    PATH_VERSION: Final[str] = '/api/version'

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        fork = client.fork()
        fork.authenticator.exclude_path(literal=Hiro7ProbeRest.PATH_VERSION)
        self.__base_client = fork

    def probe(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__base_client.request(
            'GET', Hiro7ProbeRest.PATH_VERSION, headers=headers
        )


class Hiro7ProbeData(AbcProbeData):
    __rest_client: Final[Hiro7ProbeRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro7ProbeRest(client)

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


class Hiro7ProbeModel(AbcProbeModel):
    __data_client: Final[Hiro7ProbeData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro7ProbeData(client)

    def probe(self) -> Optional[Version]:
        res_data = self.__data_client.probe()
        if res_data is None or 'health' not in res_data:
            return None
        health: Dict[str, Any] = res_data['health']
        if 'version' not in health:
            return None
        version: str = health['version']
        if version.startswith('7.'):
            return Version.HIRO_7
        return None
