from pydantic import create_model, Field, BaseModel

from app.external.discord.models import UserPIIResponse, PartialGuild
from app.models.settings import GuildSettings, DefaultSettings
from app.models.subscription import Subscription
from app.schemas.connection_state import ConnectionState
from app.schemas.metrics import Metrics

# todo: connection_state(単数形)に修正
ConnectionStateData: type[BaseModel] = create_model("ConnectionStateDataModel", connection_states=(ConnectionState, ...))
DictData: type[BaseModel] = create_model("DictDataModel", dict_=(dict, Field(..., alias="dict")))
GuildSettingsData: type[BaseModel] = create_model("GuildSettingsDataModel", settings=(GuildSettings, ...))
SubscriptionsData: type[BaseModel] = create_model("SubscriptionsDataModel", subscriptions=(list[Subscription], ...))
MetricsData: type[BaseModel] = create_model("MetricsDataModel", metrics=(Metrics, ...))
ShardConnectionCommandsData: type[BaseModel] = create_model("ShardConnectionCommandsDataModel", commands=(dict, ...))
ShardsListData: type[BaseModel] = create_model("ShardsListDataModel", ids=(list[int], ...))
UserInfoData: type[BaseModel] = create_model("UserInfoDataModel", info=(UserPIIResponse, ...))
GuildsListData: type[BaseModel] = create_model("GuildsListDataModel", guilds=(list[PartialGuild], ...))
GuildInfoData: type[BaseModel] = create_model("GuildInfoData", info=(PartialGuild, ...))
URLData: type[BaseModel] = create_model("URLDataModel", url=(str, ...))
