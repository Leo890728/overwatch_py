import hishel
import httpx

from httpx_retries import Retry, RetryTransport

from .config import Config
from .exceptions import *


class HTTPSession:
    def __init__(self, config: Config = None):
        self.config = config or Config()
        retry = Retry(
            total=self.config.retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        transport: httpx.AsyncBaseTransport = RetryTransport(retry=retry)

        if self.config.cache:
            transport = hishel.AsyncCacheTransport(
                transport=transport,
                storage=self._make_storage(),
            )

        self.transport = transport
        self.client = httpx.AsyncClient(
            base_url=str(self.config.base_url),
            transport=self.transport,
            timeout=self.config.timeout,
        )

    def _make_storage(self) -> hishel.AsyncBaseStorage:
        match self.config.cache_backend:
            case "memory":
                return hishel.AsyncInMemoryStorage()
            case "sqlite":
                return hishel.AsyncSQLiteStorage()
            case "file":
                return hishel.AsyncFileStorage()

    async def get(self, path, **kwargs):
        resp = await self.client.get(path, **kwargs)
        match resp.status_code:
            case 400:
                raise BadRequestError(resp.text, resp.status_code, resp)
            case 404:
                raise NotFoundError(resp.text, resp.status_code, resp)
            case 422:
                raise ValidationError(resp.text, resp.status_code, resp)
            case 429:
                raise APIRateLimitError(resp.text, resp.status_code, resp)
            case 500:
                raise InternalServerError(resp.text, resp.status_code, resp)
            case 503:
                raise BlizzardRateLimitError(resp.text, resp.status_code, resp)
            case 504:
                raise BlizzardServerError(resp.text, resp.status_code, resp)
            case _:
                resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()