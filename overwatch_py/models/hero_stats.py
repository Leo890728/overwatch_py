from pydantic import BaseModel

from ..enums import Hero


class HeroStats(BaseModel):
    hero: Hero
    pickrate: float
    winrate: float