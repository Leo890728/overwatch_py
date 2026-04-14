from typing import Optional

from ..enums import MapGamemode
from ..session import HTTPSession
from ..models import GamemodeDetails, MapDetails


class MapsService:
    def __init__(self, session: HTTPSession):
        self.session = session

    async def get_maps(self, map_gamemode: Optional[MapGamemode] = None) -> list[MapDetails]:
        """Get a list of Overwatch maps : Hanamura, King's Row, Dorado, etc."""
        params = {}
        if map_gamemode is not None:
            params["gamemode"] = map_gamemode.value
        return list(map(lambda data: MapDetails(**data), await self.session.get("/maps", params=params)))

    async def get_gamemode_details(self) -> list[GamemodeDetails]:
        """Get a list of Overwatch gamemodes : Assault, Escort, Flashpoint, Hybrid, etc."""
        return list(map(lambda data: GamemodeDetails(**data), await self.session.get("/gamemodes")))