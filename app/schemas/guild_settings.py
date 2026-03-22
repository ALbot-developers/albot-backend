from typing import Optional, Literal

from pydantic import BaseModel, Field


class GuildSettingsUpdate(BaseModel):
    lang: Optional[str] = None
    character_limit: Optional[int] = Field(default=None, le=4000, ge=0,
                                           description="Maximum character limit for messages")
    speech_speed: Optional[float] = Field(default=None, ge=0.1, le=4.0, description="Speech speed multiplier")
    read_name: Optional[bool] = None
    custom_voice: Optional[str] = None
    translate: Optional[bool] = None
    read_name_on_join: Optional[bool] = None
    read_name_on_leave: Optional[bool] = None
    read_guild: Optional[bool] = None
    read_not_joined_users: Optional[bool] = None
    audio_api: Optional[Literal["gtts", "openai"]] = None
