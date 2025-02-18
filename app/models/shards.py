from pydantic import BaseModel


class ProvisioningConfig(BaseModel):
    shard_count: int
    shard_id: int
    discord_token: str
    sentry_dsn: str
    tts_key: str
    heartbeat_token: str
