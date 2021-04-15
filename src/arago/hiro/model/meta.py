from dataclasses import dataclass, field
from enum import unique, Enum, auto
from typing import Optional


@unique
class Lifecycle(Enum):
    EXPERIMENTAL = auto()
    STABLE = auto()
    DEPRECATED = auto()
    REMOVED = auto()

    def __repr__(self):
        # https://docs.python.org/3/library/enum.html#omitting-values
        return '<%s.%s>' % (self.__class__.__name__, self.name)


@unique
class Support(Enum):
    SUPPORTED = auto()
    UNSUPPORTED = auto()

    def __repr__(self):
        # https://docs.python.org/3/library/enum.html#omitting-values
        return '<%s.%s>' % (self.__class__.__name__, self.name)


@dataclass(frozen=True)
class Api:
    endpoint: str
    docs: Optional[str] = field(default=None)
    lifecycle: Optional[Lifecycle] = field(default=None)
    protocols: Optional[str] = field(default=None)
    specs: Optional[str] = field(default=None)
    support: Optional[Support] = field(default=None)
    version: Optional[str] = field(default=None)
    note: Optional[str] = field(default=None)
