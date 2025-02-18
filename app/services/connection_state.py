import json

from app.schemas.connection_state import ConnectionStateCreate, ConnectionState
from app.services import guild_settings, guild_dict, character_usages

with open("static/gtts_languages.json") as f:
    gtts_languages = json.load(f)


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


async def create(guild_id: int, options: ConnectionStateCreate):
    settings_data = await guild_settings.get(guild_id)
    dict_data = await guild_dict.get(guild_id)
    dict_keys = sorted(dict_data, key=lambda x: len(x[0]))
    language_code = options.lang if options.lang else settings_data.lang or "ja-JP"
    translate = False if language_code == "auto" else (
        options.translate if options.translate else settings_data.translate or False
    )
    voices = set_voice(language_code, settings_data.custom_voice)
    read_guild = settings_data.read_guild if options.read_guild is None else options.read_guild
    return ConnectionState(
        guild_id=guild_id,
        vc_id=options.vc_id,
        target_id=guild_id if read_guild else options.tc_id,
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
        character_usage=await character_usages.get(guild_id),
        read_guild=read_guild,
        read_name_on_join=settings_data.read_name_on_join,
        read_name_on_leave=settings_data.read_name_on_leave,
        read_not_joined_users=settings_data.read_not_joined_users
    )
