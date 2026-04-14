from pydantic import BaseModel, HttpUrl

from ..enums import Hero, HeroGamemode, Role


class HeroShort(BaseModel):
    key: Hero
    name: str
    portrait: HttpUrl
    role: Role
    gamemodes: list[HeroGamemode]
