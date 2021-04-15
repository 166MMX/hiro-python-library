from collections import UserDict
from typing import Any, Optional, Mapping as Mapping, Dict

from arago.hiro.model.graph.attribute import ATTRIBUTE_T, to_attribute, SystemAttribute, \
    ReadOnlyAttribute, FinalAttribute, VirtualAttribute
from arago.ogit import OgitAttribute
from arago.ontology import Attribute


class GraphDict(UserDict[ATTRIBUTE_T, Any]):
    def __init__(self, data: Optional[Mapping[ATTRIBUTE_T, Any]] = None, **kwargs: Any) -> None:
        d = {}
        if isinstance(data, Mapping):
            for k, v in data.items():
                if isinstance(k, Attribute):
                    d[k] = v
                elif isinstance(k, (
                        OgitAttribute, VirtualAttribute, SystemAttribute, ReadOnlyAttribute, FinalAttribute)):
                    d[k.value] = v
                elif isinstance(k, str):
                    a = to_attribute(k)
                    d[a] = v
                else:
                    raise TypeError(type(k))
        for k, v in kwargs.items():
            a = to_attribute(k)
            d[a] = v
        super().__init__(d)

    def __getitem__(self, key: ATTRIBUTE_T) -> Any:
        if isinstance(key, Attribute):
            return super().__getitem__(key)
        elif isinstance(key, (OgitAttribute, VirtualAttribute, SystemAttribute, ReadOnlyAttribute, FinalAttribute)):
            return super().__getitem__(key.value)
        else:
            a = to_attribute(key)
            return super().__getitem__(a)

    def __setitem__(self, key: ATTRIBUTE_T, item: Any) -> None:
        if isinstance(key, Attribute):
            super().__setitem__(key, item)
        elif isinstance(key, (OgitAttribute, VirtualAttribute, SystemAttribute, ReadOnlyAttribute, FinalAttribute)):
            super().__setitem__(key.value, item)
        else:
            a = to_attribute(key)
            super().__setitem__(a, item)

    def __delitem__(self, key: ATTRIBUTE_T) -> None:
        if isinstance(key, Attribute):
            super().__delitem__(key)
        elif isinstance(key, (OgitAttribute, VirtualAttribute, SystemAttribute, ReadOnlyAttribute, FinalAttribute)):
            super().__delitem__(key.value)
        else:
            a = to_attribute(key)
            super().__delitem__(a)

    def __contains__(self, key: object) -> bool:
        if isinstance(key, Attribute):
            return super().__contains__(key)
        elif isinstance(key, (OgitAttribute, VirtualAttribute, SystemAttribute, ReadOnlyAttribute, FinalAttribute)):
            return super().__contains__(key.value)
        elif isinstance(key, str):
            a = to_attribute(key)
            return super().__contains__(a)
        else:
            raise TypeError(type(key))

    def to_dict(self) -> Dict[str, Any]:
        r = dict()
        for k, v in self.data.items():
            r[k.name.uri] = v
        return r

# class TypedGraphDict(GraphDict):
#     @overload
#     def __getitem__(self, key: Literal[OgitAttribute.OGIT__CREATED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[OgitAttribute.OGIT__MODIFIED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[OgitAttribute.OGIT__DELETED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[OgitAttribute.OGIT__XID]) -> Union[ExternalVertexId, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[OgitAttribute.OGIT__ID]) -> Union[VertexId, EdgeId, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[OgitAttribute.OGIT__TYPE]) -> Union[OntologyEntity, OntologyVerb, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[OgitAttribute.OGIT__GRAPH_TYPE]) -> GraphType:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[VirtualAttribute.OGIT__GRAPH_TYPE]) -> GraphType:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[ReadOnlyAttribute.OGIT__CREATED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[ReadOnlyAttribute.OGIT__MODIFIED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[ReadOnlyAttribute.OGIT__DELETED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[ReadOnlyAttribute.OGIT__ID]) -> Union[VertexId, EdgeId, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[ReadOnlyAttribute.OGIT__GRAPH_TYPE]) -> GraphType:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[FinalAttribute.OGIT__CREATED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[FinalAttribute.OGIT__DELETED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[FinalAttribute.OGIT__XID]) -> Union[ExternalVertexId, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[FinalAttribute.OGIT__ID]) -> Union[VertexId, EdgeId, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[FinalAttribute.OGIT__TYPE]) -> Union[OntologyEntity, OntologyVerb, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[FinalAttribute.OGIT__GRAPH_TYPE]) -> GraphType:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[SystemAttribute.OGIT__CREATED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[SystemAttribute.OGIT__MODIFIED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[SystemAttribute.OGIT__DELETED_ON]) -> Union[datetime]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[SystemAttribute.OGIT__XID]) -> Union[ExternalVertexId, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[SystemAttribute.OGIT__ID]) -> Union[VertexId, EdgeId, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[SystemAttribute.OGIT__TYPE]) -> Union[OntologyEntity, OntologyVerb, str]:
#         ...
#
#     @overload
#     def __getitem__(self, key: Literal[SystemAttribute.OGIT__GRAPH_TYPE]) -> GraphType:
#         ...
#
#     def __getitem__(self, key: ATTRIBUTE_T) -> Any:
#         from arago.hiro.utils.cast import to_graph_type, to_vertex_type, to_verb, to_edge_id, to_vertex_id, \
#             to_vertex_xid, to_datetime
#         k: Attribute
#         v: Any
#         if isinstance(key, Attribute):
#             k = key
#             v = super().__getitem__(key)
#         else:
#             k = to_attribute(key)
#             v = super().__getitem__(k)
#         if k is SystemAttribute.OGIT__GRAPH_TYPE:
#             return to_graph_type(v)
#         elif k is SystemAttribute.OGIT__TYPE:
#             if SystemAttribute.OGIT__GRAPH_TYPE not in self:
#                 if isinstance(v, (OgitVerb, OgitEntity)):  # unpack OgitEnum
#                     return v.value
#                 else:
#                     return v
#                 # raise RuntimeError('Unable to upcast type without graph type hint')
#             graph_type = self[SystemAttribute.OGIT__GRAPH_TYPE]
#             if graph_type is GraphType.EDGE:
#                 return to_verb(v)
#             elif graph_type is GraphType.VERTEX:
#                 return to_vertex_type(v)
#             else:
#                 raise RuntimeError('Unreachable')
#         elif k == OgitAttribute.OGIT__ID:
#             if SystemAttribute.OGIT__GRAPH_TYPE not in self:
#                 return v
#                 # raise RuntimeError('Unable to upcast id without graph type hint')
#             graph_type = self[SystemAttribute.OGIT__GRAPH_TYPE]
#             if graph_type is GraphType.EDGE:
#                 return to_edge_id(v)
#             elif graph_type is GraphType.VERTEX:
#                 # vertex_type: OntologyEntity = self[SystemAttribute.OGIT__TYPE]
#                 return to_vertex_id(v)  # , vertex_type
#             else:
#                 raise RuntimeError('Unreachable')
#         elif k is OgitAttribute.OGIT__XID:
#             return to_vertex_xid(v)
#         elif k in {
#             OgitAttribute.OGIT__CREATED_ON,
#             OgitAttribute.OGIT__MODIFIED_ON,
#             OgitAttribute.OGIT__DELETED_ON,
#         }:
#             return to_datetime(v)
