import time
from dataclasses import dataclass
from typing import Optional, Literal

from app.models.character_usage import CharacterUsages


@dataclass
class ConnectionStateCreate:
    vc_id: int
    tc_id: int
    read_guild: Optional[bool] = None
    read_name: Optional[bool] = None
    speech_speed: Optional[float] = None
    lang: Optional[str] = None
    character_limit: Optional[int] = None
    translate: Optional[bool] = None


@dataclass
class ConnectionState:
    guild_id: int
    vc_id: int
    target_id: int  # 読み上げるチャンネルIDかサーバーID
    service: Literal["gtts", "openai"]
    language_code: Literal["auto"] | str
    translate: bool
    wavenet_voice: str
    standard_voice: str
    custom_voice: str | None
    read_name: bool
    dict: dict
    dict_keys: list
    speech_speed: float
    character_limit: int
    character_usage: CharacterUsages
    read_guild: bool
    read_name_on_join: bool
    read_name_on_leave: bool
    read_not_joined_users: bool
    unix_time_connected: float = time.time()
    sync_count: int = 0
