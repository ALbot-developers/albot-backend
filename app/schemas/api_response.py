from pydantic import BaseModel

from app.models.character_usage import CharacterUsages
from app.models.shards import ProvisioningConfig
from app.models.trusted_roles import TrustedRoles
from app.schemas.api_data import ConnectionStateData, DictData, SubscriptionsData, MetricsData, GuildSettingsData, \
    ShardConnectionCommandsData, ShardsListData, UserInfoData, GuildsListData, GuildInfoData, URLData
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
    data: GuildSettingsData


class ListSubscriptionsAPIResponse(BaseModel):
    message: str
    data: SubscriptionsData


# memo: trusted rolesのみDBのmodelをそのまま返す。既にenabledとrole_idsで分かれているため。
class TrustedRolesResponse(BaseModel):
    message: str
    data: TrustedRoles


class MetricsAPIResponse(BaseModel):
    message: str
    data: MetricsData


class URLAPIResponse(BaseModel):
    message: str
    data: URLData


class ShardProvisionAPIResponse(BaseModel):
    message: str
    data: ProvisioningConfig


class ShardConnectionCommandsAPIResponse(BaseModel):
    message: str
    data: ShardConnectionCommandsData


class ShardsListAPIResponse(BaseModel):
    message: str
    data: ShardsListData


class UserInfoAPIResponse(BaseModel):
    message: str
    data: UserInfoData


class GuildsListAPIResponse(BaseModel):
    message: str
    data: GuildsListData


class GuildInfoAPIResponse(BaseModel):
    message: str
    data: GuildInfoData
