from enum import Enum


class MapGamemode(str, Enum):
    ASSAULT = "assault"
    CAPTURE_THE_FLAG = "capture-the-flag"
    CLASH = "clash"
    CONTROL = "control"
    DEATHMATCH = "deathmatch"
    ELIMINATION = "elimination"
    ESCORT = "escort"
    FLASHPOINT = "flashpoint"
    HYBRID = "hybrid"
    PAYLOAD_RACE = "payload-race"
    PRACTICE_RANGE = "practice-range"
    PUSH = "push"
    TEAM_DEATHMATCH = "team-deathmatch"
    WORKSHOP = "workshop"