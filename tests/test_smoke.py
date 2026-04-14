"""Smoke tests — verifies the package imports and the fixture wiring works.

Replace / expand these with real tests under tests/ (step 2).
"""
import pytest


def test_package_imports():
    import overwatch_py
    assert hasattr(overwatch_py, "Client")


def test_client_fixture(client):
    assert client.session is not None
    assert client.heros is not None
    assert client.maps is not None
    assert client.players is not None


@pytest.mark.asyncio
async def test_respx_fixture_stubs_get(client, respx_mock):
    respx_mock.get("/heroes").respond(200, json=[])
    result = await client.get_heroes()
    assert result == []
