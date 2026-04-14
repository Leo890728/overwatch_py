"""HTTP status code → exception class mapping."""
import pytest

from overwatch_py.exceptions import (
    APIError,
    APIRateLimitError,
    BadRequestError,
    BlizzardRateLimitError,
    BlizzardServerError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)


STATUS_TO_EXCEPTION = [
    (400, BadRequestError),
    (404, NotFoundError),
    (422, ValidationError),
    (429, APIRateLimitError),
    (500, InternalServerError),
    (503, BlizzardRateLimitError),
    (504, BlizzardServerError),
]


@pytest.mark.parametrize("status,exc", STATUS_TO_EXCEPTION, ids=[f"{s}-{e.__name__}" for s, e in STATUS_TO_EXCEPTION])
async def test_status_maps_to_exception(client, respx_mock, status, exc):
    respx_mock.get("/heroes").respond(status, json={"error": "x"})
    with pytest.raises(exc) as info:
        await client.get_heroes()
    assert info.value.status_code == status
    assert info.value.response is not None


async def test_all_api_errors_share_base(client, respx_mock):
    """Any API exception should still be catchable as APIError."""
    respx_mock.get("/heroes").respond(404)
    with pytest.raises(APIError):
        await client.get_heroes()


async def test_unmapped_4xx_falls_through(client, respx_mock):
    """Unmapped status codes should raise httpx's HTTPStatusError rather than silently succeed."""
    import httpx
    respx_mock.get("/heroes").respond(418)
    with pytest.raises(httpx.HTTPStatusError):
        await client.get_heroes()