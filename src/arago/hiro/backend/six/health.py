from typing import TYPE_CHECKING, Any, Dict, Final, Mapping, Optional

from requests import Response

from arago.hiro.abc.health import AbcHealthRest, AbcHealthData, AbcHealthModel

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro6HealthRest(AbcHealthRest):
    __base_client: Final['HiroRestBaseClient']

    PATH_HEALTH: Final[str] = '/_health'

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        fork = client.fork()
        fork.authenticator.exclude_path(literal=Hiro6HealthRest.PATH_HEALTH)
        self.__base_client = fork

    def check(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__base_client.request(
            'GET', Hiro6HealthRest.PATH_HEALTH, headers=headers
        )


class Hiro6HealthData(AbcHealthData):
    __rest_client: Final[Hiro6HealthRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6HealthRest(client)

    def check(self) -> Dict[str, Any]:
        with self.__rest_client.check(
                headers={'Accept': 'application/json'}
        ) as response:
            res_data = response.json()
            return res_data


class Hiro6HealthModel(AbcHealthModel):
    __data_client: Final[Hiro6HealthData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro6HealthData(client)

    def check(self) -> Dict[str, Any]:
        return self.__data_client.check()
