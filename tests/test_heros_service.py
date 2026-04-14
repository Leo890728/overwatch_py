"""Heros service: URL/query construction and response parsing."""
from overwatch_py.enums import Hero, HeroGamemode, Locale, PlayerGamemode, Platform, Region, Role


async def test_get_heroes_builds_default_query(client, respx_mock):
    route = respx_mock.get("/heroes").respond(200, json=[])
    await client.get_heroes()
    assert route.called
    assert route.calls.last.request.url.params["locale"] == Locale.EN_US.value
    assert "role" not in route.calls.last.request.url.params
    assert "gamemode" not in route.calls.last.request.url.params


async def test_get_heroes_with_filters(client, respx_mock):
    route = respx_mock.get("/heroes").respond(200, json=[])
    await client.get_heroes(role=Role.TANK, gamemode=HeroGamemode.STADIUM, locale=Locale.ZH_TW)
    params = route.calls.last.request.url.params
    assert params["role"] == "tank"
    assert params["gamemode"] == "stadium"
    assert params["locale"] == "zh-tw"


async def test_get_heroes_parses_response(client, respx_mock):
    respx_mock.get("/heroes").respond(200, json=[
        {
            "key": "ana",
            "name": "Ana",
            "portrait": "https://example.com/ana.png",
            "role": "support",
            "gamemodes": ["quickplay", "stadium"],
        }
    ])
    result = await client.get_heroes()
    assert len(result) == 1
    assert result[0].key == Hero.ANA
    assert result[0].role == Role.SUPPORT
    assert HeroGamemode.STADIUM in result[0].gamemodes


async def test_get_hero_data_uses_key_in_path(client, respx_mock):
    route = respx_mock.get("/heroes/tracer").respond(200, json={
        "name": "Tracer",
        "description": "…",
        "portrait": None,
        "backgrounds": [],
        "role": "damage",
        "location": "London, England",
        "age": 26,
        "birthday": "1990-04-10",
        "hitpoints": None,
        "abilities": [],
        "stadium_powers": None,
        "story": {"summary": "…", "media": None, "chapters": []},
    })
    data = await client.get_hero_data(Hero.TRACER)
    assert route.called
    assert data.role == Role.DAMAGE


async def test_get_heroes_stats_requires_platform_and_gamemode(client, respx_mock):
    route = respx_mock.get("/heroes/stats").respond(200, json=[])
    await client.get_heroes_stats(
        platform=Platform.PC,
        gamemode=PlayerGamemode.COMPETITIVE,
        region=Region.AMERICAS,
    )
    params = route.calls.last.request.url.params
    assert params["platform"] == "pc"
    assert params["gamemode"] == "competitive"
    assert params["region"] == "americas"
    assert params["order_by"] == "hero:asc"