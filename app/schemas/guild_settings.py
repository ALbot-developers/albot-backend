from typing import Optional, Literal, Annotated

from pydantic import BaseModel, Field

GoogleTTSVoiceCode = Annotated[str, Field(pattern=r'^[a-z]{2}-[A-Z]{2,3}-(Wavenet|Standard)-[A-Za-z]$')]

class GuildSettingsUpdate(BaseModel):
    lang: Optional[str] = None
    character_limit: Optional[int] = Field(default=None, le=4000, ge=0,
                                           description="Maximum character limit for messages")
    speech_speed: Optional[float] = Field(default=None, ge=0.1, le=4.0, description="Speech speed multiplier")
    read_name: Optional[bool] = None
    custom_voice: Optional[GoogleTTSVoiceCode] = None
    translate: Optional[bool] = None
    read_name_on_join: Optional[bool] = None
    read_name_on_leave: Optional[bool] = None
    read_guild: Optional[bool] = None
    read_not_joined_users: Optional[bool] = None
    audio_api: Optional[Literal["gtts", "openai"]] = None
    voice_clone_mode: Optional[Literal["off", "caller", "speaker"]] = None
