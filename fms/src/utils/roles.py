from enum import Enum

class UserRole(Enum):
    DEFAULT = "D"
    TEAM_MEMBER = "TM"
    FIELD_HELPER = "FH"
    FIELD_MANAGER = "FM"
    FIELD_ADMIN = "FA"