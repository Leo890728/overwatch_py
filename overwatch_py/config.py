from typing import Literal

from pydantic import BaseModel, HttpUrl


class Config(BaseModel):
    base_url: HttpUrl = "https://overfast-api.tekrop.fr"
    timeout: int = 10
    retries: int = 3
    cache: bool = False
    cache_backend: Literal["memory", "sqlite", "file"] = "memory"