"""カスタムボイスの定義"""

# キャラクターボイスの一覧
CHARACTER_VOICES: frozenset[str] = frozenset({
    "zundamon",
    "ankomon",
    "kasukabetsumugi",
    "meimeihimari",
    "shikokumetan",
    "tohokuitako",
    "tohokukiritan",
})


def is_character_voice(voice: str) -> bool:
    return voice in CHARACTER_VOICES
