from typing import NamedTuple, Literal

from arago.hiro.model.graph.attribute import ATTRIBUTE_T


class Order(NamedTuple):
    field: ATTRIBUTE_T
    dir: Literal['asc', 'dec']

# TODO impl escape elastic search query
