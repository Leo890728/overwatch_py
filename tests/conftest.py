import json
from pathlib import Path

import pytest
import respx

from overwatch_py import Client
from overwatch_py.config import Config
from overwatch_py.session import HTTPSession


BASE_URL = "https://overfast-api.tekrop.fr"
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def client() -> Client:
    """A Client pointed at BASE_URL with cache disabled — tests use `respx_mock` to stub HTTP."""
    return Client(HTTPSession(Config(base_url=BASE_URL, retries=0, cache=False)))


@pytest.fixture
def respx_mock():
    with respx.mock(base_url=BASE_URL, assert_all_called=False) as mock:
        yield mock


@pytest.fixture(scope="session")
def openapi_spec() -> dict:
    """OpenAPI spec snapshot. Refresh `tests/fixtures/openapi.json` when the API changes."""
    return json.loads((FIXTURES / "openapi.json").read_text(encoding="utf-8"))