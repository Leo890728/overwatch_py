from typing import Optional

from .services import HerosService, MapsService, PlayersService
from .services.players import HeroFilter
from .session import HTTPSession
from .models import (
    GamemodeDetails,
    HeroData,
    HeroPlayerCareerStats,
    HeroShort,
    HeroStats,
    MapDetails,
    Player,
    PlayerSearchResult,
    PlayerStats,
    PlayerStatsSummary,
    PlayerSummary,
)
from .enums import (
    CompetitiveDivisionFilter,
    Hero,
    HeroGamemode,
    Locale,
    Map,
    MapGamemode,
    Platform,
    PlayerGamemode,
    Region,
    Role,
)


class Client:
    def __init__(self, session: HTTPSession = None):
        self.session = session or HTTPSession()
        self.heros = HerosService(self.session)
        self.maps = MapsService(self.session)
        self.players = PlayersService(self.session)

    async def get_heroes(self, role: Role = None, locale: Locale = Locale.EN_US, gamemode: Optional[HeroGamemode] = None) -> list[HeroShort]:
        """Get a list of Overwatch heroes, which can be filtered using roles or gamemodes."""
        return await self.heros.get_heroes(role, locale, gamemode)

    async def get_hero_data(self, hero: Hero, locale: Locale = Locale.EN_US) -> HeroData:
        """Get data about an Overwatch hero : description, abilities, stadium powers, story, etc."""
        return await self.heros.get_hero_data(hero, locale)

    async def get_maps(self, map_gamemode: Optional[MapGamemode] = None) -> list[MapDetails]:
        """Get a list of Overwatch maps : Hanamura, King's Row, Dorado, etc."""
        return await self.maps.get_maps(map_gamemode)

    async def get_gamemode_details(self) -> list[GamemodeDetails]:
        """Get a list of Overwatch gamemodes : Assault, Escort, Flashpoint, Hybrid, etc."""
        return await self.maps.get_gamemode_details()

    async def get_heroes_stats(self, platform: Platform = Platform.PC, gamemode: PlayerGamemode = PlayerGamemode.COMPETITIVE,
                               region: Region = Region.ASIA, role: Optional[Role] = None, map: Optional[Map] = None,
                               competitive_division: Optional[CompetitiveDivisionFilter] = None, order_by: Optional[str] = "hero:asc") -> list[HeroStats]:
        """Get hero statistics usage, filtered by platform, region, role, etc. Only Role Queue gamemodes are concerned."""
        return await self.heros.get_heroes_stats(platform, gamemode, region, role, map, competitive_division, order_by)

    async def search_players(self, name: str, order_by: Optional[str] = None,
                             offset: Optional[int] = None, limit: Optional[int] = None) -> PlayerSearchResult:
        """Search for players by BattleTag name."""
        return await self.players.search_players(name, order_by, offset, limit)

    async def get_player(self, player_id: str, gamemode: Optional[PlayerGamemode] = None,
                         platform: Optional[Platform] = None) -> Player:
        """Get all player data: summary and statistics."""
        return await self.players.get_player(player_id, gamemode, platform)

    async def get_player_summary(self, player_id: str) -> PlayerSummary:
        """Get player summary: name, avatar, endorsement, competitive ranks."""
        return await self.players.get_player_summary(player_id)

    async def get_player_stats(self, player_id: str, gamemode: Optional[PlayerGamemode] = None,
                               platform: Optional[Platform] = None) -> PlayerStatsSummary:
        """Get player stats summary (general / roles / heroes)."""
        return await self.players.get_player_stats(player_id, gamemode, platform)

    async def get_player_career_stats(self, player_id: str, gamemode: PlayerGamemode,
                                      platform: Optional[Platform] = None,
                                      hero: Optional[HeroFilter] = None) -> dict[str, Optional[HeroPlayerCareerStats]]:
        """Get player career stats as flat {label: value} maps per hero."""
        return await self.players.get_player_career_stats(player_id, gamemode, platform, hero)

    async def get_player_career_stats_with_labels(self, player_id: str, gamemode: PlayerGamemode,
                                                  platform: Optional[Platform] = None,
                                                  hero: Optional[HeroFilter] = None):
        """Get player career stats with labels and categories per hero."""
        return await self.players.get_player_career_stats_with_labels(player_id, gamemode, platform, hero)

    async def get_player_full_stats(self, player_id: str, gamemode: Optional[PlayerGamemode] = None,
                                    platform: Optional[Platform] = None) -> PlayerStats:
        """Get a player's full per-platform stats (pc/console)."""
        return await self.players.get_player_full_stats(player_id, gamemode, platform)