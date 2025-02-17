from dataclasses import dataclass

from app.models.character_usage import CharacterUsages


@dataclass
class CharacterUsageAPIResponse:
    message: str
    data: CharacterUsages
