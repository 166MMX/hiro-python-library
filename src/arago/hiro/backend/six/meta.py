from typing import TYPE_CHECKING, Any, Dict, Final, List, Mapping, Optional, Tuple

from requests import Response

from arago.hiro.abc.meta import AbcMetaRest, AbcMetaData, AbcMetaModel
from arago.hiro.model.meta import Api
from arago.hiro.model.static import VERSION_SIX_RESULT

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro6MetaRest(AbcMetaRest):
    __base_client: Final['HiroRestBaseClient']

    PATH_INFO: Final[str] = '/info'

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        fork = client.fork()
        fork.authenticator.exclude_path(literal=Hiro6MetaRest.PATH_INFO)
        self.__base_client = fork

    def info(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__base_client.request(
            'GET', Hiro6MetaRest.PATH_INFO, headers=headers
        )

    def version(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        raise NotImplementedError('UnsupportedOperation')

    def versions(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        raise NotImplementedError('UnsupportedOperation')


class Hiro6MetaData(AbcMetaData):
    __rest_client: Final[Hiro6MetaRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro6MetaRest(client)

    def info(self) -> Dict[str, Any]:
        with self.__rest_client.info(
                headers={'Accept': 'application/json'}
        ) as response:
            res_data = response.json()
            return res_data

    def version(self) -> Mapping[str, Mapping[str, Optional[str]]]:
        res_data = VERSION_SIX_RESULT
        return res_data

    def versions(self) -> Mapping[str, Tuple[Mapping[str, Optional[str]]]]:
        res_data = self.version()
        result = {key: [value] for key, value in res_data.items()}
        return result


class Hiro6MetaModel(AbcMetaModel):
    __data_client: Final[Hiro6MetaData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro6MetaData(client)

    def info(self) -> Dict[str, Any]:
        return self.__data_client.info()

    def version(self) -> Dict[str, Api]:
        res_data = self.__data_client.version()
        result = {key: AbcMetaModel._transform(value) for key, value in res_data.items()}
        return result

    def versions(self) -> Dict[str, List[Api]]:
        res_data = self.__data_client.versions()
        result = {key: [AbcMetaModel._transform(entry) for entry in value] for key, value in res_data.items()}
        return result
