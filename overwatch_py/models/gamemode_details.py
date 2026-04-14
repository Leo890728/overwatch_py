from pydantic import BaseModel, HttpUrl

from ..enums import MapGamemode


class GamemodeDetails(BaseModel):
    key: MapGamemode
    name: str
    icon: HttpUrl
    screenshot: HttpUrl
    description: str