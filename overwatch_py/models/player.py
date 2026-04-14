from typing import Optional

from pydantic import BaseModel, HttpUrl

from ..enums import Rank
from .player_stats import PlayerStats


class PlayerShort(BaseModel):
    player_id: str
    name: str
    avatar: Optional[HttpUrl] = None
    namecard: Optional[HttpUrl] = None
    title: Optional[str] = None
    career_url: HttpUrl
    blizzard_id: str
    last_updated_at: Optional[int] = None
    is_public: Optional[bool] = None


class PlayerSearchResult(BaseModel):
    total: int
    results: list[PlayerShort]


class PlayerEndorsement(BaseModel):
    level: int
    frame: HttpUrl


class PlayerCompetitiveRank(BaseModel):
    division: Rank
    tier: int
    role_icon: HttpUrl
    rank_icon: HttpUrl
    tier_icon: HttpUrl


class PlatformCompetitiveRanksContainer(BaseModel):
    season: Optional[int] = None
    tank: Optional[PlayerCompetitiveRank] = None
    damage: Optional[PlayerCompetitiveRank] = None
    support: Optional[PlayerCompetitiveRank] = None
    open: Optional[PlayerCompetitiveRank] = None


class PlayerCompetitiveRanksContainer(BaseModel):
    pc: Optional[PlatformCompetitiveRanksContainer] = None
    console: Optional[PlatformCompetitiveRanksContainer] = None


class PlayerSummary(BaseModel):
    username: str
    avatar: Optional[HttpUrl] = None
    namecard: Optional[HttpUrl] = None
    title: Optional[str] = None
    endorsement: Optional[PlayerEndorsement] = None
    competitive: Optional[PlayerCompetitiveRanksContainer] = None
    last_updated_at: Optional[int] = None


class Player(BaseModel):
    summary: PlayerSummary
    stats: Optional[PlayerStats] = None
