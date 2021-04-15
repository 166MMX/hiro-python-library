from typing import FrozenSet, Any, Optional

from arago.hiro.utils.datetime import timestamp_ms_to_datetime

_TRUE: FrozenSet = frozenset({'true', 't', 'yes', 'y', '1'})
_FALSE: FrozenSet = frozenset({'false', 'f', 'no', 'n', '0'})


def to_bool(v: Any) -> Optional[bool]:
    if isinstance(v, str) and bool(v):
        v = v.lower()
        if v in _TRUE:
            return True
        elif v in _FALSE:
            return False
        else:
            return None
    else:
        return bool(v)


to_datetime = timestamp_ms_to_datetime

# def to_virt_attribute(v: Union[VirtualAttribute, VirtualSystemAttribute, str]) -> VirtualSystemAttribute:
#     if isinstance(v, VirtualSystemAttribute):
#         return v
#     elif isinstance(v, VirtualAttribute):
#         return v.value
#     elif isinstance(v, str):
#         try:
#             v: VirtualAttribute = VirtualAttribute[v]
#         except KeyError:
#             raise ValueError(v) from None
#         return v.value
#     else:
#         raise TypeError(type(v))

# def to_onto_attribute(v: Union[OgitAttribute, OntologyAttribute, str]) -> OntologyAttribute:
#     if isinstance(v, OntologyAttribute):
#         return v
#     elif isinstance(v, OgitAttribute):
#         return v.value
#     elif isinstance(v, str):
#         try:
#             v: OgitAttribute = OgitAttribute[v]
#         except KeyError:
#             raise ValueError(v) from None
#         return v.value
#     else:
#         raise TypeError(type(v))


#     def __contains__(self, k: OgitAttribute) -> bool:
#     def __contains__(self, k: VirtualAttribute) -> bool:
#     def __contains__(self, k: SystemAttribute) -> bool:
#     def __contains__(self, k: ReadOnlyAttribute) -> bool:
#     def __contains__(self, k: FinalAttribute) -> bool:
#     def __contains__(self, k: Attribute) -> bool:
#     def __contains__(self, k: str) -> bool:
