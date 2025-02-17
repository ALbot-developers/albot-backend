from pydantic import create_model, Field

from app.models.settings import GuildSettings
from app.models.subscription import Subscription
from app.schemas.connection_state import ConnectionState
from app.schemas.metrics import Metrics

# todo: connection_state(単数形)に修正
ConnectionStateData = create_model("ConnectionStateDataModel", connection_states=(ConnectionState, ...))
DictData = create_model("DictDataModel", dict_=(dict, Field(..., alias="dict")))
GuildSettingsData = create_model("GuildSettingsDataModel", settings=(GuildSettings, ...))
SubscriptionsData = create_model("SubscriptionsDataModel", subscriptions=(list[Subscription], ...))
MetricsData = create_model("MetricsDataModel", metrics=(Metrics, ...))
