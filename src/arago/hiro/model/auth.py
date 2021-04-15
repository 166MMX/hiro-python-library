from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping

# from arago.hiro.model.graph.vertex import VertexId
from arago.hiro.utils.datetime import timestamp_ms_to_datetime


@dataclass(frozen=True)
class ClientCredentials:
    id: str
    secret: str


@dataclass(frozen=True)
class AccountCredentials:
    username: str
    password: str


@dataclass(frozen=True)
class SessionCredentials:
    client: ClientCredentials
    account: AccountCredentials


@dataclass(frozen=True)
class AccessToken(ABC):
    value: str

    @property
    @abstractmethod
    def valid(self) -> bool:
        ...


class AccessTokenType(Enum):
    BEARER = 'Bearer'


@dataclass(frozen=True)
class ConstantAccessToken(AccessToken):
    @property
    def valid(self) -> bool:
        return True


@dataclass(frozen=True)
class PasswordAccessToken(AccessToken):
    application_id: str  # TODO VertexId of ogit.Auth:Application
    account_name: str
    account_id: str  # TODO VertexId of ogit.Auth:Account
    expires_at: int
    expires_at_datetime: datetime
    type: str  # TODO AccessTokenType(Enum)

    @classmethod
    def from_data(cls, data: Mapping[str, Any]) -> 'PasswordAccessToken':
        value = data['_TOKEN']
        application_id = data['_APPLICATION']
        account_name = data['_IDENTITY']
        account_id = data['_IDENTITY_ID']
        expires_at = data['expires-at']
        expires_at_datetime = timestamp_ms_to_datetime(expires_at)
        token_type = data['type']
        return cls(value, application_id, account_name, account_id, expires_at, expires_at_datetime, token_type)

    @property
    def valid(self) -> bool:
        return datetime.utcnow().replace(tzinfo=timezone.utc) < self.expires_at_datetime

#
# @dataclass(frozen=True)
# class PasswordAccessToken2(AccessToken):
#     application_id: VertexId  # TODO VertexId of ogit.Auth:Application
#     account_name: str
#     account_id: VertexId  # TODO VertexId of ogit.Auth:Account
#     expires_at: int
#     expires_at_datetime: datetime
#     type: str  # TODO AccessTokenType(Enum)
#
#     def __init__(
#             self,
#             data: Mapping[str, Any]
#     ) -> None:
#         object.__setattr__(self, 'value', data['_TOKEN'])
#         object.__setattr__(self, 'application_id', VertexId(data['_APPLICATION']))
#         object.__setattr__(self, 'account_name', str(data['_IDENTITY']))
#         object.__setattr__(self, 'account_id', VertexId(data['_IDENTITY_ID']))
#         object.__setattr__(self, 'expires_at', int(data['expires-at']))
#         object.__setattr__(self, 'expires_at_datetime', timestamp_ms_to_datetime(self.expires_at))
#         object.__setattr__(self, 'token_type', str(data['type']))
