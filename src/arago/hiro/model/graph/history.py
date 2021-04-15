import enum
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from arago.hiro.model.graph.vertex import Vertex, VertexId, VersionId
from arago.ontology import Attribute


class HistoryFormat(enum.Enum):
    FULL = 'full'
    ELEMENT = 'element'
    DIFF = 'diff'


class HistoryAction(enum.Enum):
    UPDATE = enum.auto()
    CREATE = enum.auto()
    DELETE = enum.auto()


@dataclass(frozen=True)
class HistoryMeta:
    id: VertexId
    nanotime: int  # TODO figure out how to recombine
    timestamp: int
    vid: VersionId
    version: int


@dataclass(frozen=True)
class HistoryEntry:
    identity: VertexId
    action: HistoryAction
    data: Vertex  # TODO freeze vertex
    meta: HistoryMeta


@dataclass(frozen=True)
class HistoryDiff:
    added: MappingProxyType[Attribute, Any]
    removed: MappingProxyType[Attribute, Any]
    replaced: MappingProxyType[Attribute, Any]
