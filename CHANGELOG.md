# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-14

### Added
- Initial release.
- Async client for the [OverFast API](https://overfast-api.tekrop.fr/) built on `httpx`.
- Services: `HeroesService`, `MapsService`, `GamemodesService`, `RolesService`, `PlayersService`.
- Pydantic v2 models for heroes, maps, gamemodes, roles, and player data (summary, stats, career, search).
- Enums synchronized with the OverFast API schema: `Hero`, `Role`, `Region`, `Platform`, `Rank`, `CompetitiveDivisionFilter`, `HeroGamemode`, `PlayerGamemode`, `Privacy`, `BackgroundImageSize`, `CareerStatCategory`.
- HTTP-layer caching via [hishel](https://hishel.com) (memory / sqlite / file backends), opt-in through `ClientConfig.cache`.
- Automatic retries for transient failures via `httpx-retries`.
- Typed exceptions mapped to OverFast API responses: `BadRequestError` (400), `NotFoundError` (404), `ValidationError` (422), `RateLimitError` (429), `InternalServerError` (500), `ServiceUnavailableError` (503), `ParserBlizzardError` (504).
- `py.typed` marker for PEP 561 type-checker support.

[Unreleased]: https://github.com/Leo890728/overwatch_py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Leo890728/overwatch_py/releases/tag/v0.1.0