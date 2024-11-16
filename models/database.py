import datetime
import json
from dataclasses import dataclass
from typing import Optional, Literal


class SettingsData:
    def __init__(
            self, guild_id: Optional[int] = None,
            lang: Optional[str] = None,
            character_limit: Optional[int] = None,
            speech_speed: Optional[float] = None,
            read_name: Optional[bool] = None,
            custom_voice: Optional[str] = None,
            translate: Optional[bool] = None,
            read_name_on_join: Optional[bool] = None,
            read_name_on_leave: Optional[bool] = None,
            read_guild: Optional[bool] = None,
            read_not_joined_users: Optional[bool] = None,
            audio_api: Optional[Literal["gtts", "openai"]] = None
    ):
        self.guild_id = guild_id
        self.lang = lang
        self.character_limit = character_limit
        self.speech_speed = speech_speed
        self.read_name = read_name
        self.custom_voice = custom_voice
        self.translate = translate
        self.read_name_on_join = read_name_on_join
        self.read_name_on_leave = read_name_on_leave
        self.read_guild = read_guild
        self.read_not_joined_users = read_not_joined_users
        self.audio_api = audio_api

    # テーブルから取得したデータをSettingsDataクラスに変換
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            guild_id=data.get('guild_id'),
            lang=data.get('lang'),
            # todo: データベースもword_limitからcharacter_limitに変更する
            character_limit=data.get('character_limit'),
            speech_speed=data.get('speech_speed'),
            read_name=data.get('read_name'),
            custom_voice=data.get('custom_voice'),
            translate=data.get('translate'),
            read_name_on_join=data.get('read_name_on_join'),
            read_name_on_leave=data.get('read_name_on_leave'),
            read_guild=data.get('read_guild'),
            read_not_joined_users=data.get('read_not_joined_users'),
            audio_api=data.get('audio_api')
        )

    def to_json(self):
        return json.dumps(self.__dict__)


@dataclass
class SubscriptionData:
    guild_id: int
    user_id: int
    sub_id: str
    sub_start: datetime.date
    plan: str
    last_updated: datetime.date

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            guild_id=data.get('guild_id'),
            user_id=data.get('user_id'),
            sub_id=data.get('sub_id'),
            sub_start=data.get('sub_start'),
            plan=data.get('plan'),
            last_updated=data.get('last_updated')
        )
