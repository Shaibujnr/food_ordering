from pydantic.dataclasses import dataclass
from foodie import enums


@dataclass
class InvitationTokenPayload:
    id: str
    email: str
    token_type: enums.ActivityTokenType
