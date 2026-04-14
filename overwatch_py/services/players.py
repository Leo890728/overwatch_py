from typing import Literal, Optional, Union

from ..enums import Hero, Platform, PlayerGamemode
from ..models import (
    HeroCareerStats,
    HeroPlayerCareerStats,
    Player,
    PlayerSearchResult,
    PlayerStats,
    PlayerStatsSummary,
    PlayerSummary,
)
from ..session import HTTPSession


HeroFilter = Union[Hero, Literal["all-heroes"]]


def _hero_filter_value(hero: Optional[HeroFilter]) -> Optional[str]:
    if hero is None:
        return None
    return hero.value if isinstance(hero, Hero) else hero


class PlayersService:
    def __init__(self, session: HTTPSession):
        self.session = session

    async def search_players(
        self,
        name: str,
        order_by: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> PlayerSearchResult:
        """Search for players by BattleTag name."""
        params: dict = {"name": name}
        if order_by is not None:
            params["order_by"] = order_by
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        return PlayerSearchResult(**await self.session.get("/players", params=params))

    async def get_player(
        self,
        player_id: str,
        gamemode: Optional[PlayerGamemode] = None,
        platform: Optional[Platform] = None,
    ) -> Player:
        """Get all player data: summary and statistics."""
        params: dict = {}
        if gamemode is not None:
            params["gamemode"] = gamemode.value
        if platform is not None:
            params["platform"] = platform.value
        return Player(**await self.session.get(f"/players/{player_id}", params=params))

    async def get_player_summary(self, player_id: str) -> PlayerSummary:
        """Get player summary: name, avatar, endorsement, competitive ranks, etc."""
        return PlayerSummary(**await self.session.get(f"/players/{player_id}/summary"))

    async def get_player_stats(
        self,
        player_id: str,
        gamemode: Optional[PlayerGamemode] = None,
        platform: Optional[Platform] = None,
    ) -> PlayerStatsSummary:
        """Get player stats summary (general / roles / heroes) aggregated across platforms."""
        params: dict = {}
        if gamemode is not None:
            params["gamemode"] = gamemode.value
        if platform is not None:
            params["platform"] = platform.value
        return PlayerStatsSummary(**await self.session.get(f"/players/{player_id}/stats/summary", params=params))

    async def get_player_career_stats(
        self,
        player_id: str,
        gamemode: PlayerGamemode,
        platform: Optional[Platform] = None,
        hero: Optional[HeroFilter] = None,
    ) -> dict[str, Optional[HeroPlayerCareerStats]]:
        """Get player career stats as flat {category: {label: value}} maps per hero.

        Response keys are hero keys (e.g. `ana`) or the `all-heroes` aggregate.
        """
        params: dict = {"gamemode": gamemode.value}
        if platform is not None:
            params["platform"] = platform.value
        hv = _hero_filter_value(hero)
        if hv is not None:
            params["hero"] = hv
        data = await self.session.get(f"/players/{player_id}/stats/career", params=params)
        return {
            k: (HeroPlayerCareerStats(**v) if v is not None else None)
            for k, v in data.items()
        }

    async def get_player_career_stats_with_labels(
        self,
        player_id: str,
        gamemode: PlayerGamemode,
        platform: Optional[Platform] = None,
        hero: Optional[HeroFilter] = None,
    ):
        """Get player career stats with labels and categories grouped per hero.

        Returns a `{hero_key: [HeroCareerStats, ...]}` mapping.
        """
        params: dict = {"gamemode": gamemode.value}
        if platform is not None:
            params["platform"] = platform.value
        hv = _hero_filter_value(hero)
        if hv is not None:
            params["hero"] = hv
        data = await self.session.get(f"/players/{player_id}/stats", params=params)
        return {
            k: ([HeroCareerStats(**item) for item in v] if v is not None else None)
            for k, v in data.items()
        }

    async def get_player_full_stats(
        self,
        player_id: str,
        gamemode: Optional[PlayerGamemode] = None,
        platform: Optional[Platform] = None,
    ) -> PlayerStats:
        """Convenience: get a player's full per-platform stats (pc/console).

        Equivalent to calling `get_player` and returning `.stats`.
        """
        player = await self.get_player(player_id, gamemode=gamemode, platform=platform)
        return player.stats