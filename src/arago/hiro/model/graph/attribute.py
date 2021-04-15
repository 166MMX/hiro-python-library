from dataclasses import dataclass
from enum import unique, Enum
from typing import Mapping, ClassVar, MutableMapping, Any, Iterator, Union, TypeVar, Optional, overload

from arago.ogit import OgitAttribute
from arago.ogit.utils import named_aliases, add_aliases
from arago.ontology import OntologyAttribute, QName, NamedEnum, Attribute


@dataclass(frozen=True)
class VirtualSystemAttribute(Attribute):
    name: QName


# noinspection SpellCheckingInspection
class VirtualAttribute(NamedEnum):
    value: Union[VirtualSystemAttribute, OntologyAttribute]
    OGIT__EDGE_ID = OgitAttribute.OGIT__EDGE_ID.value
    OGIT__GRAPH_TYPE = OgitAttribute.OGIT__GRAPH_TYPE.value
    OGIT__IS_DELETED = OgitAttribute.OGIT__IS_DELETED.value
    OGIT__OUT_TYPE = VirtualSystemAttribute(QName('ogit:_out-type'))
    OGIT__OUT_ID = VirtualSystemAttribute(QName('ogit:_out-id'))
    OGIT__IN_TYPE = VirtualSystemAttribute(QName('ogit:_in-type'))
    OGIT__IN_ID = VirtualSystemAttribute(QName('ogit:_in-id'))

    OGIT__ON_BEHALF_CREATOR = VirtualSystemAttribute(QName('ogit:_on-behalf-creator'))
    OGIT__ON_BEHALF_MODIFIED_BY = VirtualSystemAttribute(QName('ogit:_on-behalf-modified-by'))

    OGIT__RESOURCE_ID = VirtualSystemAttribute(QName('ogit:_resource-id'))
    OGIT__C_SIZE = VirtualSystemAttribute(QName('ogit:_c-size'))
    OGIT__C_TYPE = VirtualSystemAttribute(QName('ogit:_c-type'))

    def __repr__(self):
        return "%s.%s" % (self.__class__.__name__, self._name_)

    def __str__(self):
        return self.value.name.uri


add_aliases(VirtualAttribute, named_aliases)


class SystemAttribute(NamedEnum):
    value: OntologyAttribute
    OGIT__EDGE_ID = VirtualAttribute.OGIT__EDGE_ID.value
    OGIT__GRAPH_TYPE = VirtualAttribute.OGIT__GRAPH_TYPE.value
    OGIT__IS_DELETED = VirtualAttribute.OGIT__IS_DELETED.value

    OGIT__ID = OgitAttribute.OGIT__ID.value
    OGIT__XID = OgitAttribute.OGIT__XID.value
    OGIT__TYPE = OgitAttribute.OGIT__TYPE.value
    OGIT__V = OgitAttribute.OGIT__V.value
    OGIT__V_ID = OgitAttribute.OGIT__V_ID.value

    OGIT__CREATED_ON = OgitAttribute.OGIT__CREATED_ON.value
    OGIT__CREATOR = OgitAttribute.OGIT__CREATOR.value
    OGIT__CREATOR_APP = OgitAttribute.OGIT__CREATOR_APP.value
    OGIT__MODIFIED_BY = OgitAttribute.OGIT__MODIFIED_BY.value
    OGIT__MODIFIED_BY_APP = OgitAttribute.OGIT__MODIFIED_BY_APP.value
    OGIT__MODIFIED_ON = OgitAttribute.OGIT__MODIFIED_ON.value
    OGIT__DELETED_BY = OgitAttribute.OGIT__DELETED_BY.value
    OGIT__DELETED_BY_APP = OgitAttribute.OGIT__DELETED_BY_APP.value
    OGIT__DELETED_ON = OgitAttribute.OGIT__DELETED_ON.value

    OGIT__OWNER = OgitAttribute.OGIT__OWNER.value
    OGIT__READER = OgitAttribute.OGIT__READER.value
    OGIT__ORGANIZATION = OgitAttribute.OGIT__ORGANIZATION.value

    OGIT__CONTENT = OgitAttribute.OGIT__CONTENT.value
    OGIT__TAGS = OgitAttribute.OGIT__TAGS.value

    OGIT__C_ID = OgitAttribute.OGIT__C_ID.value
    OGIT__SCOPE = OgitAttribute.OGIT__SCOPE.value
    OGIT__SOURCE = OgitAttribute.OGIT__SOURCE.value
    OGIT__VERSION = OgitAttribute.OGIT__VERSION.value

    def __repr__(self):
        return "%s.%s" % (self.__class__.__name__, self._name_)

    def __str__(self):
        return self.value.name.uri


add_aliases(SystemAttribute, named_aliases)


class ReadOnlyAttribute(NamedEnum):
    value: Union[VirtualSystemAttribute, OntologyAttribute]
    OGIT__GRAPH_TYPE = VirtualAttribute.OGIT__GRAPH_TYPE.value
    OGIT__EDGE_ID = VirtualAttribute.OGIT__EDGE_ID.value
    OGIT__IS_DELETED = VirtualAttribute.OGIT__IS_DELETED.value
    OGIT__OUT_TYPE = VirtualAttribute.OGIT__OUT_TYPE.value
    OGIT__OUT_ID = VirtualAttribute.OGIT__OUT_ID.value
    OGIT__IN_TYPE = VirtualAttribute.OGIT__IN_TYPE.value
    OGIT__IN_ID = VirtualAttribute.OGIT__IN_ID.value

    OGIT__ID = SystemAttribute.OGIT__ID.value
    OGIT__V = SystemAttribute.OGIT__V.value
    OGIT__V_ID = SystemAttribute.OGIT__V_ID.value
    OGIT__CREATED_ON = SystemAttribute.OGIT__CREATED_ON.value
    OGIT__CREATOR = SystemAttribute.OGIT__CREATOR.value
    OGIT__CREATOR_APP = SystemAttribute.OGIT__CREATOR_APP.value
    OGIT__MODIFIED_BY = SystemAttribute.OGIT__MODIFIED_BY.value
    OGIT__MODIFIED_BY_APP = SystemAttribute.OGIT__MODIFIED_BY_APP.value
    OGIT__MODIFIED_ON = SystemAttribute.OGIT__MODIFIED_ON.value
    OGIT__DELETED_BY = SystemAttribute.OGIT__DELETED_BY.value
    OGIT__DELETED_BY_APP = SystemAttribute.OGIT__DELETED_BY_APP.value
    OGIT__DELETED_ON = SystemAttribute.OGIT__DELETED_ON.value

    def __repr__(self):
        return "%s.%s" % (self.__class__.__name__, self._name_)

    def __str__(self):
        return self.value.name.uri


add_aliases(ReadOnlyAttribute, named_aliases)


class FinalAttribute(NamedEnum):
    value: Union[VirtualSystemAttribute, OntologyAttribute]
    OGIT__GRAPH_TYPE = VirtualAttribute.OGIT__GRAPH_TYPE.value
    OGIT__EDGE_ID = VirtualAttribute.OGIT__EDGE_ID.value
    OGIT__OUT_TYPE = VirtualAttribute.OGIT__OUT_TYPE.value
    OGIT__OUT_ID = VirtualAttribute.OGIT__OUT_ID.value
    OGIT__IN_TYPE = VirtualAttribute.OGIT__IN_TYPE.value
    OGIT__IN_ID = VirtualAttribute.OGIT__IN_ID.value

    OGIT__ID = SystemAttribute.OGIT__ID.value
    OGIT__CREATED_ON = SystemAttribute.OGIT__CREATED_ON.value
    OGIT__CREATOR = SystemAttribute.OGIT__CREATOR.value
    OGIT__CREATOR_APP = SystemAttribute.OGIT__CREATOR_APP.value
    OGIT__DELETED_BY = SystemAttribute.OGIT__DELETED_BY.value
    OGIT__DELETED_BY_APP = SystemAttribute.OGIT__DELETED_BY_APP.value
    OGIT__DELETED_ON = SystemAttribute.OGIT__DELETED_ON.value

    OGIT__XID = OgitAttribute.OGIT__XID.value
    OGIT__TYPE = OgitAttribute.OGIT__TYPE.value

    def __repr__(self):
        return "%s.%s" % (self.__class__.__name__, self._name_)

    def __str__(self):
        return self.value.name.uri


add_aliases(FinalAttribute, named_aliases)


@dataclass(frozen=True)
class FreeAttribute(Attribute, Mapping[str, 'FreeAttribute']):
    __instances: ClassVar[MutableMapping[str, 'FreeAttribute']] = dict()

    def __new__(cls, name: str) -> 'FreeAttribute':
        if name.startswith(':'):
            colon_name = name
        elif name.startswith('/'):
            colon_name = ':' + name[1:]
        else:
            raise ValueError(name)  # TODO
        if colon_name in FreeAttribute.__instances:
            return FreeAttribute.__instances[colon_name]

        instance = super().__new__(cls)
        FreeAttribute.__instances[name] = instance
        return instance

    def __init__(self, name: str) -> None:
        if name.startswith(':'):
            prefixed_name = name
        elif name.startswith('/'):
            prefixed_name = ':' + name[1:]
        else:
            raise ValueError(name)  # TODO
        super().__init__(QName(prefixed_name))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, FreeAttribute):
            return False
        return self.name == o.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __getitem__(self, k: object) -> 'FreeAttribute':
        pass

    def __len__(self) -> int:
        return len(FreeAttribute.__instances)

    def __iter__(self) -> Iterator[QName]:
        return iter(FreeAttribute.__instances)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name.full_name)

    def __str__(self):
        return self.name.uri


ATTRIBUTE_T_co = TypeVar('ATTRIBUTE_T_co', bound=Attribute, covariant=True)
ATTRIBUTE_T = Union[
    OgitAttribute,
    VirtualAttribute,
    SystemAttribute,
    ReadOnlyAttribute,
    FinalAttribute,
    ATTRIBUTE_T_co,
    str]


@overload
def to_attribute(v: VirtualAttribute) -> VirtualSystemAttribute: ...


@overload
def to_attribute(v: OgitAttribute) -> OntologyAttribute: ...


@overload
def to_attribute(v: SystemAttribute) -> Union[OntologyAttribute, VirtualSystemAttribute]: ...


@overload
def to_attribute(v: ReadOnlyAttribute) -> Union[OntologyAttribute, VirtualSystemAttribute]: ...


@overload
def to_attribute(v: FinalAttribute) -> Union[OntologyAttribute, VirtualSystemAttribute]: ...


@overload
def to_attribute(v: OntologyAttribute) -> OntologyAttribute: ...


@overload
def to_attribute(v: VirtualSystemAttribute) -> VirtualSystemAttribute: ...


@overload
def to_attribute(v: FreeAttribute) -> FreeAttribute: ...


@overload
def to_attribute(v: Attribute) -> Union[OntologyAttribute, VirtualSystemAttribute, FreeAttribute]: ...


@overload
def to_attribute(v: str) -> Union[OntologyAttribute, VirtualSystemAttribute, FreeAttribute]: ...


def to_attribute(v: Any) -> Union[OntologyAttribute, VirtualSystemAttribute, FreeAttribute]:
    if isinstance(v, (
            OgitAttribute,
            VirtualAttribute,
            SystemAttribute,
            ReadOnlyAttribute,
            FinalAttribute
    )):
        return v.value
    elif isinstance(v, (
            OntologyAttribute,
            VirtualSystemAttribute,
            FreeAttribute
    )):
        return v
    elif not isinstance(v, str):
        raise TypeError(type(v))
    elif v in VirtualAttribute.__members__:
        m: VirtualAttribute = VirtualAttribute[v]
        return m.value
    elif v.startswith('ogit/_') or v.startswith('ogit:_'):
        if v in OgitAttribute.__members__:
            m: OgitAttribute = OgitAttribute[v]
            return m.value
        raise ValueError(f'Unknown system attribute: {v!r}')
    elif v.startswith('ogit/') or v.startswith('ogit:'):
        if v in OgitAttribute.__members__:
            m: OgitAttribute = OgitAttribute[v]
            return m.value
        raise ValueError(f'Unknown OGIT attribute: {v!r}')
    elif v.startswith('/') or v.startswith(':'):
        return FreeAttribute(v)
    raise ValueError(f'''Not a valid attribute: {v!r} (FreeAttributes require a '/' prefix)''')


def attribute_to_str(attr: ATTRIBUTE_T) -> str:
    if isinstance(attr, Attribute):
        return attr.name.uri
    elif isinstance(attr, (OgitAttribute, VirtualAttribute, SystemAttribute, ReadOnlyAttribute, FinalAttribute)):
        return attr.value.name.uri
    elif isinstance(attr, str):
        return attr
    else:
        raise TypeError(type(attr))


@unique
class GraphType(Enum):
    value: str
    VERTEX = 'vertex'
    EDGE = 'edge'


GRAPH_TYPE_co = TypeVar('GRAPH_TYPE_co', bound=GraphType, covariant=True)
GRAPH_TYPE_T = Union[GRAPH_TYPE_co, str]


def to_graph_type(v: Optional[GRAPH_TYPE_T]) -> Optional[GraphType]:
    if v is None:
        return None
    if isinstance(v, GraphType):
        return v
    if isinstance(v, str):
        return GraphType[v]
    raise TypeError(f'Expected any of {{str,GraphType}}, but got {type(v)}')
