from functools import cached_property
from typing import TYPE_CHECKING

from arago.hiro.frontend.auth import AuthRest, AuthData, AuthModel
from arago.hiro.frontend.graph import GraphRest, GraphData, GraphModel
from arago.hiro.frontend.health import HealthRest, HealthData, HealthModel
from arago.hiro.frontend.meta import MetaRest, MetaData, MetaModel
from arago.hiro.frontend.probe import ProbeModel
from arago.hiro.frontend.search import SearchRest, SearchData, SearchModel
from arago.hiro.frontend.storage import StorageRest, StorageData, StorageModel
from arago.hiro.model.probe import Version

if TYPE_CHECKING:
    from arago.hiro.client.client import HiroClient


class HiroRestClient:
    __client: 'HiroClient'

    def __init__(self, client: 'HiroClient') -> None:
        super().__init__()
        self.__client = client

    @cached_property
    def version(self) -> Version:
        raise NotImplementedError()

    @cached_property
    def meta(self) -> MetaRest:
        return MetaRest(self.__client)

    @cached_property
    def health(self) -> HealthRest:
        return HealthRest(self.__client)

    @cached_property
    def auth(self) -> AuthRest:
        return AuthRest(self.__client)

    @cached_property
    def graph(self) -> GraphRest:
        return GraphRest(self.__client)

    @cached_property
    def search(self) -> SearchRest:
        return SearchRest(self.__client)

    @cached_property
    def storage(self) -> StorageRest:
        return StorageRest(self.__client)

    # @cached_property
    # def iam(self) -> HiroIdentityAndAccessManagementApi:
    #     return HiroIdentityAndAccessManagementApi(self)

    # @cached_property
    # def app(self) -> HiroApplicationsApi:
    #     return HiroApplicationsApi(self)


class HiroDataClient:
    __client: 'HiroClient'

    def __init__(self, client: 'HiroClient') -> None:
        super().__init__()
        self.__client = client

    @cached_property
    def version(self) -> Version:
        raise NotImplementedError()

    @cached_property
    def meta(self) -> MetaData:
        return MetaData(self.__client)

    @cached_property
    def health(self) -> HealthData:
        return HealthData(self.__client)

    @cached_property
    def auth(self) -> AuthData:
        return AuthData(self.__client)

    @cached_property
    def graph(self) -> GraphData:
        return GraphData(self.__client)

    @cached_property
    def search(self) -> SearchData:
        return SearchData(self.__client)

    @cached_property
    def storage(self) -> StorageData:
        return StorageData(self.__client)

    # @cached_property
    # def iam(self) -> HiroIdentityAndAccessManagementApi:
    #     return HiroIdentityAndAccessManagementApi(self)

    # @cached_property
    # def app(self) -> HiroApplicationsApi:
    #     return HiroApplicationsApi(self)


class HiroModelClient:
    __client: 'HiroClient'

    def __init__(self, client: 'HiroClient') -> None:
        super().__init__()
        self.__client = client

    @cached_property
    def version(self) -> Version:
        version = ProbeModel(self.__client).probe()
        if not version:
            raise RuntimeError('Failed to automatically determine HIRO version.')
        return version

    @cached_property
    def meta(self) -> MetaModel:
        return MetaModel(self.__client)

    @cached_property
    def health(self) -> HealthModel:
        return HealthModel(self.__client)

    @cached_property
    def auth(self) -> AuthModel:
        return AuthModel(self.__client)

    @cached_property
    def graph(self) -> GraphModel:
        return GraphModel(self.__client)

    @cached_property
    def search(self) -> SearchModel:
        return SearchModel(self.__client)

    @cached_property
    def storage(self) -> StorageModel:
        return StorageModel(self.__client)

    # @cached_property
    # def iam(self) -> HiroIdentityAndAccessManagementApi:
    #     return HiroIdentityAndAccessManagementApi(self)

    # @cached_property
    # def app(self) -> HiroApplicationsApi:
    #     return HiroApplicationsApi(self)
