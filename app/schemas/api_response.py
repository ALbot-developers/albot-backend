from pydantic import BaseModel

from app.models.character_usage import CharacterUsages
from app.models.trusted_roles import TrustedRoles
from app.schemas.api_data import ConnectionStateData, DictData, SubscriptionsData
from app.schemas.connection_command import ConnectionCommand
from app.schemas.message_link_expand_pref import MessageLinkExpansionPreference


class PlainAPIResponse(BaseModel):
    message: str


class CharacterUsageAPIResponse(BaseModel):
    message: str
    data: CharacterUsages


class ConnectionCommandAPIResponse(BaseModel):
    message: str
    data: ConnectionCommand


class ConnectionStateAPIResponse(BaseModel):
    message: str
    data: ConnectionStateData


class DictAPIResponse(BaseModel):
    message: str
    data: DictData


# todo: expandからexpansionに命名を変更
class MessageLinkExpandAPIResponse(BaseModel):
    message: str
    data: MessageLinkExpansionPreference


class GuildSettingsAPIResponse(BaseModel):
    message: str
    data: dict


class SubscriptionAPIResponse(BaseModel):
    message: str
    data: SubscriptionsData


# memo: trusted rolesのみDBのmodelをそのまま返す。既にenabledとrole_idsで分かれているため。
class TrustedRolesResponse(BaseModel):
    message: str
    data: TrustedRoles
