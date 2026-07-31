"""Accessors for supported unit catalog data."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, cast

from unit_converter._data import load_json_data


def get_unit_catalog() -> dict[str, Any]:
    """Return an isolated copy of the bundled supported-unit catalog."""

    return deepcopy(load_json_data("unit_catalog.json"))


def get_ui_unit_catalog() -> dict[str, Any]:
    """Return an isolated copy of the bundled UI-oriented unit catalog."""

    return deepcopy(load_json_data("ui_unit_catalog.json"))


def list_categories() -> tuple[str, ...]:
    """Return source grouping names from the original standard."""

    catalog = load_json_data("unit_catalog.json")
    categories = cast(list[dict[str, Any]], catalog["categories"])
    return tuple(str(category["name"]) for category in categories)


def list_units(category: str | None = None) -> tuple[str, ...]:
    """Return supported units globally or within a source group."""

    catalog = load_json_data("unit_catalog.json")
    if category is None:
        records = cast(list[dict[str, Any]], catalog["units"])
        return tuple(sorted(str(record["display_name"]) for record in records))

    categories = cast(list[dict[str, Any]], catalog["categories"])
    normalized_category = category.strip().casefold()
    for category_data in categories:
        if str(category_data["name"]).casefold() == normalized_category:
            return tuple(str(unit) for unit in cast(list[str], category_data["units"]))

    raise ValueError(
        f"Unknown category: {category!r}. Use list_categories() to see supported "
        "categories."
    )


def list_unit_ids(category: str | None = None) -> tuple[str, ...]:
    """Return stable unit IDs globally or within a source group."""

    unit_id_by_name = _unit_id_by_display_name()
    return tuple(unit_id_by_name[name] for name in list_units(category))


def list_ui_categories() -> tuple[str, ...]:
    """Return UI-oriented category names."""

    catalog = load_json_data("ui_unit_catalog.json")
    categories = cast(list[dict[str, Any]], catalog["categories"])
    return tuple(str(category["name"]) for category in categories)


def list_ui_subcategories(category: str) -> tuple[str, ...]:
    """Return UI-oriented subcategory names within ``category``."""

    category_data = _find_ui_category(category)
    return tuple(
        str(subcategory)
        for subcategory in cast(list[str], category_data["subcategories"])
    )


def list_ui_units(
    category: str,
    subcategory: str | None = None,
) -> tuple[str, ...]:
    """Return display names mapped to a UI category or subcategory."""

    category_data = _find_ui_category(category)
    canonical_category = str(category_data["name"])
    canonical_subcategory = _resolve_ui_subcategory(category_data, subcategory)
    catalog = load_json_data("unit_catalog.json")
    records = cast(list[dict[str, Any]], catalog["units"])

    return tuple(
        sorted(
            str(record["display_name"])
            for record in records
            if any(
                str(mapping["category"]) == canonical_category
                and (
                    canonical_subcategory is None
                    or str(mapping["subcategory"]) == canonical_subcategory
                )
                for mapping in cast(
                    list[dict[str, Any]],
                    record["ui_categories"],
                )
            )
        )
    )


def list_ui_unit_ids(
    category: str,
    subcategory: str | None = None,
) -> tuple[str, ...]:
    """Return stable IDs mapped to a UI category or subcategory."""

    unit_id_by_name = _unit_id_by_display_name()
    return tuple(
        unit_id_by_name[name] for name in list_ui_units(category, subcategory)
    )


def _unit_id_by_display_name() -> dict[str, str]:
    catalog = load_json_data("unit_catalog.json")
    records = cast(list[dict[str, Any]], catalog["units"])
    return {
        str(record["display_name"]): str(record["unit_id"]) for record in records
    }


def _find_ui_category(category: str) -> dict[str, Any]:
    catalog = load_json_data("ui_unit_catalog.json")
    categories = cast(list[dict[str, Any]], catalog["categories"])
    normalized_category = category.strip().casefold()
    for category_data in categories:
        if str(category_data["name"]).casefold() == normalized_category:
            return category_data
    raise ValueError(
        f"Unknown UI category: {category!r}. Use list_ui_categories() to see "
        "supported UI categories."
    )


def _resolve_ui_subcategory(
    category_data: dict[str, Any],
    subcategory: str | None,
) -> str | None:
    if subcategory is None:
        return None

    normalized_subcategory = subcategory.strip().casefold()
    subcategories = cast(list[str], category_data["subcategories"])
    for candidate in subcategories:
        if str(candidate).casefold() == normalized_subcategory:
            return str(candidate)
    raise ValueError(
        f"Unknown UI subcategory {subcategory!r} for "
        f"{category_data['name']!r}. Use list_ui_subcategories() to see "
        "supported UI subcategories."
    )
