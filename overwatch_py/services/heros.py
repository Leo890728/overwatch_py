from typing import Optional, Literal

from pydantic import BaseModel

from ..enums import (
    CompetitiveDivisionFilter,
    Hero,
    HeroGamemode,
    Locale,
    Map,
    Platform,
    PlayerGamemode,
    Region,
    Role,
)
from ..session import HTTPSession
from ..models import HeroData, HeroShort, HeroStats


SortOrder = Literal["asc", "desc"]


class HerosService:
    def __init__(self, session: HTTPSession):
        self.session = session

    async def get_heroes(self, role: Role = None, locale: Locale = Locale.EN_US, gamemode: Optional[HeroGamemode] = None) -> list[HeroShort]:
        """Get a list of Overwatch heroes, which can be filtered using roles or gamemodes."""
        params = {}
        params["locale"] = locale.value if locale else Locale.EN_US.value
        if role is not None:
            params["role"] = role.value
        if gamemode is not None:
            params["gamemode"] = gamemode.value
        return list(map(lambda data: HeroShort(**data), await self.session.get("/heroes", params=params)))

    async def get_hero_data(self, hero: Hero, locale: Locale = Locale.EN_US) -> HeroData:
        """Get data about an Overwatch hero : description, abilities, stadium powers, story, etc."""
        params = {}
        params["locale"] = locale.value if locale else Locale.EN_US.value
        return HeroData(**await self.session.get(f"/heroes/{hero.value}", params=params))

    async def get_heroes_stats_with_filter(self, stats_filter: "StatsFilter") -> list[HeroStats]:
        """Get hero statistics usage, filtered by platform, region, role, etc. Only Role Queue gamemodes are concerned."""
        params = {}
        params["platform"] = stats_filter.platform.value if stats_filter.platform else Platform.PC.value
        params["gamemode"] = stats_filter.gamemode.value if stats_filter.gamemode else PlayerGamemode.COMPETITIVE.value
        params["region"] = stats_filter.region.value if stats_filter.region else Region.ASIA.value
        if stats_filter.role is not None:
            params["role"] = stats_filter.role.value
        if stats_filter.map is not None:
            params["map"] = stats_filter.map.value
        if stats_filter.competitive_division is not None:
            params["competitive_division"] = stats_filter.competitive_division.value
        if stats_filter.order_by is not None:
            params["order_by"] = stats_filter.order_by
        return list(map(lambda data: HeroStats(**data), await self.session.get("/heroes/stats", params=params)))

    async def get_heroes_stats(self, platform: Platform = Platform.PC, gamemode: PlayerGamemode = PlayerGamemode.COMPETITIVE,
                               region: Region = Region.ASIA, role: Optional[Role] = None, map: Optional[Map] = None,
                               competitive_division: Optional[CompetitiveDivisionFilter] = None, order_by: Optional[str] = "hero:asc") -> list[HeroStats]:
        """Get hero statistics usage, filtered by platform, region, role, etc. Only Role Queue gamemodes are concerned."""
        filter = StatsFilter(platform=platform, gamemode=gamemode, region=region, role=role, map=map, competitive_division=competitive_division, order_by=order_by)
        return await self.get_heroes_stats_with_filter(filter)


class StatsFilter(BaseModel):
    platform: Platform = Platform.PC
    gamemode: PlayerGamemode = PlayerGamemode.COMPETITIVE
    region: Region = Region.ASIA
    role: Optional[Role] = None
    map: Optional[Map] = None
    competitive_division: Optional[CompetitiveDivisionFilter] = None
    order_by: Optional[str] = "hero:asc"

    def with_platform(self, platform: Platform):
        self.platform = platform
        return self

    def with_gamemode(self, gamemode: PlayerGamemode):
        self.gamemode = gamemode
        return self

    def with_region(self, region: Region):
        self.region = region
        return self

    def with_role(self, role: Role):
        self.role = role
        return self

    def with_map(self, map: Map):
        self.map = map
        return self

    def with_competitive_division(self, competitive_division: CompetitiveDivisionFilter):
        self.competitive_division = competitive_division
        return self

    def order_by_hero(self, sort_order: SortOrder = "asc"):
        self.order_by = f"hero:{sort_order or 'asc'}"
        return self

    def order_by_winrate(self, sort_order: SortOrder = "asc"):
        self.order_by = f"winrate:{sort_order or 'asc'}"
        return self

    def order_by_pickrate(self, sort_order: SortOrder = "asc"):
        self.order_by = f"pickrate:{sort_order or 'asc'}"
        return self
