from typing import Optional

from pydantic import BaseModel

from app.models.character_usage import CharacterUsage


class CharacterUsagesUpdate(BaseModel):
    wavenet: Optional[CharacterUsage] = None
    standard: Optional[CharacterUsage] = None
