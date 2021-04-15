from typing import Mapping, Any, Optional

from arago.hiro.model.graph.attribute import ATTRIBUTE_T
from arago.hiro.model.graph.dict import GraphDict
from arago.hiro.model.graph.vertex import HIRO_BASE_CLIENT_T_co, VERTEX_T_co, Vertex
from arago.hiro.model.storage import BlobVertex, TimeSeriesVertex
from arago.ogit import OgitAttribute, OgitEntity


def to_vertex(
        data: Mapping[ATTRIBUTE_T, Any],
        client: Optional[HIRO_BASE_CLIENT_T_co] = None
) -> VERTEX_T_co:
    vertex_type = GraphDict(data).get(OgitAttribute.OGIT__TYPE)
    e_vertex_type = vertex_type

    if e_vertex_type is OgitEntity.OGIT_ATTACHMENT:
        return BlobVertex(data, client=client, draft=False)
    elif e_vertex_type is OgitEntity.OGIT_DATA_LOG:
        raise NotImplementedError()
    elif e_vertex_type is OgitEntity.OGIT_TIME_SERIES:
        return TimeSeriesVertex(data, client=client, draft=False)
    else:
        return Vertex(data, client=client, draft=False)
