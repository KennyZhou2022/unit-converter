#!/usr/bin/env python
"""Generate the MkDocs supported-units page from unit_catalog.json."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any, cast


CATALOG_PATH = Path("src/unit_converter/data/unit_catalog.json")
OUTPUT_PATH = Path("docs/supported-units.md")


def main() -> None:
    catalog = cast(dict[str, Any], json.loads(CATALOG_PATH.read_text(encoding="utf-8")))
    OUTPUT_PATH.write_text(render(catalog), encoding="utf-8")


def render(catalog: dict[str, Any]) -> str:
    totals = cast(dict[str, int], catalog["totals"])
    categories = cast(list[dict[str, Any]], catalog["categories"])
    lines = [
        "# Supported Units",
        "",
        "This page is generated from `src/unit_converter/data/unit_catalog.json`.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Categories | {totals['category_count']} |",
        f"| Direct conversion rules | {totals['direct_conversion_count']} |",
        f"| Unique supported units | {totals['unit_count']} |",
        "| Ordered convertible unit pairs | "
        f"{totals['ordered_convertible_pair_count']} |",
        "",
        "## Browse By Category",
        "",
        '<div class="unit-filter-panel">',
        '  <label for="unit-category-filter">Category</label>',
        '  <select id="unit-category-filter" class="unit-filter-select">',
        '    <option value="__all__">All categories</option>',
    ]
    for category in categories:
        lines.append(
            "    <option value=\"{slug}\">{name} ({unit_count} units)</option>"
            .format(
                slug=escape(str(category["slug"]), quote=True),
                name=escape(str(category["name"])),
                unit_count=category["unit_count"],
            )
        )
    lines.extend(
        [
            "  </select>",
            '  <p id="unit-filter-count" class="unit-filter-count"></p>',
            "</div>",
            "",
            '<div id="unit-category-list">',
        ]
    )
    for category in categories:
        lines.extend(render_category(category))
    lines.append("</div>")

    lines.append("")
    return "\n".join(lines)


def render_category(category: dict[str, Any]) -> list[str]:
    units = cast(list[str], category["units"])
    slug = str(category["slug"])
    name = str(category["name"])
    lines = [
        (
            '<section class="unit-category" data-category="{slug}" '
            'data-category-name="{name}" data-unit-count="{unit_count}">'
        ).format(
            slug=escape(slug, quote=True),
            name=escape(name, quote=True),
            unit_count=len(units),
        ),
        f'<h2 id="{escape(slug, quote=True)}">{escape(name)}</h2>',
        f'<p class="unit-category-count">{len(units)} supported units</p>',
        "<table>",
        "  <thead>",
        "    <tr><th>Unit</th></tr>",
        "  </thead>",
        "  <tbody>",
    ]
    for unit in units:
        lines.append(f"    <tr><td><code>{escape(unit)}</code></td></tr>")
    lines.extend(
        [
            "  </tbody>",
            "</table>",
            "</section>",
            "",
        ]
    )
    return lines


if __name__ == "__main__":
    main()
