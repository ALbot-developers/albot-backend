from pydantic import create_model, Field

from app.external.discord.models import UserPIIResponse, PartialGuild
from app.models.settings import GuildSettings, DefaultSettings
from app.models.subscription import Subscription
from app.schemas.connection_state import ConnectionState
from app.schemas.metrics import Metrics

# todo: connection_state(単数形)に修正
ConnectionStateData = create_model("ConnectionStateDataModel", connection_states=(ConnectionState, ...))
DictData = create_model("DictDataModel", dict_=(dict, Field(..., alias="dict")))
GuildSettingsData = create_model("GuildSettingsDataModel", settings=(GuildSettings | DefaultSettings, ...))
SubscriptionsData = create_model("SubscriptionsDataModel", subscriptions=(list[Subscription], ...))
MetricsData = create_model("MetricsDataModel", metrics=(Metrics, ...))
ShardConnectionCommandsData = create_model("ShardConnectionCommandsDataModel", commands=(dict, ...))
ShardsListData = create_model("ShardsListDataModel", ids=(list[int], ...))
UserInfoData = create_model("UserInfoDataModel", info=(UserPIIResponse, ...))
GuildsListData = create_model("GuildsListDataModel", guilds=(list[PartialGuild], ...))
GuildInfoData = create_model("GuildInfoData", info=(PartialGuild, ...))
URLData = create_model("URLDataModel", url=(str, ...))
