from typing import Dict, Any

from pydantic import BaseModel, Field


class DictPut(BaseModel):
    dict_data: Dict[str, Any] = Field(..., alias="dict")
