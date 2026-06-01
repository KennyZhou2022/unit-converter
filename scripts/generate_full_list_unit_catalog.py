"""Generate a development-only full-list unit catalog.

The generated JSON stores candidate unit labels by display category. It is a
coverage planning aid and is not used by the runtime converter.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = REPO_ROOT / "data" / "external" / "full_list_unit_catalog.json"
USER_AGENT = "Mozilla/5.0"

DISPLAY_CATEGORY_ORDER = [
    "Dimension Converters",
    "Mechanics Converters",
    "Heat Converters",
    "Fluids Converters",
    "Light Converters",
    "Electricity Converters",
    "Magnetism Converters",
    "Radiology Converters",
    "Miscellaneous Converters",
]

DISPLAY_CATEGORY_BY_SUBCATEGORY = {
    "Length": "Dimension Converters",
    "Area": "Dimension Converters",
    "Volume": "Dimension Converters",
    "Volume - Dry": "Dimension Converters",
    "Angle": "Dimension Converters",
    "Volume - Lumber": "Dimension Converters",
    "Weight and Mass": "Mechanics Converters",
    "Time": "Mechanics Converters",
    "Speed": "Mechanics Converters",
    "Velocity - Angular": "Mechanics Converters",
    "Acceleration": "Mechanics Converters",
    "Acceleration - Angular": "Mechanics Converters",
    "Force": "Mechanics Converters",
    "Pressure": "Mechanics Converters",
    "Energy": "Mechanics Converters",
    "Power": "Mechanics Converters",
    "Density": "Mechanics Converters",
    "Specific Volume": "Mechanics Converters",
    "Moment of Inertia": "Mechanics Converters",
    "Moment of Force": "Mechanics Converters",
    "Torque": "Mechanics Converters",
    "Temperature": "Heat Converters",
    "Fuel Consumption": "Heat Converters",
    "Currency": "Miscellaneous Converters",
    "Case": "Miscellaneous Converters",
    "Numbers": "Miscellaneous Converters",
    "Data Storage": "Miscellaneous Converters",
    "Prefixes": "Miscellaneous Converters",
    "Data Transfer": "Miscellaneous Converters",
    "Sound": "Miscellaneous Converters",
    "Typography": "Miscellaneous Converters",
}


@dataclass(frozen=True)
class ConverterLink:
    category: str
    subcategory: str
    href: str


class ConverterIndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[ConverterLink] = []
        self._in_catalog_table = False
        self._table_depth = 0
        self._current_category = ""
        self._capturing_h4 = False
        self._capturing_link = False
        self._link_href = ""
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "table" and attr.get("id") == "homelist":
            self._in_catalog_table = True
            self._table_depth = 1
            return

        if not self._in_catalog_table:
            return

        if tag == "table":
            self._table_depth += 1
        elif tag == "h4":
            self._capturing_h4 = True
            self._buffer = []
        elif tag == "a":
            self._capturing_link = True
            self._link_href = attr.get("href") or ""
            self._buffer = []

    def handle_endtag(self, tag: str) -> None:
        if not self._in_catalog_table:
            return

        if tag == "h4" and self._capturing_h4:
            self._current_category = normalize_category("".join(self._buffer))
            self._capturing_h4 = False
            self._buffer = []
        elif tag == "a" and self._capturing_link:
            text = normalize_text("".join(self._buffer))
            subcategory = strip_converter_suffix(text)
            if (
                self._current_category
                and subcategory
                and self._link_href.endswith("-converter.html")
            ):
                self.links.append(
                    ConverterLink(
                        category=self._current_category,
                        subcategory=subcategory,
                        href=self._link_href,
                    )
                )
            self._capturing_link = False
            self._link_href = ""
            self._buffer = []
        elif tag == "table":
            self._table_depth -= 1
            if self._table_depth <= 0:
                self._in_catalog_table = False

    def handle_data(self, data: str) -> None:
        if self._capturing_h4 or self._capturing_link:
            self._buffer.append(data)


class UnitOptionsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.selects: list[tuple[dict[str, str], list[str]]] = []
        self._current_select_attrs: dict[str, str] | None = None
        self._current_options: list[str] = []
        self._capturing_option = False
        self._option_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "select" and self._current_select_attrs is None:
            self._current_select_attrs = {
                key: value or "" for key, value in attrs
            }
            self._current_options = []
        elif tag == "option" and self._current_select_attrs is not None:
            self._capturing_option = True
            self._option_buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "option" and self._capturing_option:
            option = normalize_text("".join(self._option_buffer))
            if option:
                self._current_options.append(option)
            self._capturing_option = False
            self._option_buffer = []
        elif tag == "select" and self._current_select_attrs is not None:
            self.selects.append((self._current_select_attrs, self._current_options))
            self._current_select_attrs = None
            self._current_options = []

    def handle_data(self, data: str) -> None:
        if self._capturing_option:
            self._option_buffer.append(data)

    def unit_options(self) -> list[str]:
        if not self.selects:
            return []

        for attrs, options in self.selects:
            select_id = attrs.get("id", "").lower()
            select_name = attrs.get("name", "").lower()
            if "from" in select_id or "from" in select_name:
                return deduplicate(options)

        return deduplicate(self.selects[0][1])


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_category(text: str) -> str:
    words = normalize_text(text).split()
    if words and words[-1].lower() == "converters":
        words[-1] = "Converters"
    return " ".join(words)


def strip_converter_suffix(text: str) -> str:
    suffix = " Converter"
    if text.endswith(suffix):
        return text[: -len(suffix)]
    return text


def deduplicate(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_converter_links(home_url: str) -> list[ConverterLink]:
    parser = ConverterIndexParser()
    parser.feed(fetch_text(home_url))
    return parser.links


def parse_unit_options(page_url: str) -> list[str]:
    parser = UnitOptionsParser()
    parser.feed(fetch_text(page_url))
    return parser.unit_options()


def build_catalog(home_url: str, delay_seconds: float) -> dict[str, Any]:
    links = parse_converter_links(home_url)
    categories: dict[str, list[dict[str, Any]]] = {}
    all_units: list[dict[str, str]] = []

    for index, link in enumerate(links):
        page_url = urljoin(home_url, link.href)
        units = parse_unit_options(page_url)
        if index and delay_seconds > 0:
            time.sleep(delay_seconds)

        display_category = display_category_for_subcategory(
            link.subcategory,
            link.category,
        )
        subcategory = {
            "name": link.subcategory,
            "unit_count": len(units),
            "units": units,
        }
        categories.setdefault(display_category, []).append(subcategory)
        all_units.extend(
            {
                "category": display_category,
                "subcategory": link.subcategory,
                "unit": unit,
            }
            for unit in units
        )

    unique_units = sorted({record["unit"] for record in all_units})
    return {
        "version": 1,
        "catalog_name": "Full List Unit Catalog",
        "description": (
            "Development reference list of candidate unit labels grouped by "
            "display category. Runtime conversions use the bundled NIST data."
        ),
        "totals": {
            "category_count": len(categories),
            "subcategory_count": len(links),
            "unit_reference_count": len(all_units),
            "unique_unit_label_count": len(unique_units),
        },
        "categories": [
            {"name": name, "subcategories": subcategories}
            for name, subcategories in ordered_categories(categories)
        ],
        "all_units": all_units,
    }


def normalize_existing_catalog(catalog: dict[str, Any]) -> dict[str, Any]:
    categories: dict[str, list[dict[str, Any]]] = {}
    all_units: list[dict[str, str]] = []

    for source_category in catalog["categories"]:
        for source_subcategory in source_category["subcategories"]:
            display_category = display_category_for_subcategory(
                source_subcategory["name"],
                source_category["name"],
            )
            subcategory = {
                "name": source_subcategory["name"],
                "unit_count": source_subcategory["unit_count"],
                "units": source_subcategory["units"],
            }
            categories.setdefault(display_category, []).append(subcategory)
            all_units.extend(
                {
                    "category": display_category,
                    "subcategory": source_subcategory["name"],
                    "unit": unit,
                }
                for unit in source_subcategory["units"]
            )

    unique_units = sorted({record["unit"] for record in all_units})
    catalog["totals"] = {
        "category_count": len(categories),
        "subcategory_count": sum(
            len(subcategories) for subcategories in categories.values()
        ),
        "unit_reference_count": len(all_units),
        "unique_unit_label_count": len(unique_units),
    }
    catalog["categories"] = [
        {"name": name, "subcategories": subcategories}
        for name, subcategories in ordered_categories(categories)
    ]
    catalog["all_units"] = all_units
    return catalog


def display_category_for_subcategory(
    subcategory: str,
    fallback_category: str,
) -> str:
    return DISPLAY_CATEGORY_BY_SUBCATEGORY.get(subcategory, fallback_category)


def ordered_categories(
    categories: dict[str, list[dict[str, Any]]],
) -> list[tuple[str, list[dict[str, Any]]]]:
    ordered: list[tuple[str, list[dict[str, Any]]]] = [
        (category, categories[category])
        for category in DISPLAY_CATEGORY_ORDER
        if category in categories
    ]
    ordered.extend(
        (category, categories[category])
        for category in sorted(categories)
        if category not in DISPLAY_CATEGORY_ORDER
    )
    return ordered


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--home-url")
    parser.add_argument("--input", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
    )
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=0.05,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = args.output
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path

    if args.input is not None:
        input_path = args.input
        if not input_path.is_absolute():
            input_path = REPO_ROOT / input_path
        catalog = normalize_existing_catalog(
            json.loads(input_path.read_text(encoding="utf-8"))
        )
    else:
        if not args.home_url:
            raise SystemExit("--home-url is required when --input is not provided")
        catalog = build_catalog(args.home_url, args.delay_seconds)

    write_json(output_path, catalog)
    print(f"Wrote {output_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
