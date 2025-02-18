from dataclasses import dataclass
from typing import Optional, Literal, ClassVar

from pydantic import BaseModel


class GuildSettings(BaseModel):
    guild_id: int
    lang: str
    word_limit: int
    speech_speed: float
    read_name: bool
    translate: bool
    read_name_on_join: bool
    read_name_on_leave: bool
    read_guild: bool
    read_not_joined_users: bool
    audio_api: Literal["gtts", "openai"]
    custom_voice: Optional[str] = None


class DefaultSettings(GuildSettings):
    guild_id: ClassVar[int]



@dataclass
class PremiumSettings:
    sub_id: Optional[str] = None
    read_name_on_leave: Optional[bool] = None
    read_name_on_join: Optional[bool] = None
    custom_voice: Optional[str] = None
