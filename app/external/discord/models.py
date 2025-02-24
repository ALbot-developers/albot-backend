from typing import Optional, List

from pydantic import BaseModel


class UserAvatarDecorationResponse(BaseModel):
    asset: str
    sku_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            asset=data['asset'],
            sku_id=data.get('sku_id')
        )


class UserPIIResponse(BaseModel):
    id: str
    username: str
    avatar: Optional[str]
    discriminator: str
    public_flags: int
    flags: int
    bot: Optional[bool]
    system: Optional[bool]
    banner: Optional[str]
    accent_color: Optional[int]
    global_name: Optional[str]
    avatar_decoration_data: Optional[UserAvatarDecorationResponse]
    mfa_enabled: bool
    locale: str
    premium_type: Optional[str]
    email: Optional[str]
    verified: Optional[bool]


    @classmethod
    def from_dict(cls, data: dict):
        avatar_decoration = data.get('avatar_decoration_data')
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            avatar=data.get('avatar'),
            discriminator=data.get('discriminator'),
            public_flags=data.get('public_flags'),
            flags=data.get('flags'),
            bot=data.get('bot'),
            system=data.get('system'),
            banner=data.get('banner'),
            accent_color=data.get('accent_color'),
            global_name=data.get('global_name'),
            avatar_decoration_data=UserAvatarDecorationResponse.from_dict(
                avatar_decoration) if avatar_decoration else None,
            mfa_enabled=data.get('mfa_enabled'),
            locale=data.get('locale'),
            premium_type=data.get('premium_type'),
            email=data.get('email'),
            verified=data.get('verified')
        )

    def to_dict(self):
        return self.model_dump(
            exclude_unset=True,
            by_alias=True
        )


class PartialGuild(BaseModel):
    id: str
    name: str
    icon: Optional[str]
    banner: Optional[str]
    owner: bool
    permissions: str
    features: List[str]
    approximate_member_count: Optional[int] = None
    approximate_presence_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            icon=data.get('icon'),
            banner=data.get('banner'),
            owner=data.get('owner'),
            permissions=data.get('permissions'),
            features=data.get('features'),
            approximate_member_count=data.get('approximate_member_count'),
            approximate_presence_count=data.get('approximate_presence_count')
        )

    def to_dict(self):
        return self.model_dump(exclude_none=True)
