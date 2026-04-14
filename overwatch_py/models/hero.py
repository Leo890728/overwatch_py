from typing import Optional

from pydantic import BaseModel, HttpUrl

from ..enums import BackgroundImageSize, Role


class HeroData(BaseModel):
    name: str
    description: str
    portrait: Optional[HttpUrl] = None
    backgrounds: list["HeroBackground"]
    role: Role
    location: str
    age: Optional[int]
    birthday: Optional[str]
    hitpoints: Optional["HitPoints"] = None
    abilities: list["Ability"]
    stadium_powers: Optional[list["StadiumPower"]] = None
    story: "Story"


class HeroBackground(BaseModel):
    url: HttpUrl
    sizes: list[BackgroundImageSize]


class AbilityVideoLink(BaseModel):
    mp4: HttpUrl
    webm: HttpUrl


class AbilityVideo(BaseModel):
    thumbnail: HttpUrl
    link: AbilityVideoLink


class Media(BaseModel):
    type: str
    link: HttpUrl


class HitPoints(BaseModel):
    health: int
    armor: int
    shields: int
    total: int


class Ability(BaseModel):
    name: str
    description: str
    icon: HttpUrl
    video: AbilityVideo


class StadiumPower(BaseModel):
    name: str
    description: str
    icon: HttpUrl


class Story(BaseModel):
    summary: str
    media: Optional[Media] = None
    chapters: list["Chapter"]


class Chapter(BaseModel):
    title: str
    content: str
    picture: HttpUrl
