from dataclasses import dataclass
from typing import List


@dataclass
class TrustedRoles:
    enabled: bool = None
    role_ids: List[int] = None
