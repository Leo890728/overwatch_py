from enum import Enum


class HeroGamemode(str, Enum):
    """Gamemodes a hero can be played in (used by /heroes filter and HeroShort.gamemodes)."""
    QUICKPLAY = "quickplay"
    STADIUM = "stadium"


class PlayerGamemode(str, Enum):
    """Gamemodes used by player-stats endpoints."""
    QUICKPLAY = "quickplay"
    COMPETITIVE = "competitive"
