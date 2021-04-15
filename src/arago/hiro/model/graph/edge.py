from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property
from typing import Final, List, Optional, Mapping, Union, Any, TYPE_CHECKING, TypeVar

from arago.hiro.model.graph.attribute import VirtualAttribute, GraphType
from arago.hiro.model.graph.dict import GraphDict
from arago.hiro.model.graph.vertex import VertexId
from arago.hiro.utils.cast import to_bool
from arago.hiro.utils.datetime import timestamp_ms_to_datetime
from arago.ogit import OgitAttribute, OgitEntity, OgitVerb as OgitVerb
from arago.ontology import OntologyEntity, OntologyVerb, OntologyAttribute

if TYPE_CHECKING:
    from arago.hiro.client.client import HiroClient

EDGE_ID_DELIMITER: Final[str] = '$$'


class EdgeId(str):
    @cached_property
    def valid(self) -> bool:
        if self.count(EDGE_ID_DELIMITER) != 2:
            raise ValueError(f"""Expected to contain exactly two edge id delimiter '{EDGE_ID_DELIMITER}'""")
        if len(self) < 54:
            raise ValueError(f'Expected len() > 54; got {len(self)}')
        if not self.isascii():
            raise ValueError(f'Expected only ASCII chars')
        return True

    @cached_property
    def __tokens(self) -> List[str]:
        delimiter = EDGE_ID_DELIMITER
        return self.split(delimiter)

    @cached_property
    def out_id(self) -> VertexId:
        value = self.__tokens[0]
        return VertexId(value)

    @cached_property
    def type(self) -> OntologyVerb:
        value = self.__tokens[1]
        ogit_verb: OgitVerb = OgitVerb[value]
        return ogit_verb.value

    @cached_property
    def in_id(self) -> VertexId:
        value = self.__tokens[2]
        return VertexId(value)


@dataclass
class Edge:
    id: Optional[EdgeId] = field(default=None)
    type: Optional[OntologyVerb] = field(default=None)

    in_id: Optional[VertexId] = field(default=None)
    in_type: Optional[OntologyEntity] = field(default=None)
    edge_id: Optional[EdgeId] = field(default=None)
    out_id: Optional[VertexId] = field(default=None)
    out_type: Optional[OntologyEntity] = field(default=None)

    created_by_app: Optional[VertexId] = field(default=None)
    created_by: Optional[str] = field(default=None)
    created_on: Optional[datetime] = field(default=None)

    deleted_by_app: Optional[VertexId] = field(default=None)
    deleted_by: Optional[str] = field(default=None)
    deleted_on: Optional[datetime] = field(default=None)
    is_deleted: bool = field(default=False)

    _draft: bool = field(default=True)
    client: Optional['HiroClient'] = field(default=None)

    def __init__(
            self,
            data: Optional[Mapping[Union[str, OntologyAttribute, OgitAttribute], Any]],
            client: Optional['HiroClient'] = None,
            draft: bool = True
    ) -> None:
        super().__init__()
        self.client = client
        self._draft = draft

        m = GraphDict(data)

        k = VirtualAttribute.OGIT__GRAPH_TYPE
        if k in m:
            graph_type = GraphType(m[k])
            if graph_type is not GraphType.EDGE:
                raise RuntimeError()
        else:
            graph_type = None

        k = OgitAttribute.OGIT__ID
        if k in m:
            self.id = EdgeId(m[k])
            del m[k]
        k = OgitAttribute.OGIT__TYPE
        if k in m:
            verb: OgitVerb = OgitVerb[m[k]]
            self.type = verb.value
            del m[k]

        k = VirtualAttribute.OGIT__OUT_TYPE
        if k in m:
            entity: OgitEntity = OgitEntity[m[k]]
            self.out_type = entity.value
            del m[k]
        k = VirtualAttribute.OGIT__OUT_ID
        if k in m:
            self.out_id = VertexId(m[k])
            del m[k]
        k = OgitAttribute.OGIT__EDGE_ID
        if k in m:
            self.edge_id = EdgeId(m[k])
            del m[k]
        k = VirtualAttribute.OGIT__IN_TYPE
        if k in m:
            entity: OgitEntity = OgitEntity[m[k]]
            self.in_type = entity.value
            del m[k]
        k = VirtualAttribute.OGIT__IN_ID
        if k in m:
            self.in_id = VertexId(m[k])
            del m[k]

        k = OgitAttribute.OGIT__CREATOR_APP
        if k in m:
            self.created_by_app = VertexId(m[k])
            del m[k]
        k = OgitAttribute.OGIT__CREATOR
        if k in m:
            self.created_by = m[k]
            del m[k]
        k = OgitAttribute.OGIT__CREATED_ON
        if k in m:
            self.created_on = timestamp_ms_to_datetime(m[k])
            del m[k]

        k = OgitAttribute.OGIT__DELETED_BY_APP
        if k in m:
            self.deleted_by_app = VertexId(m[k])
            del m[k]
        k = OgitAttribute.OGIT__DELETED_BY
        if k in m:
            self.deleted_by = m[k]
            del m[k]
        k = OgitAttribute.OGIT__DELETED_ON
        if k in m:
            self.deleted_on = timestamp_ms_to_datetime(m[k])
            del m[k]
        k = OgitAttribute.OGIT__IS_DELETED
        if k in m:
            self.is_deleted = to_bool(m[k])
            del m[k]

        if graph_type:
            k = VirtualAttribute.OGIT__GRAPH_TYPE
            del m[k]

        for k in m:
            if isinstance(k, (OgitAttribute, OntologyAttribute)):
                raise KeyError(f'Unexpected {k!r} found')
            if not isinstance(k, str):
                raise TypeError(f'Unexpected type of key found: {type(k)}')
            if k.startswith('ogit/_'):
                raise KeyError(f'Unexpected system attribute found: {k!r}')
            elif k.startswith('ogit/'):
                raise KeyError(f'Unexpected OGIT attribute found: {k!r}')
            elif k.startswith('/'):
                raise KeyError(f'Unexpected free attribute found: {k!r}')
            else:
                raise KeyError(f'Unexpected key found: {k!r}')


EDGE_T_co = TypeVar('EDGE_T_co', bound=Edge, covariant=True)
EDGE_T = EDGE_T_co
EDGE_ID_T = Union[
    EdgeId,
    str
]
EDGE_TYPE_T = Union[
    OntologyVerb,
    OgitVerb,
    str
]


def to_verb(v: Optional[Union[EDGE_T_co, EDGE_TYPE_T]]) -> Optional[OntologyVerb]:
    if v is None:
        return None
    if isinstance(v, OntologyVerb):
        return v
    if isinstance(v, OgitVerb):
        return v.value
    if isinstance(v, Edge):
        return v.type
    if isinstance(v, str):
        verb: OgitVerb = OgitVerb[v]
        return verb.value
    raise TypeError(f'Expected any of {{str,Edge,OgitVerb,OntologyVerb}}, but got {type(v)}')


def to_edge_id(v: Optional[Union[EDGE_T_co, EDGE_ID_T]]) -> Optional[EdgeId]:
    if v is None:
        return None
    if isinstance(v, EdgeId):
        return v
    if isinstance(v, Edge):
        return v.id
    if isinstance(v, str):
        return EdgeId(v)
    raise TypeError(f'Expected any of {{str,Edge,EdgeId}}, but got {type(v)}')
