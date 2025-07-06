from pydantic import BaseModel


class QuickReportPost(BaseModel):
    category: str  # todo: 後で型定義
    description: str
