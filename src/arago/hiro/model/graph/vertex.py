from dataclasses import dataclass, field
from datetime import datetime
from enum import Flag, auto
from typing import Optional, Set, Dict, Any, Mapping, Union, Iterator, TYPE_CHECKING, TypeVar

from arago.hiro.client.rest_base_client import HiroRestBaseClient
from arago.ogit import OgitAttribute, OgitEntity as OgitEntity
from arago.ontology import OntologyEntity, Attribute
from .attribute import GraphType, ATTRIBUTE_T, to_attribute
from .cuid import Cuid
from .dict import GraphDict
from ...utils.cast import to_bool
from ...utils.datetime import timestamp_ms_to_datetime, datetime_to_timestamp_ms

if TYPE_CHECKING:
    from arago.hiro.client.client import HiroClient


class VertexId(Cuid):
    __instances: Dict[str, 'VertexId'] = dict()

    def __new__(cls, value: str) -> Any:
        instance = VertexId.__instances.get(value, None)
        if instance is not None:
            return instance

        instance = super().__new__(cls, value)
        VertexId.__instances[value] = instance
        return instance


class ExternalVertexId(str):
    pass


def b62decode(value: str) -> int:
    result = 0
    for c in value:
        # noinspection SpellCheckingInspection
        result = 62 * result + '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(c)
    return result


class VersionId(str):
    def timestamp(self) -> datetime:
        return timestamp_ms_to_datetime(int(self[:self.find('-')]))

    def random(self) -> int:  # 6 chars
        return b62decode(self[self.find('-') + 1:])


class VertexFlag(Flag):
    DRAFT = auto()
    HAS_GRAPH_TYPE = auto()


HIRO_BASE_CLIENT_T_co = TypeVar('HIRO_BASE_CLIENT_T_co', bound=HiroRestBaseClient, covariant=True)


@dataclass
class Vertex:  # MutableMapping
    id: Optional[VertexId] = field()
    xid: Optional[ExternalVertexId] = field()
    _orig_xid: Optional[ExternalVertexId] = field(repr=False, compare=False)
    type: Optional[OntologyEntity] = field()
    v: Optional[int] = field()
    v_id: Optional[VersionId] = field()

    created_by_app: Optional[VertexId] = field()
    created_by: Optional[str] = field()
    created_on: Optional[datetime] = field()
    modified_by_app: Optional[VertexId] = field()
    modified_by: Optional[str] = field()
    modified_on: Optional[datetime] = field()
    deleted_by_app: Optional[VertexId] = field()
    deleted_by: Optional[str] = field()
    deleted_on: Optional[datetime] = field()
    is_deleted: bool = field()

    owner: Optional[str] = field()
    _orig_owner: Optional[str] = field(repr=False, compare=False)
    organization: Optional[str] = field()
    _orig_organization: Optional[str] = field(repr=False, compare=False)
    reader: Optional[str] = field()
    _orig_reader: Optional[str] = field(repr=False, compare=False)
    scope: Optional[VertexId] = field()

    content: Optional[str] = field()
    _orig_content: Optional[str] = field(repr=False, compare=False)
    tags: Set[str] = field()
    _orig_tags: Set[str] = field(repr=False, compare=False)
    version: Optional[str] = field()

    _draft: bool = field(repr=False, compare=False)
    _has_graph_type: bool = field(repr=False)
    client: Optional['HiroClient'] = field(repr=False, compare=False)
    attributes: GraphDict = field()

    def __init__(
            self,
            data: Optional[Mapping[str, Any]] = None,
            client: Optional[HIRO_BASE_CLIENT_T_co] = None,
            draft: bool = True
    ) -> None:
        super().__init__()
        if isinstance(client, HiroRestBaseClient):
            self.client = client.root
        self._draft = draft

        if data is not None:
            m = GraphDict(data)

            k = OgitAttribute.OGIT__GRAPH_TYPE  # virtual attribute
            if k in m:
                graph_type = GraphType(m[k])
                if graph_type is not GraphType.VERTEX:
                    raise RuntimeError()
            else:
                graph_type = None

            self._has_graph_type = graph_type is not None

            k = OgitAttribute.OGIT__ID
            if k in m:
                self.id = VertexId(m[k])
                del m[k]
            else:
                self.id = None
            k = OgitAttribute.OGIT__XID
            if k in m:
                self.xid = ExternalVertexId(m[k])
                del m[k]
            else:
                self.xid = None
            self._orig_xid = self.xid
            k = OgitAttribute.OGIT__TYPE
            if k in m:
                entity = to_vertex_type(m[k])
                self.type = entity
                del m[k]
            else:
                self.type = None
            k = OgitAttribute.OGIT__V
            if k in m:
                self.v = int(m[k])
                del m[k]
            else:
                self.v = None
            k = OgitAttribute.OGIT__V_ID
            if k in m:
                self.v_id = VersionId(m[k])
                del m[k]
            else:
                self.v_id = None

            k = OgitAttribute.OGIT__CREATOR_APP
            if k in m:
                self.created_by_app = VertexId(m[k])
                del m[k]
            else:
                self.created_by_app = None
            k = OgitAttribute.OGIT__CREATOR
            if k in m:
                self.created_by = m[k]
                del m[k]
            else:
                self.created_by = None
            k = OgitAttribute.OGIT__CREATED_ON
            if k in m:
                self.created_on = timestamp_ms_to_datetime(m[k])
                del m[k]
            else:
                self.created_on = None

            k = OgitAttribute.OGIT__MODIFIED_BY_APP
            if k in m:
                self.modified_by_app = VertexId(m[k])
                del m[k]
            else:
                self.modified_by_app = None
            k = OgitAttribute.OGIT__MODIFIED_BY
            if k in m:
                self.modified_by = m[k]
                del m[k]
            else:
                self.modified_by = None
            k = OgitAttribute.OGIT__MODIFIED_ON
            if k in m:
                self.modified_on = timestamp_ms_to_datetime(m[k])
                del m[k]
            else:
                self.modified_on = None

            k = OgitAttribute.OGIT__DELETED_BY_APP
            if k in m:
                self.deleted_by_app = VertexId(m[k])
                del m[k]
            else:
                self.deleted_by_app = None
            k = OgitAttribute.OGIT__DELETED_BY
            if k in m:
                self.deleted_by = m[k]
                del m[k]
            else:
                self.deleted_by = None
            k = OgitAttribute.OGIT__DELETED_ON
            if k in m:
                self.deleted_on = timestamp_ms_to_datetime(m[k])
                del m[k]
            else:
                self.deleted_on = None
            k = OgitAttribute.OGIT__IS_DELETED
            if k in m:
                self.is_deleted = to_bool(m[k])
                del m[k]
            else:
                self.is_deleted = False

            k = OgitAttribute.OGIT__OWNER
            if k in m:
                self.owner = m[k]
                del m[k]
            else:
                self.owner = None
            self._orig_owner = self.owner
            k = OgitAttribute.OGIT__ORGANIZATION
            if k in m:
                self.organization = m[k]
                del m[k]
            else:
                self.organization = None
            self._orig_organization = self.organization
            k = OgitAttribute.OGIT__READER
            if k in m:
                self.reader = m[k]
                del m[k]
            else:
                self.reader = None
            self._orig_reader = self.reader
            k = OgitAttribute.OGIT__SCOPE
            if k in m:
                self.scope = m[k]
                del m[k]
            else:
                self.scope = None

            k = OgitAttribute.OGIT__CONTENT
            if k in m:
                self.content = m[k]
                del m[k]
            else:
                self.content = None
            self._orig_content = self.content
            # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/index.html#requirements-of-namespace-ids-and-attributes
            k = OgitAttribute.OGIT__TAGS
            if k in m:
                v: str = m[k]
                self.tags = set(map(str.strip, v.split(',')))
                del m[k]
            else:
                self.tags = set()
            self._orig_tags = self.tags
            k = OgitAttribute.OGIT__VERSION
            if k in m:
                self.version = m[k]
                del m[k]
            else:
                self.version = None

            if graph_type:
                k = OgitAttribute.OGIT__GRAPH_TYPE  # virtual attribute
                del m[k]

            self.attributes = GraphDict()

            for k in m:
                if isinstance(k, Attribute):
                    self[k] = m[k]
                else:
                    raise KeyError(f'Unexpected key found: {k!r}')

            #             for k in m:
            #                 if not isinstance(k, str):
            #                     raise TypeError(f'Unexpected type of key found: {type(k)}')
            #                 if k.startswith('ogit/_'):
            #                     raise KeyError(f'Unexpected system attribute found: {k!r}')
            #                 elif k.startswith('ogit/'):
            #                     attribute: OgitAttribute = OgitAttribute[k]
            #                     k = attribute.value
            #                     v = m[k]
            #                     self[k] = v
            #                 elif k.startswith('/'):  # TODO free attributes
            #                     v = m[k]
            #                     a: FreeAttribute = FreeAttribute(k)
            #                     self[a] = v
            #                 else:
            #                     raise KeyError(f'Unexpected key found: {k!r}')

    def to_dict(self) -> Dict[str, Any]:
        r = dict()
        if self._has_graph_type:
            k = OgitAttribute.OGIT__GRAPH_TYPE.value.name.uri
            v = GraphType.VERTEX.value
            r[k] = v

        if self.id is not None:
            k = OgitAttribute.OGIT__ID.value.name.uri
            v = str(self.id)
            r[k] = v
        if self.xid is not None:
            k = OgitAttribute.OGIT__XID.value.name.uri
            v = str(self.xid)
            r[k] = v
        if self.type is not None:
            k = OgitAttribute.OGIT__TYPE.value.name.uri
            v = self.type.name.uri
            r[k] = v
        if self.v is not None:
            k = OgitAttribute.OGIT__V.value.name.uri
            v = int(self.v)
            r[k] = v
        if self.v_id is not None:
            k = OgitAttribute.OGIT__V_ID.value.name.uri
            v = str(self.v_id)
            r[k] = v

        if self.created_by_app is not None:
            k = OgitAttribute.OGIT__CREATOR_APP.value.name.uri
            v = str(self.created_by_app)
            r[k] = v
        if self.created_by is not None:
            k = OgitAttribute.OGIT__CREATOR.value.name.uri
            v = self.created_by
            r[k] = v
        if self.created_on is not None:
            k = OgitAttribute.OGIT__CREATED_ON.value.name.uri
            v = datetime_to_timestamp_ms(self.created_on)
            r[k] = v

        if self.modified_by_app is not None:
            k = OgitAttribute.OGIT__MODIFIED_BY_APP.value.name.uri
            v = str(self.modified_by_app)
            r[k] = v
        if self.modified_by is not None:
            k = OgitAttribute.OGIT__MODIFIED_BY.value.name.uri
            v = self.modified_by
            r[k] = v
        if self.modified_on is not None:
            k = OgitAttribute.OGIT__MODIFIED_ON.value.name.uri
            v = datetime_to_timestamp_ms(self.modified_on)
            r[k] = v

        if self.deleted_by_app is not None:
            k = OgitAttribute.OGIT__DELETED_BY_APP.value.name.uri
            v = str(self.deleted_by_app)
            r[k] = v
        if self.deleted_by is not None:
            k = OgitAttribute.OGIT__DELETED_BY.value.name.uri
            v = self.deleted_by
            r[k] = v
        if self.deleted_on is not None:
            k = OgitAttribute.OGIT__DELETED_ON.value.name.uri
            v = datetime_to_timestamp_ms(self.deleted_on)
            r[k] = v
        if self.is_deleted is not None:
            k = OgitAttribute.OGIT__IS_DELETED.value.name.uri
            v = self.is_deleted
            r[k] = v

        if self.owner is not None:
            k = OgitAttribute.OGIT__OWNER.value.name.uri
            v = self.owner
            r[k] = v
        if self.organization is not None:
            k = OgitAttribute.OGIT__ORGANIZATION.value.name.uri
            v = self.organization
            r[k] = v
        if self.reader is not None:
            k = OgitAttribute.OGIT__READER.value.name.uri
            v = self.reader
            r[k] = v
        if self.scope is not None:
            k = OgitAttribute.OGIT__SCOPE.value.name.uri
            v = self.scope
            r[k] = v

        if self.content is not None:
            k = OgitAttribute.OGIT__CONTENT.value.name.uri
            v = self.content
            r[k] = v
        # https://docs.hiro.arago.co/hiro/6.2.0/user/hiro-graph-api/index.html#requirements-of-namespace-ids-and-attributes
        if self.tags is not None and len(self.tags) > 0:
            k = OgitAttribute.OGIT__TAGS.value.name.uri
            v = ', '.join(self.tags)
            r[k] = v
        if self.version is not None:
            k = OgitAttribute.OGIT__VERSION.value.name.uri
            v = self.version
            r[k] = v

        a: Attribute
        for a, v in self.attributes.items():
            k = a.name.uri
            r[k] = v

        return r

    def __setitem__(self, k: Union[OgitAttribute, Attribute, str], v: Any) -> None:
        k = to_attribute(k)
        self.attributes[k] = v

    def __getitem__(self, k: Union[OgitAttribute, Attribute, str]) -> Any:
        k = to_attribute(k)
        return self.attributes[k]

    def __delitem__(self, k: Union[OgitAttribute, Attribute, str]) -> None:
        k = to_attribute(k)
        del self.attributes[k]

    def __contains__(self, o: object) -> bool:
        if isinstance(o, (OgitAttribute, Attribute, str)):
            o = to_attribute(o)
        return self.attributes.__contains__(o)

    def __len__(self) -> int:
        return len(self.attributes)

    def __iter__(self) -> Iterator:
        return iter(self.attributes)

    def resolve_id(
            self,
            vertex_id: Union[None, str, VertexId] = None
    ) -> Optional[VertexId]:
        return resolve_vertex_id(self, vertex_id)

    def resolve_type(
            self,
            vertex_type: Union[None, str, OgitEntity, OntologyEntity] = None
    ) -> Optional[OntologyEntity]:
        return resolve_vertex_type(self, vertex_type)

    def update(self, vertex: Union[Mapping[Union[Attribute, str], Any], 'Vertex']) -> 'Vertex':
        return self.client.model.graph.vertex.update(self.id, vertex)

    def delete(self) -> 'Vertex':
        return self.client.model.graph.vertex.delete(self.id)


VERTEX_T_co = TypeVar('VERTEX_T_co', bound=Vertex, covariant=True)
VERTEX_T = Union[
    VERTEX_T_co,
    Mapping[ATTRIBUTE_T, Any]
]
VERTEX_ID_T_co = TypeVar('VERTEX_ID_T_co', bound=VertexId, covariant=True)
VERTEX_ID_T = Union[
    VERTEX_ID_T_co,
    str
]
VERTEX_XID_T_co = TypeVar('VERTEX_XID_T_co', bound=ExternalVertexId, covariant=True)
VERTEX_XID_T = Union[
    VERTEX_XID_T_co,
    str
]
VERTEX_TYPE_T = Union[
    OntologyEntity,
    OgitEntity,
    str
]


def resolve_vertex_id(
        vertex: Optional[VERTEX_T],
        vertex_id: Optional[VERTEX_ID_T] = None
) -> Optional[VERTEX_ID_T_co]:
    if isinstance(vertex, Vertex) and vertex.id:
        value = vertex.id
        return to_vertex_id(value)
    if isinstance(vertex, Mapping):
        g_dict = GraphDict(vertex)
        if OgitAttribute.OGIT__ID in g_dict:
            value = g_dict[OgitAttribute.OGIT__ID]
            v_id = to_vertex_id(value)
            if v_id:
                return v_id

    if vertex_id is None:
        return None
    if isinstance(vertex_id, VertexId):
        return vertex_id
    if isinstance(vertex_id, str):
        return VertexId(vertex_id)

    raise TypeError(type(vertex_id))


def resolve_vertex_xid(
        vertex: Optional[VERTEX_T],
        vertex_xid: Optional[VERTEX_XID_T] = None
) -> Optional[VERTEX_XID_T_co]:
    if isinstance(vertex, Vertex) and vertex.xid:
        value = vertex.xid
        return to_vertex_xid(value)
    if isinstance(vertex, Mapping):
        g_dict = GraphDict(vertex)
        if OgitAttribute.OGIT__XID in g_dict:
            value = g_dict[OgitAttribute.OGIT__XID]
            v_xid = to_vertex_xid(value)
            if v_xid:
                return v_xid

    if vertex_xid is None:
        return None
    if isinstance(vertex_xid, ExternalVertexId):
        return vertex_xid
    if isinstance(vertex_xid, str):
        return ExternalVertexId(vertex_xid)

    raise TypeError(type(vertex_xid))


def resolve_vertex_type(
        vertex: Optional[VERTEX_T],
        vertex_type: Optional[VERTEX_TYPE_T] = None
) -> Optional[OntologyEntity]:
    if isinstance(vertex, Vertex) and vertex.type:
        value = vertex.type
        return to_vertex_type(value)
    if isinstance(vertex, Mapping):
        g_dict = GraphDict(vertex)
        if OgitAttribute.OGIT__TYPE in g_dict:
            value = g_dict[OgitAttribute.OGIT__TYPE]
            v_type = to_vertex_type(value)
            if v_type:
                return v_type

    if vertex_type is None:
        return None
    if isinstance(vertex_type, OntologyEntity):
        return vertex_type
    if isinstance(vertex_type, OgitEntity):
        return vertex_type.value
    if isinstance(vertex_type, str):
        entity: OgitEntity = OgitEntity[vertex_type]
        return entity.value

    raise TypeError(type(vertex_type))


def to_vertex_id(v: Optional[Union[VERTEX_T_co, VERTEX_ID_T]]) -> Optional[VERTEX_ID_T_co]:
    if v is None:
        return None
    if isinstance(v, Vertex):
        return to_vertex_id(v.id)
    if isinstance(v, VertexId):
        return v
    if isinstance(v, str):
        return VertexId(v)
    raise TypeError(f'Expected any of {{str,Vertex,VertexId}}, but got {type(v)}')


def to_vertex_xid(v: Optional[Union[VERTEX_T_co, VERTEX_XID_T]]) -> Optional[VERTEX_XID_T_co]:
    if v is None:
        return None
    if isinstance(v, Vertex):
        return to_vertex_xid(v.xid)
    if isinstance(v, ExternalVertexId):
        return v
    if isinstance(v, str):
        return ExternalVertexId(v)
    raise TypeError(f'Expected any of {{str,Vertex,ExternalVertexId}}, but got {type(v)}')


def to_vertex_type(v: Optional[Union[VERTEX_T_co, VERTEX_TYPE_T]]) -> Optional[OntologyEntity]:
    if v is None:
        return None
    if isinstance(v, Vertex):
        return to_vertex_type(v.type)
    if isinstance(v, OntologyEntity):
        return v
    if isinstance(v, OgitEntity):
        return v.value
    if isinstance(v, str):
        ogit_entity: OgitEntity = OgitEntity[v]
        return ogit_entity.value
    raise TypeError(f'Expected any of {{str,Vertex,OgitEntity,OntologyEntity}}, but got {type(v)}')


def vertex_id_to_str(vertex_id: VERTEX_ID_T) -> str:
    if isinstance(vertex_id, VertexId):
        return str(vertex_id)
    if isinstance(vertex_id, str):
        return vertex_id
    if isinstance(vertex_id, Vertex):
        return str(vertex_id.id)

    raise TypeError(type(vertex_id))


def external_id_to_str(external_id: VERTEX_XID_T) -> str:
    if isinstance(external_id, ExternalVertexId):
        return str(external_id)
    if isinstance(external_id, str):
        return external_id
    if isinstance(external_id, Vertex):
        return str(external_id.xid)

    raise TypeError(type(external_id))


def vertex_type_to_str(vertex_type: VERTEX_TYPE_T) -> str:
    if isinstance(vertex_type, OgitEntity):
        return str(vertex_type.value.name.uri)
    if isinstance(vertex_type, str):
        return vertex_type
    if isinstance(vertex_type, OntologyEntity):
        return str(vertex_type.name.uri)

    raise TypeError(type(vertex_type))
