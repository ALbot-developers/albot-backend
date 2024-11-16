from dataclasses import dataclass


@dataclass
class CharacterUsage:
    used_characters: int
    monthly_quota: int = None

    @property
    def remaining_characters(self) -> int:
        return self.monthly_quota - self.used_characters


@dataclass
class CharacterUsages:
    wavenet: CharacterUsage = None
    standard: CharacterUsage = None


@dataclass
class CharacterUsageAPIResponse:
    message: str
    data: CharacterUsages
