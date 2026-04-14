from enum import Enum


class Role(str, Enum):
    TANK = "tank"
    DAMAGE = "damage"
    SUPPORT = "support"