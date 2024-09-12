import json
from typing import Optional


class UserAvatarDecorationResponse:
    def __init__(self, asset: str, sku_id: Optional[str] = None):
        self.asset = asset
        self.sku_id = sku_id

    @classmethod
    def from_json(cls, data: dict):
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
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
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
            avatar_decoration_data=UserAvatarDecorationResponse.from_json(
                avatar_decoration) if avatar_decoration else None,
            mfa_enabled=data.get('mfa_enabled'),
            locale=data.get('locale'),
            premium_type=PremiumTypes.from_value(premium_type_data) if premium_type_data else None,
            email=data.get('email'),
            verified=data.get('verified')
        )

    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)
