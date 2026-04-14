"""Ensure every Python enum still matches the API spec.

If any of these fail, either:
  - the API added a value → update the Python enum,
  - the API removed/renamed a value → update the Python enum + any callers,
  - the snapshot is outdated → refresh `tests/fixtures/openapi.json` and re-run.
"""
import pytest

from overwatch_py.enums import (
    BackgroundImageSize,
    CareerStatCategory,
    CompetitiveDivisionFilter,
    Hero,
    HeroGamemode,
    Locale,
    Map,
    MapGamemode,
    Platform,
    PlayerGamemode,
    Rank,
    Region,
    Role,
)


def _spec_enum(spec: dict, schema_name: str) -> set[str]:
    return set(spec["components"]["schemas"][schema_name]["enum"])


ENUM_TO_SCHEMA = [
    (Role, "Role"),
    (Hero, "HeroKey"),
    (Locale, "Locale"),
    (Platform, "PlayerPlatform"),
    (Region, "PlayerRegion"),
    (PlayerGamemode, "PlayerGamemode"),
    (HeroGamemode, "HeroGamemode"),
    (Map, "MapKey"),
    (MapGamemode, "MapGamemode"),
    (Rank, "CompetitiveDivision"),
    (CompetitiveDivisionFilter, "CompetitiveDivisionFilter"),
    (BackgroundImageSize, "BackgroundImageSize"),
    (CareerStatCategory, "CareerStatCategory"),
]


@pytest.mark.parametrize("enum_cls,schema_name", ENUM_TO_SCHEMA, ids=[n for _, n in ENUM_TO_SCHEMA])
def test_enum_matches_spec(openapi_spec, enum_cls, schema_name):
    spec_values = _spec_enum(openapi_spec, schema_name)
    enum_values = {e.value for e in enum_cls}
    missing_in_python = spec_values - enum_values
    extra_in_python = enum_values - spec_values
    assert not missing_in_python, f"{enum_cls.__name__} is missing values present in API: {missing_in_python}"
    assert not extra_in_python, f"{enum_cls.__name__} has values not in API: {extra_in_python}"