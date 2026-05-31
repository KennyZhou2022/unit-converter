#!/usr/bin/env python
"""Convert reviewed CSV conversion rules into package JSON data."""

from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


FROM_HEADERS = {"convert_from", "convert from", "from", "source", "unit_from"}
TO_HEADERS = {"convert_to", "convert to", "to", "target", "unit_to"}
RULE_HEADERS = {"rule", "factor", "formula", "multiplier", "multiplier_or_formula"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--source-name")
    parser.add_argument("--source-document")
    args = parser.parse_args()

    rows = read_conversion_rows(args.input_csv)
    payload = {
        "version": 1,
        "source": {
            "name": args.source_name,
            "document": args.source_document,
        },
        "conversions": [normalize_row(row) for row in rows],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def read_conversion_rows(path: Path) -> list[tuple[str, str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))

    rows = [row for row in rows if row and any(cell.strip() for cell in row)]
    if not rows:
        return []

    header = [_normalize_header(cell) for cell in rows[0]]
    header_indexes = _header_indexes(header)
    if header_indexes is not None:
        from_index, to_index, rule_index = header_indexes
        data_rows = rows[1:]
    else:
        from_index, to_index, rule_index = 0, 1, 2
        data_rows = rows

    return [
        (row[from_index].strip(), row[to_index].strip(), row[rule_index].strip())
        for row in data_rows
        if len(row) > max(from_index, to_index, rule_index)
    ]


def normalize_row(row: tuple[str, str, str]) -> dict[str, str]:
    from_unit, to_unit, rule = row
    if not from_unit or not to_unit or not rule:
        raise ValueError(f"Incomplete conversion row: {row!r}")

    normalized = {
        "from": from_unit,
        "to": to_unit,
    }
    if _is_decimal(rule):
        normalized["factor"] = rule
    else:
        normalized["formula"] = rule
    return normalized


def _normalize_header(value: str) -> str:
    return value.strip().lower().replace("-", "_")


def _header_indexes(header: list[str]) -> tuple[int, int, int] | None:
    from_index = _find_header(header, FROM_HEADERS)
    to_index = _find_header(header, TO_HEADERS)
    rule_index = _find_header(header, RULE_HEADERS)
    if from_index is None or to_index is None or rule_index is None:
        return None
    return from_index, to_index, rule_index


def _find_header(header: list[str], candidates: set[str]) -> int | None:
    for index, value in enumerate(header):
        if value in candidates:
            return index
    return None


def _is_decimal(value: str) -> bool:
    try:
        Decimal(value)
    except InvalidOperation:
        return False
    return True


if __name__ == "__main__":
    main()
