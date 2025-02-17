from dataclasses import dataclass
from typing import Optional, Literal

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

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)



@dataclass
class PremiumSettings:
    guild_id: Optional[int] = None
    sub_id: Optional[str] = None
    read_name_on_leave: Optional[bool] = None
    read_name_on_join: Optional[bool] = None
    custom_voice: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            guild_id=data.get('guild_id'),
            sub_id=data.get('sub_id'),
            read_name_on_leave=data.get('read_name_on_leave'),
            read_name_on_join=data.get('read_name_on_join'),
            custom_voice=data.get('custom_voice')
        )
