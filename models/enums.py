import enum


class RoleType(enum.Enum):
    user = "user"
    moderator = "moderator"
    administrator = "administrator"


class State(enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
