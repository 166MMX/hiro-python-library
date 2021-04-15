from typing import TYPE_CHECKING, Dict, Any, List, Mapping, Optional, Final, Tuple

from requests.models import Response

from arago.hiro.abc.meta import AbcMetaRest, AbcMetaData, AbcMetaModel
from arago.hiro.model.meta import Api
from arago.hiro.model.probe import Version

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class MetaRest(AbcMetaRest):
    __client: Final[AbcMetaRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.meta import Hiro6MetaRest as ImplMetaRest
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.meta import Hiro7MetaRest as ImplMetaRest
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplMetaRest(client)

    def info(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__client.info(headers)

    def version(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__client.version(headers)

    def versions(self, headers: Optional[Mapping[str, str]] = None) -> Response:
        return self.__client.versions(headers)


class MetaData(AbcMetaData):
    __client: Final[AbcMetaData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.meta import Hiro6MetaData as ImplMetaData
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.meta import Hiro7MetaData as ImplMetaData
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplMetaData(client)

    def info(self) -> Dict[str, Any]:
        return self.__client.info()

    def version(self) -> Mapping[str, Mapping[str, Optional[str]]]:
        return self.__client.version()

    def versions(self) -> Mapping[str, Tuple[Mapping[str, Optional[str]]]]:
        return self.__client.versions()


class MetaModel(AbcMetaModel):
    __client: Final[AbcMetaModel]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.meta import Hiro6MetaModel as ImplMetaModel
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.meta import Hiro7MetaModel as ImplMetaModel
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplMetaModel(client)

    def info(self) -> Dict[str, Any]:
        return self.__client.info()

    def version(self) -> Dict[str, Api]:
        return self.__client.version()

    def versions(self) -> Dict[str, List[Api]]:
        return self.__client.versions()
