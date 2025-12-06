from typing import Optional, Literal

from pydantic import BaseModel


class GuildSettingsUpdate(BaseModel):
    lang: Optional[str] = None
    character_limit: Optional[int] = None
    speech_speed: Optional[float] = None
    read_name: Optional[bool] = None
    custom_voice: Optional[str] = None
    translate: Optional[bool] = None
    read_name_on_join: Optional[bool] = None
    read_name_on_leave: Optional[bool] = None
    read_guild: Optional[bool] = None
    read_not_joined_users: Optional[bool] = None
    audio_api: Optional[Literal["gtts", "openai"]] = None
