#!/usr/bin/env python
"""Maintain stable unit and physical-quantity identifiers."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONVERSIONS_PATH = REPO_ROOT / "src" / "unit_converter" / "data" / "conversions.json"
ALIASES_PATH = REPO_ROOT / "data" / "overrides" / "unit_aliases.json"
REGISTRY_PATH = REPO_ROOT / "data" / "registry" / "unit_registry.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    conversions = load_json(CONVERSIONS_PATH)["conversions"]
    aliases = load_aliases(ALIASES_PATH)
    existing = load_json(REGISTRY_PATH) if REGISTRY_PATH.exists() else None
    registry = build_registry(conversions, aliases, existing)

    if args.check:
        if existing != registry:
            raise SystemExit(
                "unit_registry.json is stale; run scripts/generate_unit_registry.py"
            )
        print("unit_registry.json is up to date.")
        return

    write_json(REGISTRY_PATH, registry)
    print(f"Wrote {REGISTRY_PATH.relative_to(REPO_ROOT)}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_aliases(path: Path) -> dict[str, tuple[str, ...]]:
    payload = load_json(path)
    result: dict[str, tuple[str, ...]] = {}
    for record in payload["units"]:
        display_name = str(record["display_name"])
        if display_name in result:
            raise ValueError(f"Duplicate alias record for {display_name!r}.")
        result[display_name] = tuple(str(alias) for alias in record["aliases"])
    return result


def build_registry(
    conversions: list[dict[str, Any]],
    aliases: dict[str, tuple[str, ...]],
    existing: dict[str, Any] | None,
) -> dict[str, Any]:
    components = conversion_components(conversions)
    supported_units = {unit for component in components for unit in component}
    unknown_alias_targets = sorted(set(aliases) - supported_units)
    if unknown_alias_targets:
        raise ValueError(
            f"Alias records reference unsupported units: {unknown_alias_targets}"
        )

    existing_records = [] if existing is None else existing["units"]
    existing_by_key = index_existing_records(existing_records)
    next_unit_number = next_identifier_number(
        (record["unit_id"] for record in existing_records),
        r"unit\.u(\d+)",
    )
    next_quantity_number = next_identifier_number(
        (record["quantity_id"] for record in existing_records),
        r"quantity\.q(\d+)",
    )

    records_by_name: dict[str, dict[str, Any]] = {}
    used_existing_ids: set[str] = set()
    for display_name in sorted(supported_units):
        configured_aliases = aliases.get(display_name, ())
        existing_record = find_existing_record(
            display_name,
            configured_aliases,
            existing_by_key,
        )
        if existing_record is None:
            unit_id = f"unit.u{next_unit_number:04d}"
            next_unit_number += 1
            quantity_id = None
        else:
            unit_id = str(existing_record["unit_id"])
            quantity_id = str(existing_record["quantity_id"])
            used_existing_ids.add(unit_id)
        records_by_name[display_name] = {
            "unit_id": unit_id,
            "quantity_id": quantity_id,
            "display_name": display_name,
            "aliases": list(configured_aliases),
        }

    removed_ids = sorted(
        {
            str(record["unit_id"])
            for record in existing_records
            if record["unit_id"] not in used_existing_ids
        }
    )
    if removed_ids:
        raise ValueError(
            "Existing unit IDs would be removed; migrate or retire them explicitly: "
            f"{removed_ids}"
        )

    quantity_components: dict[str, tuple[str, ...]] = {}
    for component in components:
        existing_quantity_ids = {
            records_by_name[unit]["quantity_id"]
            for unit in component
            if records_by_name[unit]["quantity_id"] is not None
        }
        if len(existing_quantity_ids) > 1:
            raise ValueError(
                "A conversion component would merge stable quantity IDs: "
                f"{sorted(existing_quantity_ids)}"
            )
        if existing_quantity_ids:
            quantity_id = str(existing_quantity_ids.pop())
        else:
            quantity_id = f"quantity.q{next_quantity_number:04d}"
            next_quantity_number += 1
        if quantity_id in quantity_components:
            raise ValueError(
                f"Stable quantity ID {quantity_id!r} was split across components."
            )
        quantity_components[quantity_id] = component
        for unit in component:
            records_by_name[unit]["quantity_id"] = quantity_id

    records = [records_by_name[name] for name in sorted(records_by_name)]
    validate_registry_records(records)
    return {
        "version": 1,
        "totals": {
            "unit_count": len(records),
            "quantity_count": len(quantity_components),
            "alias_count": sum(len(record["aliases"]) for record in records),
        },
        "units": records,
    }


def index_existing_records(
    records: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for record in records:
        keys = [
            str(record["unit_id"]),
            str(record["display_name"]),
            *(str(alias) for alias in record["aliases"]),
        ]
        for key in keys:
            previous = index.get(key)
            if previous is not None and previous["unit_id"] != record["unit_id"]:
                raise ValueError(f"Registry key {key!r} resolves to multiple units.")
            index[key] = record
    return index


def find_existing_record(
    display_name: str,
    aliases: tuple[str, ...],
    existing_by_key: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    matches = {
        str(record["unit_id"]): record
        for key in (display_name, *aliases)
        if (record := existing_by_key.get(key)) is not None
    }
    if len(matches) > 1:
        raise ValueError(
            f"Unit {display_name!r} matches multiple existing IDs: {sorted(matches)}"
        )
    return next(iter(matches.values()), None)


def conversion_components(
    conversions: list[dict[str, Any]],
) -> list[tuple[str, ...]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for conversion in conversions:
        from_unit = str(conversion["from"])
        to_unit = str(conversion["to"])
        adjacency[from_unit].add(to_unit)
        adjacency[to_unit].add(from_unit)

    components: list[tuple[str, ...]] = []
    remaining = set(adjacency)
    while remaining:
        pending = [min(remaining)]
        component: set[str] = set()
        while pending:
            unit = pending.pop()
            if unit in component:
                continue
            component.add(unit)
            remaining.discard(unit)
            pending.extend(sorted(adjacency[unit] - component, reverse=True))
        components.append(tuple(sorted(component)))
    return sorted(components, key=lambda component: component[0])


def next_identifier_number(values: Any, pattern: str) -> int:
    numbers = []
    for value in values:
        match = re.fullmatch(pattern, str(value))
        if match is None:
            raise ValueError(f"Invalid stable identifier: {value!r}.")
        numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def validate_registry_records(records: list[dict[str, Any]]) -> None:
    unit_ids = [str(record["unit_id"]) for record in records]
    if len(unit_ids) != len(set(unit_ids)):
        raise ValueError("Stable unit IDs must be unique.")

    resolution_keys: dict[str, str] = {}
    for record in records:
        unit_id = str(record["unit_id"])
        for key in (
            unit_id,
            str(record["display_name"]),
            *(str(alias) for alias in record["aliases"]),
        ):
            previous = resolution_keys.get(key)
            if previous is not None and previous != unit_id:
                raise ValueError(f"Unit lookup key {key!r} is ambiguous.")
            resolution_keys[key] = unit_id


if __name__ == "__main__":
    main()
