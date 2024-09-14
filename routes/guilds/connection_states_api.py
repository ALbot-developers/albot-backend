import json
from dataclasses import dataclass
from typing import Literal

import time
from fastapi import APIRouter, Security

from auth import verify_token
from routes.guilds.character_usage_api import get_guild_character_usage
from routes.guilds.dict_api import get_guild_dict
from routes.guilds.settings_api import get_guild_settings
from type_specifications.api_response import CharacterUsages

router = APIRouter()

with open("gtts_languages.json") as f:
    gtts_languages = json.load(f)


@dataclass
class ConnectionStatesOptions:
    guild_id: int
    vc_id: int
    target_id: int
    read_guild: bool = None
    read_name: bool = None
    speech_speed: float = None
    lang: str = None
    character_limit: int = None
    translate: bool = None


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
    read_name_on_join: bool
    read_name_on_leave: bool
    read_not_joined_users: bool
    unix_time_connected: float = time.time()
    sync_count: int = 0


def set_voice(lang: str, custom_voice: str):
    if lang == "auto":
        return "auto", "auto"
    voices = gtts_languages[lang]
    # Wavenet音声を決定
    if "wavenet" in voices:
        if "C" in voices["wavenet"]:
            wavenet_voice = f"{lang}-Wavenet-C"
        else:
            voice_type_list = list(voices["wavenet"].keys())
            voice_type_list.sort()
            primary_voice_type = voice_type_list[0]
            wavenet_voice = f"{lang}-Wavenet-{primary_voice_type}"
    else:
        wavenet_voice = None
    # Standard音声を決定
    voice_type_list = list(voices["standard"].keys())
    voice_type_list.sort()
    primary_voice_type = voice_type_list[0]
    standard_voice = f"{lang}-Standard-{primary_voice_type}"
    if custom_voice:
        custom_voice_type = custom_voice.split("-")[-2]
        wavenet_voice = custom_voice if custom_voice_type == "Wavenet" else wavenet_voice
        standard_voice = custom_voice if custom_voice_type == "Standard" else standard_voice
    return wavenet_voice, standard_voice


async def create_connection_states(guild_id: int, options: ConnectionStatesOptions):
    settings_data = await get_guild_settings(guild_id)
    dict_data = await get_guild_dict(guild_id)
    dict_keys = sorted(dict_data, key=lambda x: len(x[0]))
    language_code = options.lang if options.lang else settings_data.lang or "ja-JP"
    translate = False if language_code == "auto" else (
        options.translate if options.translate else settings_data.translate or False
    )
    voices = set_voice(language_code, settings_data.custom_voice)
    return ConnectionState(
        guild_id=guild_id,
        vc_id=options.vc_id,
        target_id=options.target_id,
        service="gtts",
        language_code=language_code,
        translate=translate,
        wavenet_voice=voices[0],
        standard_voice=voices[1],
        custom_voice=settings_data.custom_voice,
        read_name=options.read_name if options.read_name else settings_data.read_name or False,
        dict=dict_data,
        dict_keys=dict_keys,
        speech_speed=options.speech_speed if options.speech_speed else settings_data.speech_speed or 1.0,
        character_limit=options.character_limit if options.character_limit else settings_data.character_limit or 100,
        character_usage=await get_guild_character_usage(guild_id),
        read_name_on_join=settings_data.read_name_on_join,
        read_name_on_leave=settings_data.read_name_on_leave,
        read_not_joined_users=settings_data.read_not_joined_users
    )


@router.post("/{guild_id}/connection_states")
async def create_connection_states_api(guild_id: int, data: ConnectionStatesOptions,
                                       _auth=Security(lambda: verify_token("bearer"))):
    # connection_statesデータを作成
    connection_states = await create_connection_states(guild_id, data)
    return {
        "message": "Updated guild data.",
        "data": connection_states
    }
