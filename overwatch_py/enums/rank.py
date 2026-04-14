from enum import Enum


class Rank(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"
    MASTER = "master"
    GRANDMASTER = "grandmaster"
    ULTIMATE = "ultimate"


class CompetitiveDivisionFilter(str, Enum):
    """Same as Rank, but without ULTIMATE — accepted by /heroes/stats `competitive_division` query."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"
    MASTER = "master"
    GRANDMASTER = "grandmaster"
