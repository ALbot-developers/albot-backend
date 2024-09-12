import json
from typing import Optional, Literal


class SettingsData:
    def __init__(
            self, guild_id: Optional[int] = None,
            lang: Optional[str] = None,
            word_limit: Optional[int] = None,
            speech_speed: Optional[float] = None,
            read_name: Optional[bool] = None,
            custom_voice: Optional[str] = None,
            translate: Optional[bool] = None,
            read_name_on_join: Optional[bool] = None,
            read_name_on_leave: Optional[bool] = None,
            read_guild: Optional[bool] = None,
            read_not_joined_user: Optional[bool] = None,
            audio_api: Optional[Literal["gtts", "openai"]] = None
    ):
        self.guild_id = guild_id
        self.lang = lang
        self.word_limit = word_limit
        self.speech_speed = speech_speed
        self.read_name = read_name
        self.custom_voice = custom_voice
        self.translate = translate
        self.read_name_on_join = read_name_on_join
        self.read_name_on_leave = read_name_on_leave
        self.read_guild = read_guild
        self.read_not_joined_user = read_not_joined_user
        self.audio_api = audio_api

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            guild_id=data.get('guild_id'),
            lang=data.get('lang'),
            word_limit=data.get('word_limit'),
            speech_speed=data.get('speech_speed'),
            read_name=data.get('read_name'),
            custom_voice=data.get('custom_voice'),
            translate=data.get('translate'),
            read_name_on_join=data.get('read_name_on_join'),
            read_name_on_leave=data.get('read_name_on_leave'),
            read_guild=data.get('read_guild'),
            read_not_joined_user=data.get('read_not_joined_user'),
            audio_api=data.get('audio_api')
        )

    def to_json(self):
        return json.dumps(self.__dict__)
