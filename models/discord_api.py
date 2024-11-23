from dataclasses import dataclass
from typing import Optional, List


@dataclass
class UserAvatarDecorationResponse:
    asset: str
    sku_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            asset=data['asset'],
            sku_id=data.get('sku_id')
        )


class PremiumTypes:
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_0 = 3

    @classmethod
    def from_value(cls, value: int):
        premium_types = {
            0: 'None',
            1: 'Nitro Classic',
            2: 'Nitro Standard',
            3: 'Nitro Basic'
        }
        return premium_types.get(value, 'Unknown Type')


# todo: dataclassに
class UserPIIResponse:
    def __init__(self, user_id: str, username: str, avatar: Optional[str], discriminator: str,
                 public_flags: int, flags: int, bot: Optional[bool], system: Optional[bool],
                 banner: Optional[str], accent_color: Optional[int], global_name: Optional[str],
                 avatar_decoration_data: Optional[UserAvatarDecorationResponse],
                 mfa_enabled: bool, locale: str, premium_type: Optional[PremiumTypes],
                 email: Optional[str], verified: Optional[bool]):
        self.id = user_id
        self.username = username
        self.avatar = avatar
        self.discriminator = discriminator
        self.public_flags = public_flags
        self.flags = flags
        self.bot = bot
        self.system = system
        self.banner = banner
        self.accent_color = accent_color
        self.global_name = global_name
        self.avatar_decoration_data = avatar_decoration_data
        self.mfa_enabled = mfa_enabled
        self.locale = locale
        self.premium_type = premium_type
        self.email = email
        self.verified = verified

    @classmethod
    def from_dict(cls, data: dict):
        avatar_decoration = data.get('avatar_decoration_data')
        premium_type_data = data.get('premium_type')
        return cls(
            user_id=data.get('id'),
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
            premium_type=PremiumTypes.from_value(premium_type_data) if premium_type_data else None,
            email=data.get('email'),
            verified=data.get('verified')
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "avatar": self.avatar,
            "discriminator": self.discriminator,
            "public_flags": self.public_flags,
            "flags": self.flags,
            "bot": self.bot,
            "system": self.system,
            "banner": self.banner,
            "accent_color": self.accent_color,
            "global_name": self.global_name,
            "avatar_decoration_data": self.avatar_decoration_data,
            "mfa_enabled": self.mfa_enabled,
            "locale": self.locale,
            "premium_type": self.premium_type,
            "email": self.email,
            "verified": self.verified
        }


@dataclass
class PartialGuild:
    """
    {
      "id": "80351110224678912",
      "name": "1337 Krew",
      "icon": "8342729096ea3675442027381ff50dfe",
      "banner": "bb42bdc37653b7cf58c4c8cc622e76cb",
      "owner": true,
      "permissions": "36953089",
      "features": ["COMMUNITY", "NEWS", "ANIMATED_ICON", "INVITE_SPLASH", "BANNER", "ROLE_ICONS"],
      "approximate_member_count": 3268,
      "approximate_presence_count": 784
    }
    """
    id: str
    name: str
    icon: Optional[str]
    banner: Optional[str]
    owner: bool
    permissions: str
    features: List[str]
    approximate_member_count: int
    approximate_presence_count: int

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
        return {k: v for k, v in self.__dict__.items() if v is not None}
