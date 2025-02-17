from pydantic import BaseModel, create_model, Field

from app.models.character_usage import CharacterUsages
from app.models.settings import GuildSettings
from app.models.subscription import Subscription
from app.models.trusted_roles import TrustedRoles
from app.schemas.connection_command import ConnectionCommand
from app.schemas.connection_state import ConnectionState
from app.schemas.message_link_expand_pref import MessageLinkExpansionPreference


class PlainAPIResponse(BaseModel):
    message: str


class CharacterUsageAPIResponse(BaseModel):
    message: str
    data: CharacterUsages


class ConnectionCommandAPIResponse(BaseModel):
    message: str
    data: ConnectionCommand


# todo: connection_state(単数形)に修正
ConnectionStateData = create_model("ConnectionStateDataModel", connection_states=(ConnectionState, ...))


class ConnectionStateAPIResponse(BaseModel):
    message: str
    data: ConnectionStateData


DictData = create_model(
    "DictDataModel",
    dict_=(dict, Field(..., alias="dict"))
)


class DictAPIResponse(BaseModel):
    message: str
    data: DictData


# todo: expandからexpansionに命名を変更
class MessageLinkExpandAPIResponse(BaseModel):
    message: str
    data: MessageLinkExpansionPreference


GuildSettingsData = create_model("GuildSettingsDataModel", settings=(GuildSettings, ...))


class GuildSettingsAPIResponse(BaseModel):
    message: str
    data: dict


SubscriptionsData = create_model("SubscriptionsDataModel", subscriptions=(list[Subscription], ...))


class SubscriptionAPIResponse(BaseModel):
    message: str
    data: SubscriptionsData


# memo: trusted rolesのみDBのmodelをそのまま返す。既にenabledとrole_idsで分かれているため。
class TrustedRolesResponse(BaseModel):
    message: str
    data: TrustedRoles
