from typing import TYPE_CHECKING, Any, Dict, Final, List, Mapping, Optional, Tuple

from requests import Response

from arago.hiro.abc.meta import AbcMetaRest, AbcMetaData, AbcMetaModel
from arago.hiro.model.meta import Api, Lifecycle, Support

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro7MetaRest(AbcMetaRest):
    __base_client: Final['HiroRestBaseClient']

    PATH_VERSION: Final[str] = '/api/version'
    PATH_VERSIONS: Final[str] = '/api/versions'

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        fork = client.fork()
        fork.authenticator.exclude_path(literal=Hiro7MetaRest.PATH_VERSION)
        fork.authenticator.exclude_path(literal=Hiro7MetaRest.PATH_VERSIONS)
        self.__base_client = fork

    def info(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        raise NotImplementedError('UnsupportedOperation')

    def version(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__base_client.request(
            'GET', '/api/version', headers=headers
        )

    def versions(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__base_client.request(
            'GET', '/api/versions', headers=headers
        )

    # TODO remove
    def __version(self, api: str) -> Api:
        with self.__base_client.request(
                'GET', '/api/version', headers={'Accept': 'application/json'}
        ) as response:
            res_data = response.json()
            if api not in res_data:
                raise RuntimeError()
            data = res_data[api]
            data['lifecycle'] = Lifecycle(str(data['lifecycle']).upper())
            data['support'] = Support(str(data['support']).upper())
            return Api(**data)


class Hiro7MetaData(AbcMetaData):
    __rest_client: Final[Hiro7MetaRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro7MetaRest(client)

    def info(self) -> Dict[str, Any]:
        raise NotImplementedError('UnsupportedOperation')

    def version(self) -> Mapping[str, Mapping[str, Optional[str]]]:
        with self.__rest_client.version(
                {'Accept': 'application/json'}
        ) as response:
            res_data = response.json()
            return res_data

    def versions(self) -> Mapping[str, Tuple[Mapping[str, Optional[str]]]]:
        with self.__rest_client.versions(
                {'Accept': 'application/json'}
        ) as response:
            res_data = response.json()
            return res_data


class Hiro7MetaModel(AbcMetaModel):
    __data_client: Final[Hiro7MetaData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__data_client = Hiro7MetaData(client)

    def info(self) -> Dict[str, Any]:
        raise NotImplementedError('UnsupportedOperation')

    def version(self) -> Dict[str, Api]:
        res_data = self.__data_client.version()
        result = {key: AbcMetaModel._transform(value) for key, value in res_data.items()}
        return result

    def versions(self) -> Dict[str, List[Api]]:
        res_data = self.__data_client.versions()
        result = {key: [AbcMetaModel._transform(entry) for entry in value] for key, value in res_data.items()}
        return result
