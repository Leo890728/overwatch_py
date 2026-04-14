"""Players service: URL/query construction, hero filter handling, response parsing."""
from overwatch_py.enums import Hero, Platform, PlayerGamemode


async def test_search_players_required_name(client, respx_mock):
    route = respx_mock.get("/players").respond(200, json={"total": 0, "results": []})
    await client.search_players("TeKrop")
    assert route.calls.last.request.url.params["name"] == "TeKrop"


async def test_search_players_optional_params(client, respx_mock):
    route = respx_mock.get("/players").respond(200, json={"total": 0, "results": []})
    await client.search_players("x", order_by="name:asc", offset=20, limit=10)
    p = route.calls.last.request.url.params
    assert p["order_by"] == "name:asc"
    assert p["offset"] == "20"
    assert p["limit"] == "10"


async def test_search_players_parses_results(client, respx_mock):
    respx_mock.get("/players").respond(200, json={
        "total": 1,
        "results": [{
            "player_id": "TeKrop-2217",
            "name": "TeKrop",
            "avatar": "https://example.com/a.png",
            "namecard": None,
            "title": None,
            "career_url": "https://overfast-api.tekrop.fr/players/TeKrop-2217",
            "blizzard_id": "abc",
            "last_updated_at": 1704209332,
            "is_public": True,
        }],
    })
    result = await client.search_players("TeKrop")
    assert result.total == 1
    assert result.results[0].player_id == "TeKrop-2217"


async def test_get_player_summary_path(client, respx_mock):
    route = respx_mock.get("/players/TeKrop-2217/summary").respond(200, json={
        "username": "TeKrop",
        "avatar": None, "namecard": None, "title": None,
        "endorsement": None, "competitive": None, "last_updated_at": None,
    })
    summary = await client.get_player_summary("TeKrop-2217")
    assert route.called
    assert summary.username == "TeKrop"


async def test_get_player_career_stats_with_hero_enum(client, respx_mock):
    route = respx_mock.get("/players/x/stats/career").respond(200, json={
        "ana": {"combat": {"eliminations": 1}},
    })
    result = await client.get_player_career_stats(
        "x", gamemode=PlayerGamemode.COMPETITIVE, platform=Platform.PC, hero=Hero.ANA,
    )
    p = route.calls.last.request.url.params
    assert p["gamemode"] == "competitive"
    assert p["platform"] == "pc"
    assert p["hero"] == "ana"
    assert result["ana"].combat == {"eliminations": 1}


async def test_get_player_career_stats_with_all_heroes_literal(client, respx_mock):
    route = respx_mock.get("/players/x/stats/career").respond(200, json={
        "all-heroes": {"combat": {"eliminations": 42}},
    })
    result = await client.get_player_career_stats(
        "x", gamemode=PlayerGamemode.COMPETITIVE, hero="all-heroes",
    )
    assert route.calls.last.request.url.params["hero"] == "all-heroes"
    assert result["all-heroes"].combat["eliminations"] == 42


async def test_get_player_stats_summary_optional_params(client, respx_mock):
    route = respx_mock.get("/players/x/stats/summary").respond(200, json={})
    await client.get_player_stats("x")
    assert route.called
    assert "gamemode" not in route.calls.last.request.url.params
    assert "platform" not in route.calls.last.request.url.params