from typing import Optional, Literal, Annotated

from pydantic import BaseModel, Field

GoogleTTSVoiceCode = Annotated[str, Field(pattern=r'^[a-z]{2}-[A-Z]{2,3}-(Wavenet|Standard)-[A-Za-z]$')]

class GuildSettingsUpdate(BaseModel):
    lang: Optional[str] = None
    character_limit: Optional[int] = None
    speech_speed: Optional[float] = None
    read_name: Optional[bool] = None
    custom_voice: Optional[GoogleTTSVoiceCode] = None
    translate: Optional[bool] = None
    read_name_on_join: Optional[bool] = None
    read_name_on_leave: Optional[bool] = None
    read_guild: Optional[bool] = None
    read_not_joined_users: Optional[bool] = None
    audio_api: Optional[Literal["gtts", "openai"]] = None
