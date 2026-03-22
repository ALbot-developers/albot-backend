import json
import re

from app.core.error import CustomHTTPException
from app.db.connection import get_connection_pool
from app.models.custom_voices import is_character_voice

with open("app/static/gtts_languages.json") as f:
    gtts_languages = json.load(f)

_GTTS_VOICE_PATTERN = re.compile(r"^([a-z]{2,3}-[A-Z]{2})-(?:Wavenet|Standard)-([A-Z])$")


def is_valid_gtts_voice(voice: str) -> bool:
    m = _GTTS_VOICE_PATTERN.match(voice)
    if not m:
        return False
    lang, letter = m.group(1), m.group(2)
    if lang not in gtts_languages:
        return False
    lang_voices = gtts_languages[lang]
    voice_type = voice.split("-")[-2].lower()
    return voice_type in lang_voices and letter in lang_voices[voice_type]


async def is_cloned_voice(voice: str, guild_id: int) -> bool:
    async with get_connection_pool().acquire() as conn:
        row = await conn.fetchval(
            "SELECT 1 FROM cloned_voices WHERE voice = $1 AND guild_id = $2",
            voice, guild_id
        )
    return row is not None


async def validate_custom_voice(voice: str, guild_id: int):
    if is_valid_gtts_voice(voice):
        return
    if is_character_voice(voice):
        return
    if await is_cloned_voice(voice, guild_id):
        return
    raise CustomHTTPException(400,
                              "Invalid custom_voice: not a valid Google TTS voice code and not found in cloned voices for this guild.")
