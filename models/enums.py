import enum


class RoleType(enum.Enum):
    user = "user"
    moderator = "moderator"
    administrator = "administrator"


class State(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
