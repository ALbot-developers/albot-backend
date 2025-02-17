from typing import List, Optional

from pydantic import BaseModel


class TrustedRolesUpdate(BaseModel):
    enabled: Optional[bool] = None
    role_ids: Optional[List[int]] = None
