from typing import Generator, Iterator
from typing import Mapping, Any

from arago.hiro.model.graph.dict import GraphDict
from arago.hiro.model.graph.vertex import HIRO_BASE_CLIENT_T_co, VERTEX_T_co, to_vertex_type, Vertex
from arago.hiro.model.storage import BlobVertex, TimeSeriesVertex
from arago.ogit import OgitAttribute, OgitEntity


def to_vertex(
        data: Mapping[str, Any],
        client: HIRO_BASE_CLIENT_T_co
) -> VERTEX_T_co:
    vertex_type = GraphDict(data).get(OgitAttribute.OGIT__TYPE)
    e_vertex_type = to_vertex_type(vertex_type)

    if e_vertex_type is OgitEntity.OGIT_ATTACHMENT:
        return BlobVertex(data, client=client, draft=False)
    elif e_vertex_type is OgitEntity.OGIT_DATA_LOG:
        raise NotImplementedError()
    elif e_vertex_type is OgitEntity.OGIT_TIME_SERIES:
        return TimeSeriesVertex(data, client=client, draft=False)
    else:
        return Vertex(data, client=client, draft=False)


def to_vertices(
        items: Iterator[Mapping[str, Any]],
        client: HIRO_BASE_CLIENT_T_co
) -> Generator[VERTEX_T_co, None, None]:
    for item in items:
        yield to_vertex(item, client)
