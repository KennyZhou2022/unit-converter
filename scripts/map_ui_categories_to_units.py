"""Add direct UI category metadata to the supported unit catalog."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
UNIT_CATALOG_PATH = REPO_ROOT / "src" / "unit_converter" / "data" / "unit_catalog.json"
FULL_LIST_PATH = REPO_ROOT / "data" / "external" / "full_list_unit_catalog.json"

UiPair = tuple[str, str]
NistLocation = tuple[str, str | None]


NIST_UI_HINTS: dict[NistLocation, list[UiPair]] = {
    ("ACCELERATION", None): [("Mechanics Converters", "Acceleration")],
    ("ANGLE", None): [("Dimension Converters", "Angle")],
    ("AREA AND SECOND MOMENT OF AREA", None): [("Dimension Converters", "Area")],
    ("ELECTRICITY and MAGNETISM", None): [],
    ("ENERGY (includes WORK)", None): [("Mechanics Converters", "Energy")],
    ("ENERGY DIVIDED BY AREA TIME", None): [
        ("Heat Converters", "Heat Flux Density")
    ],
    ("FORCE", None): [("Mechanics Converters", "Force")],
    ("FORCE DIVIDED BY LENGTH", None): [("Fluids Converters", "Surface Tension")],
    ("HEAT", None): [("Heat Converters", "Heat Transfer Coefficient")],
    ("HEAT", "Available Energy"): [("Mechanics Converters", "Energy")],
    ("HEAT", "Coefficient of Heat Transfer"): [
        ("Heat Converters", "Heat Transfer Coefficient")
    ],
    ("HEAT", "Density of Heat"): [("Heat Converters", "Heat Density")],
    ("HEAT", "Density of Heat Flow Rate"): [
        ("Heat Converters", "Heat Flux Density")
    ],
    ("HEAT", "Fuel Consumption"): [("Heat Converters", "Fuel Consumption")],
    ("HEAT", "Heat Capacity and Entropy"): [
        ("Heat Converters", "Specific Heat Capacity")
    ],
    ("HEAT", "Heat Flow Rate"): [("Mechanics Converters", "Power")],
    ("HEAT", "Specific Heat Capacity and Specific Entropy"): [
        ("Heat Converters", "Specific Heat Capacity")
    ],
    ("HEAT", "Thermal Conductivity"): [
        ("Heat Converters", "Thermal Conductivity")
    ],
    ("HEAT", "Thermal Diffusivity"): [
        ("Heat Converters", "Thermal Conductivity")
    ],
    ("HEAT", "Thermal Insulance"): [
        ("Heat Converters", "Thermal Resistance")
    ],
    ("HEAT", "Thermal Resistance"): [
        ("Heat Converters", "Thermal Resistance")
    ],
    ("HEAT", "Thermal Resistivity"): [
        ("Heat Converters", "Thermal Resistance")
    ],
    ("LENGTH", None): [("Dimension Converters", "Length")],
    ("LIGHT", None): [],
    ("MASS and MOMENT OF INERTIA", None): [
        ("Mechanics Converters", "Weight and Mass")
    ],
    ("MASS DIVIDED BY AREA", None): [("Fluids Converters", "Mass Flux Density")],
    ("MASS DIVIDED BY LENGTH", None): [
        ("Mechanics Converters", "Weight and Mass")
    ],
    ("MASS DIVIDED BY TIME (includes FLOW)", None): [
        ("Fluids Converters", "Flow - Mass")
    ],
    (
        "MASS DIVIDED BY VOLUME (includes MASS DENSITY and MASS CONCENTRATION)",
        None,
    ): [("Mechanics Converters", "Density")],
    ("MOMENT OF FORCE or TORQUE", None): [("Mechanics Converters", "Torque")],
    ("MOMENT OF FORCE or TORQUE, DIVIDED BY LENGTH", None): [
        ("Mechanics Converters", "Torque")
    ],
    ("PERMEABILITY", None): [("Fluids Converters", "Permeability")],
    ("POWER", None): [("Mechanics Converters", "Power")],
    ("PRESSURE or STRESS (FORCE DIVIDED BY AREA)", None): [
        ("Mechanics Converters", "Pressure")
    ],
    ("RADIOLOGY", None): [],
    ("TEMPERATURE", None): [("Heat Converters", "Temperature")],
    ("TEMPERATURE INTERVAL", None): [("Heat Converters", "Temperature Interval")],
    ("TIME", None): [("Mechanics Converters", "Time")],
    ("VELOCITY (includes SPEED)", None): [("Mechanics Converters", "Speed")],
    ("VISCOSITY, DYNAMIC", None): [("Fluids Converters", "Viscosity - Dynamic")],
    ("VISCOSITY, KINEMATIC", None): [
        ("Fluids Converters", "Viscosity - Kinematic")
    ],
    ("VOLUME (includes CAPACITY)", None): [("Dimension Converters", "Volume")],
    ("VOLUME DIVIDED BY TIME (includes FLOW)", None): [
        ("Fluids Converters", "Flow")
    ],
}


def main() -> None:
    unit_catalog = load_json(UNIT_CATALOG_PATH)
    full_list_catalog = load_json(FULL_LIST_PATH)
    unit_records = build_unit_records(unit_catalog, full_list_catalog)

    method_counts = Counter(
        ui_mapping["match_method"]
        for unit in unit_records
        for ui_mapping in unit["ui_categories"]
    )
    unit_catalog["units"] = unit_records
    unit_catalog["totals"]["unit_record_count"] = len(unit_records)
    unit_catalog["totals"]["unit_ui_mapping_count"] = sum(
        len(unit["ui_categories"]) for unit in unit_records
    )
    unit_catalog["totals"]["full_list_ui_mapping_count"] = method_counts[
        "full_list_unit"
    ]
    unit_catalog["totals"]["nist_context_ui_mapping_count"] = method_counts[
        "nist_context"
    ]

    write_json(UNIT_CATALOG_PATH, unit_catalog)
    print(f"Wrote {UNIT_CATALOG_PATH.relative_to(REPO_ROOT)}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_unit_records(
    unit_catalog: dict[str, Any],
    full_list_catalog: dict[str, Any],
) -> list[dict[str, Any]]:
    full_list_records = build_full_list_records(full_list_catalog)
    full_list_index = build_full_list_index(full_list_records)
    nist_locations = build_precise_nist_locations(unit_catalog)
    valid_ui_pairs = {
        (category["name"], subcategory["name"])
        for category in full_list_catalog["categories"]
        for subcategory in category["subcategories"]
    }

    unit_records: list[dict[str, Any]] = []
    for label in unit_catalog["all_units"]:
        locations = nist_locations[label]
        ui_categories = resolve_ui_categories(
            label,
            locations,
            full_list_index,
            valid_ui_pairs,
        )
        unit_records.append(
            {
                "label": label,
                "nist_categories": [
                    nist_category_record(category, subcategory)
                    for category, subcategory in locations
                ],
                "ui_categories": ui_categories,
            }
        )

    return unit_records


def nist_category_record(category: str, subcategory: str | None) -> dict[str, str]:
    record = {"category": category}
    if subcategory is not None:
        record["subcategory"] = subcategory
    return record


def build_precise_nist_locations(
    unit_catalog: dict[str, Any],
) -> dict[str, list[NistLocation]]:
    locations: dict[str, list[NistLocation]] = defaultdict(list)
    for category in unit_catalog["categories"]:
        category_name = category["name"]
        subcategory_by_unit: dict[str, list[str]] = defaultdict(list)
        for subcategory in category.get("subcategories", []):
            for unit in subcategory["units"]:
                subcategory_by_unit[unit].append(subcategory["name"])

        for unit in category["units"]:
            subcategories = subcategory_by_unit.get(unit)
            if subcategories:
                for subcategory_name in subcategories:
                    locations[unit].append((category_name, subcategory_name))
            else:
                locations[unit].append((category_name, None))

    return {
        unit: sorted(unit_locations)
        for unit, unit_locations in locations.items()
    }


def build_full_list_records(full_list_catalog: dict[str, Any]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for category in full_list_catalog["categories"]:
        for subcategory in category["subcategories"]:
            for unit in subcategory["units"]:
                name, symbol = split_full_list_label(unit)
                records.append(
                    {
                        "label": unit,
                        "name": name,
                        "symbol": symbol,
                        "ui_category": category["name"],
                        "ui_subcategory": subcategory["name"],
                    }
                )
    return records


def build_full_list_index(
    records: list[dict[str, str]],
) -> dict[str, dict[Any, list[dict[str, str]]]]:
    by_both: dict[Any, list[dict[str, str]]] = defaultdict(list)
    by_name: dict[Any, list[dict[str, str]]] = defaultdict(list)
    by_symbol: dict[Any, list[dict[str, str]]] = defaultdict(list)
    by_label: dict[Any, list[dict[str, str]]] = defaultdict(list)

    for record in records:
        name_key = normalize_name(record["name"])
        symbol_key = normalize_symbol(record["symbol"])
        label_key = normalize_name(record["label"])
        if name_key:
            by_name[name_key].append(record)
        if symbol_key:
            by_symbol[symbol_key].append(record)
        if name_key and symbol_key:
            by_both[(name_key, symbol_key)].append(record)
        if label_key:
            by_label[label_key].append(record)

    return {
        "by_both": by_both,
        "by_name": by_name,
        "by_symbol": by_symbol,
        "by_label": by_label,
    }


def resolve_ui_categories(
    label: str,
    nist_locations: list[NistLocation],
    full_list_index: dict[str, dict[Any, list[dict[str, str]]]],
    valid_ui_pairs: set[UiPair],
) -> list[dict[str, Any]]:
    hints = infer_ui_pairs(label, nist_locations, valid_ui_pairs)
    candidates = find_full_list_candidates(label, full_list_index)
    filtered_candidates = filter_candidates_by_hints(candidates, hints)

    if filtered_candidates:
        return full_list_ui_records(filtered_candidates)

    if candidates and not hints:
        return full_list_ui_records(candidates)

    if hints:
        return [
            {
                "category": category,
                "subcategory": subcategory,
                "match_method": "nist_context",
            }
            for category, subcategory in hints
        ]

    raise ValueError(f"Unable to map unit to a UI category: {label}")


def find_full_list_candidates(
    label: str,
    full_list_index: dict[str, dict[Any, list[dict[str, str]]]],
) -> list[dict[str, str]]:
    name, symbol = split_supported_unit_label(label)
    name_key = normalize_name(name)
    symbol_key = normalize_symbol(symbol)
    label_key = normalize_name(strip_supported_unit_suffix(label))

    candidate_groups: list[list[dict[str, str]]] = []
    if label_key:
        candidate_groups.append(full_list_index["by_label"].get(label_key, []))
    if name_key and symbol_key:
        candidate_groups.append(
            full_list_index["by_both"].get((name_key, symbol_key), [])
        )
    if name_key:
        candidate_groups.append(full_list_index["by_name"].get(name_key, []))
    if symbol_key:
        symbol_matches = full_list_index["by_symbol"].get(symbol_key, [])
        if len(symbol_matches) <= 4:
            candidate_groups.append(symbol_matches)

    candidates: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for group in candidate_groups:
        for candidate in group:
            key = (
                candidate["label"],
                candidate["ui_category"],
                candidate["ui_subcategory"],
            )
            if key not in seen:
                seen.add(key)
                candidates.append(candidate)

    return candidates


def filter_candidates_by_hints(
    candidates: list[dict[str, str]],
    hints: list[UiPair],
) -> list[dict[str, str]]:
    if not hints:
        return candidates

    hinted_pairs = set(hints)
    exact = [
        candidate
        for candidate in candidates
        if (candidate["ui_category"], candidate["ui_subcategory"]) in hinted_pairs
    ]
    if exact:
        return exact

    hinted_categories = {category for category, _ in hints}
    category_matches = [
        candidate
        for candidate in candidates
        if candidate["ui_category"] in hinted_categories
    ]
    return category_matches


def full_list_ui_records(candidates: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[UiPair, list[str]] = defaultdict(list)
    for candidate in candidates:
        key = (candidate["ui_category"], candidate["ui_subcategory"])
        grouped[key].append(candidate["label"])

    return [
        {
            "category": category,
            "subcategory": subcategory,
            "match_method": "full_list_unit",
            "matched_full_list_units": sorted(set(labels)),
        }
        for (category, subcategory), labels in sorted(grouped.items())
    ]


def infer_ui_pairs(
    label: str,
    nist_locations: list[NistLocation],
    valid_ui_pairs: set[UiPair],
) -> list[UiPair]:
    pairs = infer_ui_pairs_from_label(label)
    if not pairs:
        pairs = [
            pair
            for location in nist_locations
            for pair in NIST_UI_HINTS.get(location, [])
        ]
    return deduplicate_pair_order(pair for pair in pairs if pair in valid_ui_pairs)


def infer_ui_pairs_from_label(label: str) -> list[UiPair]:
    text = normalize_name(strip_supported_unit_suffix(label))
    if any(term in text for term in ("weber", "maxwell", "unit pole")):
        return [("Magnetism Converters", "Magnetic Flux")]
    if any(term in text for term in ("tesla", "gauss", "gamma")):
        return [("Magnetism Converters", "Magnetic Flux Density")]
    if "gilbert" in text:
        return [("Magnetism Converters", "Magnetomotive Force")]
    if "oersted" in text or "ampere/meter" in text or "ampere per meter" in text:
        return [("Magnetism Converters", "Magnetic Field Strength")]
    if any(term in text for term in ("farad", "capacitance")):
        return [("Electricity Converters", "Electrostatic Capacitance")]
    if any(term in text for term in ("henry", "inductance")):
        return [("Electricity Converters", "Inductance")]
    if any(term in text for term in ("siemens", "mho")):
        if "/meter" in text or " per meter" in text or "centimeter" in text:
            return [("Electricity Converters", "Electric Conductivity")]
        return [("Electricity Converters", "Electric Conductance")]
    if "ohm" in text or "resistance" in text:
        if any(term in text for term in ("meter", "centimeter", "circular")):
            return [("Electricity Converters", "Electric Resistivity")]
        return [("Electricity Converters", "Electric Resistance")]
    if any(term in text for term in ("volt", "electric potential")):
        return [("Electricity Converters", "Electric Potential")]
    if any(term in text for term in ("coulomb", "franklin", "faraday", "ampere hour")):
        return [("Electricity Converters", "Charge")]
    if any(term in text for term in ("ampere", "biot", "current")):
        return [("Electricity Converters", "Current")]
    if any(term in text for term in ("becquerel", "curie")):
        return [("Radiology Converters", "Radiation-Activity")]
    if "coulomb/kilogram" in text or "roentgen" in text:
        return [("Radiology Converters", "Radiation-Exposure")]
    if any(term in text for term in ("gray", "rad ", "rad absorbed", "rem", "sievert")):
        return [("Radiology Converters", "Radiation-Absorbed Dose")]
    if any(term in text for term in ("footcandle", "lux", "phot", "lumen/square")):
        return [("Light Converters", "Illumination")]
    if any(term in text for term in ("lambert", "stilb", "candela/square")):
        return [("Light Converters", "Luminance")]
    if "candela" in text:
        return [("Light Converters", "Luminous Intensity")]
    return []


def deduplicate_pair_order(pairs: Any) -> list[UiPair]:
    seen: set[UiPair] = set()
    result: list[UiPair] = []
    for pair in pairs:
        if pair not in seen:
            seen.add(pair)
            result.append(pair)
    return result


def split_full_list_label(label: str) -> tuple[str, str]:
    match = re.search(r"\[([^\[\]]+)\]$", label)
    if match:
        return label[: match.start()].strip(), match.group(1).strip()
    return label.strip(), ""


def split_supported_unit_label(label: str) -> tuple[str, str]:
    label = strip_supported_unit_suffix(label)
    match = re.search(r"\[([^\[\]]+)\]$", label)
    if match:
        return label[: match.start()].strip(), match.group(1).strip()

    match = re.search(r"\(([^()]*)\)$", label)
    if match and looks_like_symbol(match.group(1)):
        return label[: match.start()].strip(), match.group(1).strip()

    return label.strip(), ""


def strip_supported_unit_suffix(label: str) -> str:
    return re.sub(r" \[temperature(?: interval)?\]$", "", label)


def looks_like_symbol(value: str) -> bool:
    return (
        len(value) <= 16
        or "/" in value
        or any(character.isupper() for character in value)
        or any(character.isdigit() for character in value)
    )


def normalize_name(value: str) -> str:
    text = normalize_text(value)
    replacements = {
        "degree celsius": "celsius",
        "degree fahrenheit": "fahrenheit",
        "degree rankine": "rankine",
        "degree centigrade": "centigrade",
        "calorieit": "calorie it",
        "calorieth": "calorie th",
        "kilocalorieit": "kilocalorie it",
        "kilocalorieth": "kilocalorie th",
        "british thermal unitit": "british thermal unit it",
        "british thermal unitth": "british thermal unit th",
        "international table": "it",
        "thermochemical": "th",
        "u.s.": "us",
        "sq.": "square",
        "cu.": "cubic",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\bsq\b", "square", text)
    text = re.sub(r"\bcu\b", "cubic", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_symbol(value: str) -> str:
    text = normalize_text(value)
    text = text.replace("degree", "")
    text = text.replace(" ", "")
    text = text.replace("*", "")
    text = text.replace("(", "").replace(")", "")
    return text


def normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(
        character for character in text if not unicodedata.combining(character)
    )
    text = text.casefold()
    text = text.replace("µ", "u")
    text = text.replace("μ", "u")
    text = text.replace("°", "degree")
    text = text.replace(" per ", "/")
    text = text.replace("·", "*")
    text = text.replace("×", "*")
    text = text.replace("^", "")
    text = text.replace("²", "2").replace("³", "3")
    text = re.sub(r"\s*/\s*", "/", text)
    text = re.sub(r"\s*\*\s*", "*", text)
    text = re.sub(r"[,_\[\]]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


if __name__ == "__main__":
    main()
