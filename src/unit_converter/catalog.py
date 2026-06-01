"""Accessors for supported unit catalog data."""

from __future__ import annotations

import json
from functools import cache
from importlib.resources import files
from typing import Any, cast


@cache
def get_unit_catalog() -> dict[str, Any]:
    """Return the bundled supported-unit catalog."""

    return _load_json_data("unit_catalog.json")


@cache
def get_ui_unit_catalog() -> dict[str, Any]:
    """Return the bundled UI-oriented supported-unit catalog."""

    return _load_json_data("ui_unit_catalog.json")


def list_categories() -> tuple[str, ...]:
    """Return source grouping names from the original standard."""

    catalog = get_unit_catalog()
    categories = cast(list[dict[str, Any]], catalog["categories"])
    return tuple(str(category["name"]) for category in categories)


def list_units(category: str | None = None) -> tuple[str, ...]:
    """Return supported units globally or within a source group."""

    catalog = get_unit_catalog()
    if category is None:
        return tuple(str(unit) for unit in cast(list[str], catalog["all_units"]))

    categories = cast(list[dict[str, Any]], catalog["categories"])
    normalized_category = category.strip().casefold()
    for category_data in categories:
        if str(category_data["name"]).casefold() == normalized_category:
            return tuple(str(unit) for unit in cast(list[str], category_data["units"]))

    raise ValueError(
        f"Unknown category: {category!r}. Use list_categories() to see supported "
        "categories."
    )


def _load_json_data(filename: str) -> dict[str, Any]:
    data_path = files("unit_converter.data").joinpath(filename)
    with data_path.open(encoding="utf-8") as handle:
        return cast(dict[str, Any], json.load(handle))
