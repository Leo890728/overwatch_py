# overfast-client

Async Python client for the [OverFast API](https://overfast-api.tekrop.fr) — comprehensive Overwatch data (heroes, maps, gamemodes, player stats) via a typed, pydantic-backed interface.

## Install

```bash
pip install overfast-client
```

> The PyPI distribution is `overfast-client`; the import name is `overwatch_py`.

Or from source (editable):

```bash
pip install -e .
```

## Quick start

```python
import asyncio
from overwatch_py import Client
from overwatch_py.enums import Hero, Locale, Role, HeroGamemode, PlayerGamemode, Platform

async def main():
    client = Client()

    # List heroes
    heroes = await client.get_heroes(role=Role.SUPPORT, locale=Locale.EN_US)
    for h in heroes:
        print(h.key, h.name)

    # Full hero data (abilities, story, hitpoints, ...)
    ana = await client.get_hero_data(Hero.ANA)
    print(ana.hitpoints, len(ana.abilities))

    # Maps & gamemodes
    maps = await client.get_maps()
    gamemodes = await client.get_gamemode_details()

    # Hero usage stats (pickrate / winrate)
    stats = await client.get_heroes_stats(
        platform=Platform.PC,
        gamemode=PlayerGamemode.COMPETITIVE,
    )

    # Players
    result = await client.search_players("TeKrop", limit=10)
    player = await client.get_player(result.results[0].player_id)
    summary = await client.get_player_summary("TeKrop-2217")
    stats_summary = await client.get_player_stats("TeKrop-2217", gamemode=PlayerGamemode.COMPETITIVE)

asyncio.run(main())
```

## Configuration

```python
from overwatch_py import Client
from overwatch_py.config import Config
from overwatch_py.session import HTTPSession

config = Config(
    timeout=10,          # seconds
    retries=3,           # retries on 5xx
    cache=True,          # HTTP-level cache (hishel), respects server Cache-Control
    cache_backend="sqlite",  # "memory" | "sqlite" | "file"
)
client = Client(HTTPSession(config))
```

### Caching

Caching is disabled by default. When enabled, [hishel](https://hishel.com) sits in the httpx transport stack and honors each endpoint's `Cache-Control` / `Age` headers (e.g. `/heroes` is cached ~1 day, `/heroes/stats` ~1 hour by the upstream API).

## Exceptions

All non-2xx responses map to subclasses of `APIError`:

| Status | Exception |
|--------|-----------|
| 400    | `BadRequestError` |
| 404    | `NotFoundError` |
| 422    | `ValidationError` |
| 429    | `APIRateLimitError` |
| 500    | `InternalServerError` |
| 503    | `BlizzardRateLimitError` |
| 504    | `BlizzardServerError` |

```python
from overwatch_py.exceptions import NotFoundError, APIRateLimitError

try:
    await client.get_player_summary("does-not-exist-1234")
except NotFoundError:
    ...
except APIRateLimitError as e:
    print("rate limited:", e.response.headers.get("retry-after"))
```

## API surface

Exposed on `Client`:

- **Heroes** — `get_heroes`, `get_hero_data`, `get_heroes_stats`
- **Maps / Gamemodes** — `get_maps`, `get_gamemode_details`
- **Players** — `search_players`, `get_player`, `get_player_summary`, `get_player_stats`, `get_player_career_stats`, `get_player_career_stats_with_labels`, `get_player_full_stats`

The underlying services (`client.heros`, `client.maps`, `client.players`) are also available if you prefer service-level access.

### Career stats: flat vs. with labels

Two shapes are available for the same underlying data:

```python
from overwatch_py.enums import Hero, PlayerGamemode

# Flat: {hero_key: {category: {stat_label: value}}} — best for lookups
flat = await client.get_player_career_stats(
    "TeKrop-2217", gamemode=PlayerGamemode.COMPETITIVE, hero=Hero.ANA,
)
eliminations = flat["ana"].combat["eliminations"]

# With labels: {hero_key: [HeroCareerStats, ...]} — preserves category/label order
labeled = await client.get_player_career_stats_with_labels(
    "TeKrop-2217", gamemode=PlayerGamemode.COMPETITIVE, hero=Hero.ANA,
)
for group in labeled["ana"]:
    print(group.category, [(s.label, s.value) for s in group.stats])
```

`hero` accepts a `Hero` enum, the literal string `"all-heroes"` (aggregate across heroes), or `None` (all heroes, keyed individually).

### Return types

All responses are pydantic models — use your IDE's autocomplete, or see [overwatch_py/models/](overwatch_py/models/). Example for `get_player_summary`:

```python
summary = await client.get_player_summary("TeKrop-2217")
summary.username                              # str
summary.endorsement.level                     # int
summary.competitive.pc.support.division       # Rank enum
summary.competitive.pc.support.tier           # int
```

Available enums live in [overwatch_py/enums/](overwatch_py/enums/) (`Hero`, `Map`, `Role`, `Platform`, `Region`, `Locale`, `Rank`, `PlayerGamemode`, `HeroGamemode`, `MapGamemode`, `CompetitiveDivisionFilter`).

## Development

```bash
pip install -e ".[dev]"
pytest                     # unit + mocked HTTP tests
pytest -m live             # hits the real API (rate-limited)
pytest -m 'live or not live'  # run everything
```

## License

MIT.