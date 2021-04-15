from datetime import date, datetime
from typing import overload, Literal, Union, Any, Mapping, Optional

from arago.hiro.model.graph.attribute import ATTRIBUTE_T
from arago.hiro.model.graph.dict import GraphDict
from arago.hiro.model.graph.vertex import Vertex, VERTEX_T_co, HIRO_BASE_CLIENT_T_co
from arago.hiro.utils.cast_b import to_vertex as cast_to_vertex
from arago.ogit import OgitAttribute, OgitEntity
from arago.ontology import Attribute


class OgitContract(Vertex):
    @overload
    def __getitem__(self, k: Literal[OgitAttribute.OGIT_VALID_FROM]) -> date:
        ...

    @overload
    def __getitem__(self, k: Literal[OgitAttribute.OGIT_VALID_TO]) -> date:
        ...

    def __getitem__(self, k: Union[OgitAttribute, Attribute, str]) -> Any:
        value = super().__getitem__(k)
        if k is OgitAttribute.OGIT_VALID_FROM or \
                k is OgitAttribute.OGIT_VALID_TO:
            return datetime.strptime(value, '%d.%m.%Y').date()
        return value


class OgitLicense(Vertex):
    @overload
    def __getitem__(self, k: Literal[OgitAttribute.OGIT_DEADLINE]) -> date:
        ...

    @overload
    def __getitem__(self, k: Literal[OgitAttribute.OGIT_EXPIRATION_DATE]) -> date:
        ...

    @overload
    def __getitem__(self, k: Literal[OgitAttribute.OGIT_VALID_FROM]) -> date:
        ...

    @overload
    def __getitem__(self, k: Literal[OgitAttribute.OGIT_VALID_TO]) -> date:
        ...

    def __getitem__(self, k: Union[OgitAttribute, Attribute, str]) -> Any:
        value = super().__getitem__(k)
        if k is k is OgitAttribute.OGIT_DEADLINE:
            return datetime.strptime(value, '%d.%m.%Y').date()
        if k is k is OgitAttribute.OGIT_EXPIRATION_DATE:
            return datetime.strptime(value, '%d.%m.%Y').date()
        if k is k is OgitAttribute.OGIT_VALID_FROM:
            return datetime.strptime(value, '%Y-%m-%d').date()
        if k is k is OgitAttribute.OGIT_VALID_TO:
            return datetime.strptime(value, '%Y-%m-%d').date()
        return value


class OgitAuthOrganization(Vertex):
    pass


class OgitAuthAccount(Vertex):
    pass


def to_vertex(
        data: Mapping[ATTRIBUTE_T, Any],
        client: Optional[HIRO_BASE_CLIENT_T_co] = None
) -> VERTEX_T_co:
    vertex_type = GraphDict(data).get(OgitAttribute.OGIT__TYPE)

    if vertex_type is OgitEntity.OGIT_CONTRACT:
        return OgitContract(data, client, False)
    if vertex_type is OgitEntity.OGIT_LICENSE:
        return OgitLicense(data, client, False)
    if vertex_type is OgitEntity.OGIT_AUTH_ORGANIZATION:
        return OgitAuthOrganization(data, client, False)
    if vertex_type is OgitEntity.OGIT_AUTH_ACCOUNT:
        return OgitAuthAccount(data, client, False)
    return cast_to_vertex(data, client)
