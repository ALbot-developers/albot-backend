from pydantic import BaseModel


class MessageLinkExpansionPreference(BaseModel):
    enabled: bool
