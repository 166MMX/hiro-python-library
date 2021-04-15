from typing import TYPE_CHECKING, Final

from arago.hiro.abc.graph import AbcGraphModel, AbcGraphEdgeModel, AbcGraphVertexModel, AbcGraphRest, \
    AbcGraphData, AbcGraphEdgeRest, AbcGraphVertexRest, AbcGraphEdgeData, AbcGraphVertexData
from arago.hiro.model.probe import Version

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


# TODO evaluate generics usage for properties


class GraphRest(AbcGraphRest):
    __client: Final[AbcGraphRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.graph import Hiro6GraphRest as ImplGraphRest
        elif version == Version.HIRO_7:
            raise NotImplementedError()
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplGraphRest(client)

    @property
    def edge(self) -> AbcGraphEdgeRest:
        return self.__client.edge

    @property
    def vertex(self) -> AbcGraphVertexRest:
        return self.__client.vertex


class GraphData(AbcGraphData):
    __client: Final[AbcGraphData]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.graph import Hiro6GraphData as ImplGraphData
        elif version == Version.HIRO_7:
            from arago.hiro.backend.seven.graph import Hiro7GraphData as ImplGraphData
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplGraphData(client)

    @property
    def edge(self) -> AbcGraphEdgeData:
        return self.__client.edge

    @property
    def vertex(self) -> AbcGraphVertexData:
        return self.__client.vertex


class GraphModel(AbcGraphModel):
    __client: Final[AbcGraphModel]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        version = client.root.model.version
        if version == Version.HIRO_5:
            raise NotImplementedError()
        elif version == Version.HIRO_6:
            from arago.hiro.backend.six.graph import Hiro6GraphModel as ImplGraphModel
        elif version == Version.HIRO_7:
            raise NotImplementedError()
        else:
            raise RuntimeError('Unreachable')
        self.__client = ImplGraphModel(client)

    @property
    def edge(self) -> AbcGraphEdgeModel:
        return self.__client.edge

    @property
    def vertex(self) -> AbcGraphVertexModel:
        return self.__client.vertex
