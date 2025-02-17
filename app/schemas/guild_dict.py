from typing import Dict, Any

from pydantic import BaseModel, Field


class DictPut(BaseModel):
    dict: Dict[str, Any] = Field(...)
