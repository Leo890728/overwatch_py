from typing import Optional
from pydantic import BaseModel, HttpUrl

from ..enums import Map, MapGamemode


class MapDetails(BaseModel):
    key: Map
    name: str
    screenshot: HttpUrl
    gamemodes: list[MapGamemode]
    location: str
    country_code: Optional[str]