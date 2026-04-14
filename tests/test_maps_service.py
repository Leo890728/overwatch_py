"""Maps service: URL/query construction and response parsing."""
from overwatch_py.enums import Map, MapGamemode


async def test_get_maps_no_filter(client, respx_mock):
    route = respx_mock.get("/maps").respond(200, json=[])
    await client.get_maps()
    assert route.called
    assert "gamemode" not in route.calls.last.request.url.params


async def test_get_maps_with_gamemode(client, respx_mock):
    route = respx_mock.get("/maps").respond(200, json=[])
    await client.get_maps(MapGamemode.PUSH)
    assert route.calls.last.request.url.params["gamemode"] == "push"


async def test_get_maps_parses_response(client, respx_mock):
    respx_mock.get("/maps").respond(200, json=[
        {
            "key": "busan",
            "name": "Busan",
            "screenshot": "https://example.com/busan.jpg",
            "gamemodes": ["control"],
            "location": "South Korea",
            "country_code": "KR",
        }
    ])
    result = await client.get_maps()
    assert result[0].key == Map.BUSAN
    assert MapGamemode.CONTROL in result[0].gamemodes


async def test_get_gamemode_details(client, respx_mock):
    route = respx_mock.get("/gamemodes").respond(200, json=[
        {
            "key": "push",
            "name": "Push",
            "icon": "https://example.com/push.svg",
            "screenshot": "https://example.com/push.jpg",
            "description": "…",
        }
    ])
    result = await client.get_gamemode_details()
    assert route.called
    assert result[0].key == MapGamemode.PUSH