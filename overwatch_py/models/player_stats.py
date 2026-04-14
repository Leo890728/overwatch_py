from typing import Optional, Union

from pydantic import BaseModel

from ..enums import CareerStatCategory, Hero


Number = Union[int, float]


class TotalStatsSummary(BaseModel):
    eliminations: int
    assists: int
    deaths: int
    damage: int
    healing: int


class AverageStatsSummary(BaseModel):
    eliminations: float
    assists: float
    deaths: float
    damage: float
    healing: float


class StatsSummary(BaseModel):
    games_played: int
    games_won: int
    games_lost: int
    kda: float
    time_played: int
    winrate: float
    total: TotalStatsSummary
    average: AverageStatsSummary


class PlayerRolesStats(BaseModel):
    tank: Optional[StatsSummary] = None
    damage: Optional[StatsSummary] = None
    support: Optional[StatsSummary] = None


class PlayerStatsSummary(BaseModel):
    general: Optional[StatsSummary] = None
    roles: Optional[PlayerRolesStats] = None
    heroes: Optional[dict[Hero, StatsSummary]] = None


class SingleCareerStat(BaseModel):
    key: str
    label: str
    value: Number


class HeroCareerStats(BaseModel):
    """Career stats for a single hero, grouped by category (as returned by /stats)."""
    category: CareerStatCategory
    label: str
    stats: list[SingleCareerStat]


class HeroPlayerCareerStats(BaseModel):
    """Career stats for a single hero, as flat {label: value} maps keyed by category (as returned by /stats/career)."""
    assists: Optional[dict[str, Number]] = None
    average: Optional[dict[str, Number]] = None
    best: Optional[dict[str, Number]] = None
    combat: Optional[dict[str, Number]] = None
    game: Optional[dict[str, Number]] = None
    hero_specific: Optional[dict[str, Number]] = None
    match_awards: Optional[dict[str, Number]] = None
    miscellaneous: Optional[dict[str, Number]] = None


class HeroStat(BaseModel):
    hero: Hero
    value: Number


class HeroesStats(BaseModel):
    label: str
    values: list[HeroStat]


class HeroesComparisons(BaseModel):
    time_played: Optional[HeroesStats] = None
    games_won: Optional[HeroesStats] = None
    win_percentage: Optional[HeroesStats] = None
    weapon_accuracy_best_in_game: Optional[HeroesStats] = None
    eliminations_per_life: Optional[HeroesStats] = None
    kill_streak_best: Optional[HeroesStats] = None
    multikill_best: Optional[HeroesStats] = None
    eliminations_avg_per_10_min: Optional[HeroesStats] = None
    deaths_avg_per_10_min: Optional[HeroesStats] = None
    final_blows_avg_per_10_min: Optional[HeroesStats] = None
    solo_kills_avg_per_10_min: Optional[HeroesStats] = None
    objective_kills_avg_per_10_min: Optional[HeroesStats] = None
    objective_time_avg_per_10_min: Optional[HeroesStats] = None
    hero_damage_done_avg_per_10_min: Optional[HeroesStats] = None
    healing_done_avg_per_10_min: Optional[HeroesStats] = None


class PlayerGamemodeStats(BaseModel):
    heroes_comparisons: HeroesComparisons
    career_stats: dict[str, Optional[list[HeroCareerStats]]]


class PlayerPlatformStats(BaseModel):
    quickplay: Optional[PlayerGamemodeStats] = None
    competitive: Optional[PlayerGamemodeStats] = None


class PlayerStats(BaseModel):
    pc: Optional[PlayerPlatformStats] = None
    console: Optional[PlayerPlatformStats] = None