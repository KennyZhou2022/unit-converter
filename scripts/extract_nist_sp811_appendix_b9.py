#!/usr/bin/env python
"""Extract Appendix B.9 conversion data from NIST SP 811."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

from pypdf import PdfReader


APPENDIX = "B.9"
SOURCE_NAME = "NIST Special Publication 811 (2008), Appendix B.9"
SOURCE_DOCUMENT = "standards/raw/nistspecialpublication811e2008.pdf"
SOURCE_PAGES = "57-69"
DEFAULT_PDF = Path(SOURCE_DOCUMENT)
DEFAULT_CSV = Path("data/interim/nist_sp811_appendix_b9_conversions.csv")
DEFAULT_PACKAGE_JSON = Path("src/unit_converter/data/conversions.json")
DEFAULT_CATEGORY_JSON = Path(
    "src/unit_converter/data/physical_quantity_conversions.json"
)
DEFAULT_UNIT_CATALOG_JSON = Path("src/unit_converter/data/unit_catalog.json")
B9_PAGE_INDEXES = range(68, 81)

CATEGORY_HEADINGS = {
    "ACCELERATION",
    "ANGLE",
    "AREA AND SECOND MOMENT OF AREA",
    "CAPACITY (see VOLUME)",
    "DENSITY (that is, MASS DENSITY- see MASS DIVIDED BY VOLUME)",
    "ELECTRICITY and MAGNETISM",
    "ENERGY (includes WORK)",
    "ENERGY DIVIDED BY AREA TIME",
    "FLOW (see MASS DIVIDED BY TIME or VOLUME DIVIDED BY TIME)",
    "FORCE",
    "FORCE DIVIDED BY AREA (see PRESSURE)",
    "FORCE DIVIDED BY LENGTH",
    "HEAT",
    "LENGTH",
    "LIGHT",
    "MASS and MOMENT OF INERTIA",
    "MASS DENSITY (see MASS DIVIDED BY VOLUME)",
    "MASS DIVIDED BY AREA",
    "MASS DIVIDED BY CAPACITY (see MASS DIVIDED BY VOLUME)",
    "MASS DIVIDED BY LENGTH",
    "MASS DIVIDED BY TIME (includes FLOW)",
    "MASS DIVIDED BY VOLUME (includes MASS DENSITY and MASS CONCENTRATION)",
    "MOMENT OF FORCE or TORQUE",
    "MOMENT OF FORCE or TORQUE, DIVIDED BY LENGTH",
    "PERMEABILITY",
    "POWER",
    "PRESSURE or STRESS (FORCE DIVIDED BY AREA)",
    "RADIOLOGY",
    "SPEED (see VELOCITY)",
    "STRESS (see PRESSURE)",
    "TEMPERATURE",
    "TEMPERATURE INTERVAL",
    "TIME",
    "TORQUE (see MOMENT OF FORCE)",
    "VELOCITY (includes SPEED)",
    "VISCOSITY, DYNAMIC",
    "VISCOSITY, KINEMATIC",
    "VOLUME (includes CAPACITY)",
    "VOLUME DIVIDED BY TIME (includes FLOW)",
    "WORK (see ENERGY)",
}

MISSING_MIDDLE_LEADER_TARGETS = (
    "kilogram per square meter",
)

SUBCATEGORY_HEADINGS = {
    "Available Energy",
    "Coefficient of Heat Transfer",
    "Density of Heat",
    "Density of Heat Flow Rate",
    "Fuel Consumption",
    "Heat Capacity and Entropy",
    "Heat Flow Rate",
    "Specific Heat Capacity and Specific Entropy",
    "Thermal Conductivity",
    "Thermal Diffusivity",
    "Thermal Insulance",
    "Thermal Resistance",
    "Thermal Resistivity",
}

TEMPERATURE_UNIT_SUFFIXES = {
    "TEMPERATURE": " [temperature]",
    "TEMPERATURE INTERVAL": " [temperature interval]",
}

TEMPERATURE_UNIT_LABELS = {
    "degree Celsius (°C)",
    "degree centigrade",
    "degree Fahrenheit (°F)",
    "degree Rankine (°R)",
    "kelvin (K)",
}

SHARED_COMPATIBLE_UNIT_LABELS = {
    "watt (W)",
    "watt per square meter (W / m2)",
}

TEXT_REPLACEMENTS = {
    "co ulomb": "coulomb",
    "can dela": "candela",
    "ga l": "gal",
    "k ilogram": "kilogram",
    "k ilonewton": "kilonewton",
    "kilogr am": "kilogram",
    "m eter": "meter",
    "m illigram": "milligram",
    "m illiliter": "milliliter",
    "m illimeter": "millimeter",
    "m illinewton": "millinewton",
    "pa scal": "pascal",
    "pe r": "per",
    "liter pe r": "liter per",
    "square mete r": "square meter",
    "Caliber": "caliber",
}


@dataclass(frozen=True)
class ExtractedConversion:
    category: str
    subcategory: str | None
    from_unit: str
    to_unit: str
    rule: str
    source_page: int

    @property
    def rule_type(self) -> str:
        return "factor" if is_decimal(self.rule) else "formula"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--package-json", type=Path, default=DEFAULT_PACKAGE_JSON)
    parser.add_argument("--category-json", type=Path, default=DEFAULT_CATEGORY_JSON)
    parser.add_argument(
        "--unit-catalog-json",
        type=Path,
        default=DEFAULT_UNIT_CATALOG_JSON,
    )
    args = parser.parse_args()

    conversions = extract_b9_conversions(args.pdf)
    validate_conversions(conversions)
    write_csv(args.csv, conversions)
    write_package_json(args.package_json, conversions)
    write_category_json(args.category_json, conversions)
    write_unit_catalog_json(args.unit_catalog_json, conversions)

    print(f"Extracted {len(conversions)} conversions from Appendix {APPENDIX}.")
    print(f"Wrote CSV: {args.csv}")
    print(f"Wrote package JSON: {args.package_json}")
    print(f"Wrote category JSON: {args.category_json}")
    print(f"Wrote unit catalog JSON: {args.unit_catalog_json}")


def extract_b9_conversions(pdf_path: Path) -> list[ExtractedConversion]:
    reader = PdfReader(str(pdf_path))
    rows: list[ExtractedConversion] = []
    pending_lines: list[str] = []
    category: str | None = None
    subcategory: str | None = None
    split_category = False

    for page_index in B9_PAGE_INDEXES:
        source_page = page_index + 1
        text = reader.pages[page_index].extract_text() or ""
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if should_skip_line(line):
                continue

            normalized_line = normalize_text(line)
            if not normalized_line:
                continue

            if (
                normalized_line
                == "MASS DIVIDED BY VOLUME (includes MASS DENSITY and MASS"
            ):
                split_category = True
                continue

            if split_category and normalized_line == "CONCENTRATION)":
                category = (
                    "MASS DIVIDED BY VOLUME "
                    "(includes MASS DENSITY and MASS CONCENTRATION)"
                )
                subcategory = None
                split_category = False
                continue

            split_category = False

            if not pending_lines and normalized_line in CATEGORY_HEADINGS:
                category = normalized_line
                subcategory = None
                continue

            if not pending_lines and normalized_line in SUBCATEGORY_HEADINGS:
                subcategory = normalized_line
                continue

            pending_lines.append(line)
            parsed = parse_conversion(pending_lines)
            if parsed is None:
                continue

            if category is None:
                raise ValueError(
                    f"Parsed a conversion before finding a category: {parsed}"
                )

            rows.append(
                ExtractedConversion(
                    category=category,
                    subcategory=subcategory,
                    from_unit=qualified_unit_name(parsed[0], category),
                    to_unit=qualified_unit_name(parsed[1], category),
                    rule=parsed[2],
                    source_page=source_page,
                )
            )
            pending_lines = []

    if pending_lines:
        raise ValueError(f"Unparsed trailing lines: {pending_lines!r}")

    return rows


def parse_conversion(lines: list[str]) -> tuple[str, str, str] | None:
    source = normalize_text(" ".join(lines))
    if "..." not in source:
        return None

    parts = [
        normalize_text(part)
        for part in re.split(r"\s*\.{2,}\s*", source)
        if normalize_text(part)
    ]

    if len(parts) == 2 and is_decimal(parts[1]):
        split_units = split_missing_middle_leader(parts[0])
        if split_units is None:
            return None
        return split_units[0], split_units[1], normalize_factor(parts[1])

    if len(parts) < 3:
        return None

    from_unit = clean_unit(parts[0])
    to_unit = clean_unit(" ".join(parts[1:-1]))
    rule = normalize_text(parts[-1].strip(". "))

    if rule == "divide 235.215 by":
        return None

    if is_decimal(rule):
        return from_unit, to_unit, normalize_factor(rule)

    return from_unit, to_unit, normalize_formula(from_unit, to_unit, rule)


def split_missing_middle_leader(value: str) -> tuple[str, str] | None:
    for target in MISSING_MIDDLE_LEADER_TARGETS:
        match = re.search(rf"\s({re.escape(target)}\b.*)", value)
        if match is None:
            continue
        from_unit = clean_unit(value[: match.start()])
        to_unit = clean_unit(match.group(1))
        if from_unit and to_unit:
            return from_unit, to_unit
    return None


def clean_unit(value: str) -> str:
    value = normalize_text(value.strip(". "))
    value = re.sub(r"\)\s*\d{1,2}(?=\s|$|\.|,)", ")", value)
    value = value.replace("degree centigrade15", "degree centigrade")
    value = value.replace("mile, nautical20", "mile, nautical")
    value = value.replace("darcy14", "darcy")
    value = value.replace("lambert17", "lambert")
    value = value.replace("( ° )", "(°)")
    value = re.sub(r"\s+\)", ")", value)
    value = re.sub(r"\(H$", "(H)", value)
    value = re.sub(r"\(gal / min\)?$", "(gal / min)", value)
    return normalize_text(value)


def qualified_unit_name(unit: str, category: str) -> str:
    suffix = TEMPERATURE_UNIT_SUFFIXES.get(category)
    if suffix is None or unit not in TEMPERATURE_UNIT_LABELS:
        return unit
    return f"{unit}{suffix}"


def normalize_formula(from_unit: str, to_unit: str, value: str) -> str:
    from_lower = from_unit.lower()
    to_lower = to_unit.lower()

    if "mile per gallon" in from_lower and "100 kilometer" in to_lower:
        return "235.215 / x"

    if "fahrenheit" in from_lower and "celsius" in to_lower:
        return "(x - 32) / 1.8"

    if "fahrenheit" in from_lower and "kelvin" in to_lower:
        return "(x + 459.67) / 1.8"

    if "rankine" in from_lower and "kelvin" in to_lower:
        return "x / 1.8"

    if "celsius" in from_lower and "kelvin" in to_lower:
        return "x + 273.15"

    if from_lower.startswith("kelvin") and "celsius" in to_lower:
        return "x - 273.15"

    if "centigrade" in from_lower and "celsius" in to_lower:
        return "x"

    return normalize_text(value.replace(" ! ", " - "))


def normalize_text(value: str) -> str:
    value = (
        value.replace("\u2212", "-")
        .replace("−", "-")
        .replace("º", "°")
        .replace("Ω", "Ω")
        .replace("–", "-")
        .replace("—", "-")
        .replace("!1", "^-1")
    )
    for original, replacement in TEXT_REPLACEMENTS.items():
        value = value.replace(original, replacement)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"(?<=[A-Za-zΩ])\s+([234])(?=[)\]/ ·,]|$)", r"\1", value)
    return value


def normalize_factor(value: str) -> str:
    return normalize_text(value).replace(" ", "").lstrip(".")


def is_decimal(value: str) -> bool:
    normalized = normalize_factor(value)
    try:
        Decimal(normalized)
    except InvalidOperation:
        return False
    return True


def should_skip_line(line: str) -> bool:
    if not line:
        return True
    if line.startswith("Guide for the Use"):
        return True
    if re.fullmatch(r"\d+", line):
        return True
    return line.startswith(
        (
            "B.9 ",
            "Caution:",
            "of those few",
            "Factors in",
            "To convert from",
        )
    )


def validate_conversions(conversions: list[ExtractedConversion]) -> None:
    factor_pattern = re.compile(r"\b\d(?:[\d .]*\d)?\s*E[+-]\d{2}\b")
    bad_rows: list[str] = []
    unit_contexts: dict[str, set[tuple[str, str | None]]] = defaultdict(set)
    for index, conversion in enumerate(conversions, start=1):
        unit_text = f"{conversion.from_unit} | {conversion.to_unit}"
        context = (conversion.category, conversion.subcategory)
        unit_contexts[conversion.from_unit].add(context)
        unit_contexts[conversion.to_unit].add(context)
        if any(heading in unit_text for heading in CATEGORY_HEADINGS):
            bad_rows.append(f"{index}: category heading leaked into unit fields")
        if conversion.category in TEMPERATURE_UNIT_SUFFIXES:
            for unit in (conversion.from_unit, conversion.to_unit):
                if unit in TEMPERATURE_UNIT_LABELS:
                    bad_rows.append(f"{index}: unqualified temperature unit {unit!r}")
        if factor_pattern.search(unit_text):
            bad_rows.append(f"{index}: numeric factor leaked into unit fields")
        if conversion.from_unit.count("(") != conversion.from_unit.count(")"):
            bad_rows.append(f"{index}: unbalanced parentheses in from unit")
        if conversion.to_unit.count("(") != conversion.to_unit.count(")"):
            bad_rows.append(f"{index}: unbalanced parentheses in to unit")
        if conversion.rule_type == "formula":
            try:
                compile(conversion.rule, "<conversion formula>", "eval")
            except SyntaxError:
                bad_rows.append(f"{index}: invalid formula {conversion.rule!r}")

    for unit, contexts in unit_contexts.items():
        if len(contexts) > 1 and unit not in SHARED_COMPATIBLE_UNIT_LABELS:
            formatted_contexts = ", ".join(
                format_source_context(*context)
                for context in sorted(contexts, key=lambda item: item[0])
            )
            bad_rows.append(
                f"unit label {unit!r} appears in multiple source contexts: "
                f"{formatted_contexts}"
            )

    if bad_rows:
        details = "\n".join(bad_rows)
        raise ValueError(f"Extracted conversion data failed validation:\n{details}")


def format_source_context(category: str, subcategory: str | None) -> str:
    if subcategory is None:
        return category
    return f"{category} / {subcategory}"


def write_csv(path: Path, conversions: list[ExtractedConversion]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["convert_from", "to", "rule"])
        for conversion in conversions:
            writer.writerow([conversion.from_unit, conversion.to_unit, conversion.rule])


def write_package_json(path: Path, conversions: list[ExtractedConversion]) -> None:
    payload = {
        "version": 1,
        "source": {
            "name": SOURCE_NAME,
            "document": SOURCE_DOCUMENT,
        },
        "conversions": [
            package_conversion(conversion) for conversion in conversions
        ],
    }
    write_json(path, payload)


def package_conversion(conversion: ExtractedConversion) -> dict[str, str]:
    row = {
        "from": conversion.from_unit,
        "to": conversion.to_unit,
        "category": conversion.category,
    }
    if conversion.subcategory is not None:
        row["subcategory"] = conversion.subcategory
    if conversion.rule_type == "factor":
        row["factor"] = conversion.rule
    else:
        row["formula"] = conversion.rule
    return row


def write_category_json(path: Path, conversions: list[ExtractedConversion]) -> None:
    grouped: dict[str, list[ExtractedConversion]] = defaultdict(list)
    for conversion in conversions:
        grouped[conversion.category].append(conversion)

    payload = {
        "version": 1,
        "source": {
            "name": SOURCE_NAME,
            "document": SOURCE_DOCUMENT,
            "appendix": APPENDIX,
            "pages": SOURCE_PAGES,
        },
        "appendix_relationship": {
            "b8": "Appendix B.8 lists the same units alphabetically.",
            "b9": (
                "Appendix B.9 lists the same units alphabetically within "
                "kinds of quantities and fields of science."
            ),
            "selected_source": APPENDIX,
        },
        "categories": [
            {
                "name": category,
                "slug": slugify(category),
                "conversions": [
                    category_conversion(conversion)
                    for conversion in grouped[category]
                ],
            }
            for category in grouped
        ],
    }
    write_json(path, payload)


def write_unit_catalog_json(path: Path, conversions: list[ExtractedConversion]) -> None:
    grouped: dict[str, list[ExtractedConversion]] = defaultdict(list)
    for conversion in conversions:
        grouped[conversion.category].append(conversion)

    category_catalogs = [
        catalog_group(category, grouped[category])
        for category in grouped
    ]
    components = [
        component
        for category in category_catalogs
        for component in category["connected_components"]
    ]
    all_units = sorted(
        {
            unit
            for conversion in conversions
            for unit in (conversion.from_unit, conversion.to_unit)
        }
    )

    payload = {
        "version": 1,
        "source": {
            "name": SOURCE_NAME,
            "document": SOURCE_DOCUMENT,
            "appendix": APPENDIX,
            "pages": SOURCE_PAGES,
        },
        "totals": {
            "category_count": len(category_catalogs),
            "direct_conversion_count": len(conversions),
            "unit_count": len(all_units),
            "unordered_convertible_pair_count": sum(
                int(component["unordered_convertible_pair_count"])
                for component in components
            ),
            "ordered_convertible_pair_count": sum(
                int(component["ordered_convertible_pair_count"])
                for component in components
            ),
        },
        "all_units": all_units,
        "categories": category_catalogs,
    }
    write_json(path, payload)


def catalog_group(
    name: str,
    conversions: list[ExtractedConversion],
    *,
    subcategory: str | None = None,
) -> dict[str, object]:
    units = sorted(
        {
            unit
            for conversion in conversions
            for unit in (conversion.from_unit, conversion.to_unit)
        }
    )
    components = connected_components(conversions)
    catalog: dict[str, object] = {
        "name": name,
        "slug": slugify(name),
        "unit_count": len(units),
        "direct_conversion_count": len(conversions),
        "connected_component_count": len(components),
        "unordered_convertible_pair_count": sum(
            component_pair_count(component) for component in components
        ),
        "ordered_convertible_pair_count": sum(
            component_pair_count(component) * 2 for component in components
        ),
        "units": units,
        "connected_components": [
            {
                "unit_count": len(component),
                "unordered_convertible_pair_count": component_pair_count(component),
                "ordered_convertible_pair_count": component_pair_count(component) * 2,
                "units": component,
            }
            for component in components
        ],
    }
    if subcategory is None:
        subcategory_groups: dict[str, list[ExtractedConversion]] = defaultdict(list)
        for conversion in conversions:
            if conversion.subcategory is not None:
                subcategory_groups[conversion.subcategory].append(conversion)
        if subcategory_groups:
            catalog["subcategories"] = [
                catalog_group(
                    subcategory_name,
                    subcategory_groups[subcategory_name],
                    subcategory=subcategory_name,
                )
                for subcategory_name in subcategory_groups
            ]
    else:
        catalog["subcategory"] = subcategory
    return catalog


def connected_components(conversions: list[ExtractedConversion]) -> list[list[str]]:
    adjacency: dict[str, set[str]] = defaultdict(set)
    for conversion in conversions:
        adjacency[conversion.from_unit].add(conversion.to_unit)
        adjacency[conversion.to_unit].add(conversion.from_unit)

    components: list[list[str]] = []
    seen: set[str] = set()
    for unit in sorted(adjacency):
        if unit in seen:
            continue
        stack = [unit]
        component: set[str] = set()
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            component.add(current)
            stack.extend(sorted(adjacency[current] - seen, reverse=True))
        components.append(sorted(component))

    return sorted(components, key=lambda component: (-len(component), component[0]))


def component_pair_count(component: list[str]) -> int:
    unit_count = len(component)
    return unit_count * (unit_count - 1) // 2


def category_conversion(conversion: ExtractedConversion) -> dict[str, str | int]:
    row: dict[str, str | int] = {
        "from": conversion.from_unit,
        "to": conversion.to_unit,
        "rule": conversion.rule,
        "rule_type": conversion.rule_type,
        "display_label": f"{conversion.from_unit} -> {conversion.to_unit}",
        "source_appendix": APPENDIX,
        "source_page": conversion.source_page,
    }
    if conversion.subcategory is not None:
        row["subcategory"] = conversion.subcategory
    return row


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\([^)]*\)", "", value)
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
