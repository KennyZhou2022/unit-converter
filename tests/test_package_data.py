import csv
import json
import re
import sys
from decimal import Decimal, localcontext
from importlib.resources import files
from pathlib import Path

import pytest

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from unit_converter import (
    Conversion,
    IncompatibleUnitError,
    UnitConverter,
    UnitNotFoundError,
    convert,
    get_ui_unit_catalog,
    get_unit_catalog,
    list_categories,
    list_ui_categories,
    list_ui_subcategories,
    list_ui_unit_ids,
    list_ui_units,
    list_unit_ids,
    list_units,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_conversion_rows() -> list[dict[str, object]]:
    data_path = REPO_ROOT / "src" / "unit_converter" / "data" / "conversions.json"
    return json.loads(data_path.read_text(encoding="utf-8"))["conversions"]


def load_quantity_catalog() -> dict[str, object]:
    data_path = (
        REPO_ROOT / "data" / "interim" / "nist_sp811_appendix_b9_by_quantity.json"
    )
    return json.loads(data_path.read_text(encoding="utf-8"))


def conversion_from_review_row(row: dict[str, object]) -> Conversion:
    rule_type = str(row["rule_type"])
    return Conversion(
        str(row["from"]),
        str(row["to"]),
        factor=str(row["rule"]) if rule_type == "factor" else None,
        formula=str(row["rule"]) if rule_type == "formula" else None,
    )


def conversion_components(
    rows: list[dict[str, object]],
) -> list[set[str]]:
    adjacency: dict[str, set[str]] = {}
    for row in rows:
        from_unit = str(row["from"])
        to_unit = str(row["to"])
        adjacency.setdefault(from_unit, set()).add(to_unit)
        adjacency.setdefault(to_unit, set()).add(from_unit)

    remaining = set(adjacency)
    components: list[set[str]] = []
    while remaining:
        pending = [remaining.pop()]
        component = set(pending)
        while pending:
            unit = pending.pop()
            for neighbor in adjacency[unit] - component:
                component.add(neighbor)
                remaining.discard(neighbor)
                pending.append(neighbor)
        components.append(component)
    return components


def count_convertible_pairs(
    converter: UnitConverter,
    units: tuple[str, ...] | None = None,
) -> tuple[int, int]:
    candidates = converter.available_units() if units is None else units
    unordered_count = 0
    ordered_count = 0
    for index, left in enumerate(candidates):
        for right in candidates[index + 1 :]:
            forward = converter.can_convert(left, right)
            reverse = converter.can_convert(right, left)
            unordered_count += int(forward or reverse)
            ordered_count += int(forward) + int(reverse)
    return unordered_count, ordered_count


def test_converts_from_bundled_nist_factor_data() -> None:
    assert convert(1, "mile per hour (mi / h)", "kilometer per hour (km / h)") == (
        Decimal("1.609344")
    )


def test_converts_from_bundled_nist_formula_data() -> None:
    assert convert(
        10,
        "mile per gallon (U.S.) (mpg) (mi / gal)",
        "liter per 100 kilometer (L / 100 km)",
    ) == Decimal("23.5215")


def test_rejects_removed_category_argument() -> None:
    with pytest.raises(TypeError):
        convert(
            32,
            "degree Fahrenheit (°F) [temperature]",
            "degree Celsius (°C) [temperature]",
            category="TEMPERATURE",
        )


def test_converts_temperature_value_with_explicit_unit_label() -> None:
    assert convert(
        32,
        "degree Fahrenheit (°F) [temperature]",
        "degree Celsius (°C) [temperature]",
    ) == Decimal("0E+1")


def test_converts_temperature_interval_with_explicit_unit_label() -> None:
    assert convert(
        18,
        "degree Fahrenheit (°F) [temperature interval]",
        "degree Celsius (°C) [temperature interval]",
    ) == Decimal("10.0000008")


def test_rejects_unqualified_temperature_unit_labels() -> None:
    with pytest.raises(UnitNotFoundError):
        convert(32, "degree Fahrenheit (°F)", "degree Celsius (°C)")


def test_converts_between_nist_units_through_joule() -> None:
    assert convert(1, "British thermal unitIT (BtuIT)", "calorieIT (calIT)") == (
        Decimal("251.9957963122193560714626923")
    )


def test_converts_between_nist_power_units_through_watt() -> None:
    assert convert(1, "watt hour (W · h)", "kilowatt hour (kW · h)") == (
        Decimal("0.001")
    )


def test_converts_when_rounded_nist_paths_are_equivalent() -> None:
    assert convert(
        1,
        "square meter (m2)",
        "square kilometer (km2)",
    ) == Decimal("0.000001")


def test_exposes_supported_unit_catalog() -> None:
    catalog = get_unit_catalog()

    assert catalog["version"] == 3
    assert catalog["totals"]["direct_conversion_count"] == 451
    assert catalog["totals"]["unit_count"] == 462
    assert catalog["totals"]["connected_component_count"] == 65
    assert catalog["totals"]["unordered_convertible_pair_count"] == 3054
    assert catalog["totals"]["ordered_convertible_pair_count"] == 6108
    assert len(catalog["units"]) == 462
    assert "calorieIT (calIT)" in list_units()
    assert "kilogram (kg)" in list_units()
    assert "millimeter (mm)" in list_units()
    assert "newton meter (N · m)" in list_units()
    assert "ohm (Ω)" in list_units()
    assert "degree Fahrenheit (°F) [temperature]" in list_units()
    assert "degree Fahrenheit (°F) [temperature interval]" in list_units()


def test_catalog_pair_totals_match_runtime_convertibility() -> None:
    catalog = get_unit_catalog()
    converter = UnitConverter.from_package_data()
    unordered_count, ordered_count = count_convertible_pairs(converter)

    assert catalog["totals"]["convertibility_model"] == "runtime_graph"
    assert catalog["totals"]["unordered_convertible_pair_count"] == unordered_count
    assert catalog["totals"]["ordered_convertible_pair_count"] == ordered_count


def test_category_pair_totals_match_runtime_convertibility() -> None:
    catalog = get_unit_catalog()
    quantity_categories = {
        category["name"]: category
        for category in load_quantity_catalog()["categories"]  # type: ignore[index]
    }

    for category in catalog["categories"]:
        review_category = quantity_categories[category["name"]]
        category_rows = review_category["conversions"]
        converter = UnitConverter(
            conversion_from_review_row(row) for row in category_rows
        )
        unordered_count, ordered_count = count_convertible_pairs(converter)
        assert category["unordered_convertible_pair_count"] == unordered_count
        assert category["ordered_convertible_pair_count"] == ordered_count

        for subcategory in category.get("subcategories", []):
            subcategory_rows = [
                row
                for row in category_rows
                if row.get("subcategory") == subcategory["name"]
            ]
            subcategory_converter = UnitConverter(
                conversion_from_review_row(row) for row in subcategory_rows
            )
            unordered_count, ordered_count = count_convertible_pairs(
                subcategory_converter
            )
            assert subcategory["unordered_convertible_pair_count"] == unordered_count
            assert subcategory["ordered_convertible_pair_count"] == ordered_count


def test_unit_catalog_exposes_stable_identity_and_display_fields() -> None:
    catalog = get_unit_catalog()
    records = catalog["units"]

    assert catalog["version"] == 3
    assert "all_units" not in catalog
    assert "all_unit_ids" not in catalog
    assert "unit_record_count" not in catalog["totals"]
    assert len({record["unit_id"] for record in records}) == len(records)
    assert len({record["display_name"] for record in records}) == len(records)
    assert all(record["unit_id"].startswith("unit.u") for record in records)
    assert all(record["quantity_id"].startswith("quantity.q") for record in records)
    assert all("label" not in record for record in records)
    assert all(isinstance(record["aliases"], list) for record in records)


def test_runtime_conversion_rows_contain_only_runtime_fields() -> None:
    data_path = REPO_ROOT / "src" / "unit_converter" / "data" / "conversions.json"
    assert json.loads(data_path.read_text(encoding="utf-8"))["version"] == 2
    for row in load_conversion_rows():
        assert set(row) <= {"from", "to", "factor", "formula"}


def test_bundled_converter_accepts_stable_ids_and_legacy_aliases() -> None:
    records_by_name = {
        record["display_name"]: record for record in get_unit_catalog()["units"]
    }
    meter_id = records_by_name["meter (m)"]["unit_id"]
    mile_id = records_by_name["mile (mi)"]["unit_id"]

    assert convert(1, mile_id, meter_id) == Decimal("1.609344E+03")
    assert convert(1, "ohm ( Ω)", "ohm (Ω)") == Decimal("1")


def test_every_stable_id_and_registered_alias_resolves() -> None:
    records = get_unit_catalog()["units"]
    converter = UnitConverter.from_package_data()

    assert set(converter.available_unit_ids()) == {
        record["unit_id"] for record in records
    }
    for record in records:
        assert converter.convert(
            1,
            record["unit_id"],
            record["display_name"],
        ) == Decimal("1")
        for alias in record["aliases"]:
            assert converter.convert(1, alias, record["unit_id"]) == Decimal("1")


def test_quantity_ids_follow_conversion_graph_components() -> None:
    records_by_name = {
        record["display_name"]: record for record in get_unit_catalog()["units"]
    }

    assert (
        records_by_name["meter (m)"]["quantity_id"]
        == records_by_name["mile (mi)"]["quantity_id"]
    )
    assert (
        records_by_name["meter (m)"]["quantity_id"]
        != records_by_name["second (s)"]["quantity_id"]
    )


def test_registry_keys_are_unique_and_quantities_match_graph_components() -> None:
    records = get_unit_catalog()["units"]
    records_by_name = {record["display_name"]: record for record in records}
    lookup_owners: dict[str, str] = {}
    for record in records:
        for lookup_key in (
            record["unit_id"],
            record["display_name"],
            *record["aliases"],
        ):
            previous = lookup_owners.setdefault(lookup_key, record["unit_id"])
            assert previous == record["unit_id"], lookup_key

    quantity_components: dict[str, set[str]] = {}
    for component in conversion_components(load_conversion_rows()):
        quantity_ids = {records_by_name[unit]["quantity_id"] for unit in component}
        assert len(quantity_ids) == 1
        quantity_id = quantity_ids.pop()
        assert quantity_id not in quantity_components
        quantity_components[quantity_id] = component

    assert len(quantity_components) == 65
    assert set(records_by_name) == {
        unit for component in quantity_components.values() for unit in component
    }


def test_lists_stable_unit_ids_globally_and_by_source_category() -> None:
    records_by_name = {
        record["display_name"]: record for record in get_unit_catalog()["units"]
    }

    assert len(list_unit_ids()) == len(list_units())
    assert records_by_name["meter (m)"]["unit_id"] in list_unit_ids("LENGTH")
    assert records_by_name["second (s)"]["unit_id"] not in list_unit_ids("LENGTH")


def test_supported_unit_labels_are_unique_after_spacing_normalization() -> None:
    labels_by_key: dict[str, list[str]] = {}
    for label in list_units():
        key = re.sub(r"\s+", "", label).casefold()
        labels_by_key.setdefault(key, []).append(label)

    collisions = {
        key: labels for key, labels in labels_by_key.items() if len(labels) > 1
    }
    assert collisions == {}


def test_supported_unit_labels_do_not_contain_known_ocr_spacing_errors() -> None:
    labels = list_units()

    assert all("( " not in label for label in labels)
    assert all(" ·m" not in label for label in labels)
    assert all("mil limeter" not in label for label in labels)
    assert all("](" not in label for label in labels)
    assert all("Kelvin" not in label for label in labels)


def test_every_bundled_direct_rule_applies_and_round_trips() -> None:
    rows = load_conversion_rows()

    assert len(rows) == 451
    round_tripped = 0
    with localcontext() as context:
        context.prec = 50
        for index, row in enumerate(rows, start=1):
            conversion = Conversion.from_mapping(row)
            source = Decimal("1")
            converted = conversion.apply(source)
            assert converted.is_finite(), f"row {index}: {row}"
            if conversion.can_apply_inverse():
                restored = conversion.apply_inverse(converted)
                error = abs(restored - source)
                assert error <= Decimal("1E-40"), (
                    f"row {index} round-trip error {error}: {row}"
                )
                round_tripped += 1
    assert round_tripped == len(rows)


def test_every_connected_bundled_unit_pair_can_be_converted() -> None:
    components = conversion_components(load_conversion_rows())

    converter = UnitConverter.from_package_data()
    tested_pairs = 0
    for component in components:
        for from_unit in component:
            for to_unit in component - {from_unit}:
                converted = converter.convert(1, from_unit, to_unit)
                assert converted.is_finite()
                restored = converter.convert(converted, to_unit, from_unit)
                relative_error = abs(restored - Decimal("1"))
                assert relative_error <= Decimal("2E-6"), (
                    f"{from_unit!r} -> {to_unit!r} -> {from_unit!r} "
                    f"had relative error {relative_error}"
                )
                tested_pairs += 1

    assert tested_pairs == 6108


def test_lists_supported_units_by_category() -> None:
    assert "LENGTH" in list_categories()

    length_units = list_units("LENGTH")
    assert "meter (m)" in length_units
    assert "mile (mi)" in length_units
    assert "second (s)" not in length_units

    assert list_units(" length ") == length_units


def test_raises_for_unknown_unit_category() -> None:
    with pytest.raises(ValueError, match="Unknown category"):
        list_units("NOT A CATEGORY")


def test_exposes_ui_unit_catalog() -> None:
    catalog = get_ui_unit_catalog()

    assert catalog["catalog_name"] == "Full List UI Categories"
    assert catalog["version"] == 1
    assert "all_units" not in catalog
    assert ("unit" + "converters") not in json.dumps(catalog).lower()
    assert ("Common" + " Converters") not in json.dumps(catalog)

    dimensions = next(
        category
        for category in catalog["categories"]
        if category["name"] == "Dimension Converters"
    )
    assert "Length" in dimensions["subcategories"]
    assert all(
        isinstance(subcategory, str) for subcategory in dimensions["subcategories"]
    )


def test_lists_ui_taxonomy_without_reading_internal_json() -> None:
    assert "Dimension Converters" in list_ui_categories()
    assert "Length" in list_ui_subcategories("Dimension Converters")
    assert list_ui_subcategories(" dimension converters ") == (
        list_ui_subcategories("Dimension Converters")
    )


def test_lists_units_by_ui_category_and_subcategory() -> None:
    dimension_units = list_ui_units("Dimension Converters")
    length_units = list_ui_units("Dimension Converters", "Length")
    length_unit_ids = list_ui_unit_ids("Dimension Converters", "Length")
    records_by_name = {
        record["display_name"]: record for record in get_unit_catalog()["units"]
    }

    assert "meter (m)" in dimension_units
    assert "liter (L)" in dimension_units
    assert "meter (m)" in length_units
    assert "mile (mi)" in length_units
    assert "liter (L)" not in length_units
    assert list_ui_units(" dimension converters ", " length ") == length_units
    assert length_unit_ids == tuple(
        records_by_name[unit]["unit_id"] for unit in length_units
    )


def test_ui_taxonomy_queries_validate_category_and_subcategory() -> None:
    with pytest.raises(ValueError, match="Unknown UI category"):
        list_ui_subcategories("not a category")
    with pytest.raises(ValueError, match="Unknown UI category"):
        list_ui_units("not a category")
    with pytest.raises(ValueError, match="Unknown UI subcategory"):
        list_ui_units("Dimension Converters", "not a subcategory")


def test_valid_ui_subcategory_without_supported_units_returns_empty_tuple() -> None:
    assert "Volume - Lumber" in list_ui_subcategories("Dimension Converters")
    assert list_ui_units("Dimension Converters", "Volume - Lumber") == ()
    assert list_ui_unit_ids("Dimension Converters", "Volume - Lumber") == ()


def test_catalog_accessors_isolate_cached_data_from_caller_mutation() -> None:
    unit_catalog = get_unit_catalog()
    ui_catalog = get_ui_unit_catalog()

    unit_catalog["units"][0]["display_name"] = "mutated"
    unit_catalog["categories"][0]["units"].clear()
    ui_catalog["categories"][0]["subcategories"].clear()

    fresh_unit_catalog = get_unit_catalog()
    fresh_ui_catalog = get_ui_unit_catalog()
    assert fresh_unit_catalog["units"][0]["display_name"] != "mutated"
    assert fresh_unit_catalog["categories"][0]["units"]
    assert fresh_ui_catalog["categories"][0]["subcategories"]
    assert list_units()


def test_supported_unit_catalog_has_direct_ui_unit_metadata() -> None:
    catalog = get_unit_catalog()
    units_by_label = {unit["display_name"]: unit for unit in catalog["units"]}

    meter = units_by_label["meter (m)"]
    assert meter["nist_categories"] == [{"category": "LENGTH"}]
    assert meter["ui_categories"] == [
        {
            "category": "Dimension Converters",
            "subcategory": "Length",
            "match_method": "full_list_unit",
            "matched_full_list_units": ["meter [m]"],
        }
    ]

    temperature = units_by_label["degree Fahrenheit (°F) [temperature]"]
    assert temperature["ui_categories"][0]["subcategory"] == "Temperature"
    assert temperature["ui_categories"][0]["category"] == "Heat Converters"

    interval = units_by_label["degree Fahrenheit (°F) [temperature interval]"]
    assert interval["ui_categories"][0]["subcategory"] == "Temperature Interval"


def test_ui_category_overrides_prevent_known_semantic_misclassifications() -> None:
    units_by_label = {
        unit["display_name"]: unit for unit in get_unit_catalog()["units"]
    }

    assert units_by_label["electronvolt (eV)"]["ui_categories"] == [
        {
            "category": "Mechanics Converters",
            "subcategory": "Energy",
            "match_method": "explicit_override",
        }
    ]
    assert units_by_label["coulomb per kilogram (C / kg)"]["ui_categories"] == [
        {
            "category": "Radiology Converters",
            "subcategory": "Radiation-Exposure",
            "match_method": "explicit_override",
        }
    ]

    intentionally_unmapped = (
        "square foot per hour (ft2 / h)",
        "square meter per second (m2 / s)",
        "foot to the fourth power (ft4)",
        "inch to the fourth power (in4)",
        "meter to the fourth power (m4)",
    )
    for label in intentionally_unmapped:
        record = units_by_label[label]
        assert record["ui_mapping_status"] == "unmapped"
        assert record["ui_categories"] == []
        assert record["ui_mapping_note"]

    assert all(
        unit["ui_mapping_status"] in {"mapped", "unmapped"}
        for unit in units_by_label.values()
    )


def test_every_ui_mapping_is_valid_and_status_is_semantically_consistent() -> None:
    unit_catalog = get_unit_catalog()
    ui_catalog = get_ui_unit_catalog()
    valid_pairs = {
        (category["name"], subcategory)
        for category in ui_catalog["categories"]
        for subcategory in category["subcategories"]
    }

    mapped_count = 0
    unmapped_count = 0
    for unit in unit_catalog["units"]:
        ui_categories = unit["ui_categories"]
        if unit["ui_mapping_status"] == "mapped":
            assert ui_categories
            assert "ui_mapping_note" not in unit
            mapped_count += 1
        else:
            assert ui_categories == []
            assert unit["ui_mapping_note"]
            unmapped_count += 1

        for mapping in ui_categories:
            assert (mapping["category"], mapping["subcategory"]) in valid_pairs
            assert mapping["match_method"] in {
                "full_list_unit",
                "nist_context",
                "explicit_override",
            }

    assert mapped_count + unmapped_count == unit_catalog["totals"]["unit_count"]
    assert unmapped_count == unit_catalog["totals"]["unmapped_ui_unit_count"]


def test_external_full_list_unit_catalog_is_neutral_reference_data() -> None:
    catalog_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "external"
        / "full_list_unit_catalog.json"
    )
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))

    assert catalog["catalog_name"] == "Full List Unit Catalog"
    assert catalog["totals"]["unit_reference_count"] > 1000
    assert ("unit" + "converters") not in json.dumps(catalog).lower()
    assert ("Common" + " Converters") not in json.dumps(catalog)

    dimensions = next(
        category
        for category in catalog["categories"]
        if category["name"] == "Dimension Converters"
    )
    length = next(
        subcategory
        for subcategory in dimensions["subcategories"]
        if subcategory["name"] == "Length"
    )
    assert "meter [m]" in length["units"]
    assert "kilometer [km]" in length["units"]


def test_development_only_data_is_not_runtime_package_data() -> None:
    runtime_path = files("unit_converter.data").joinpath(
        "physical_quantity_conversions.json"
    )
    runtime_registry_path = files("unit_converter.data").joinpath(
        "unit_registry.json"
    )
    development_path = (
        REPO_ROOT / "data" / "interim" / "nist_sp811_appendix_b9_by_quantity.json"
    )
    development_registry_path = REPO_ROOT / "data" / "registry" / "unit_registry.json"

    assert not runtime_path.is_file()
    assert not runtime_registry_path.is_file()
    assert development_path.is_file()
    assert development_registry_path.is_file()


def test_development_dependencies_have_one_source_and_a_named_lock() -> None:
    declared = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8").casefold()
    lock_text = (REPO_ROOT / "requirements" / "dev.lock").read_text(
        encoding="utf-8"
    )

    assert not (REPO_ROOT / "requirements.txt").exists()
    for dependency in (
        "build",
        "hatchling",
        "mkdocs",
        "mkdocs-material",
        "mypy",
        "pip-tools",
        "pypdf",
        "pytest",
        "ruff",
        "twine",
    ):
        assert dependency in declared
        assert re.search(rf"^{re.escape(dependency)}==", lock_text, re.MULTILINE)


def test_converts_corrected_mass_per_area_and_length_rows() -> None:
    assert convert(
        1,
        "pound per square inch (not pound force) (lb / in2)",
        "kilogram per square meter (kg / m2)",
    ) == Decimal("703.0696")
    assert convert(1, "denier", "kilogram per meter (kg / m)") == Decimal("1.111111E-7")


def test_applies_confirmed_nist_appendix_b9_erratum() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    data = json.loads(
        (repo_root / "src" / "unit_converter" / "data" / "conversions.json").read_text(
            encoding="utf-8"
        )
    )
    errata = json.loads(
        (
            repo_root / "data" / "overrides" / "nist_sp811_appendix_b9_errata.json"
        ).read_text(encoding="utf-8")
    )
    correction = errata["corrections"][0]
    matching_rows = [
        row
        for row in data["conversions"]
        if row["from"] == correction["from"] and row["to"] == correction["to"]
    ]

    assert correction["published_rule"] == "6.938112E+04"
    assert correction["corrected_rule"] == "6.938112E+00"
    assert matching_rows == [
        {
            "from": correction["from"],
            "to": correction["to"],
            "factor": correction["corrected_rule"],
        }
    ]
    with (
        repo_root / "data" / "interim" / "nist_sp811_appendix_b9_conversions.csv"
    ).open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    matching_csv_rows = [
        row
        for row in csv_rows
        if row["convert_from"] == correction["from"] and row["to"] == correction["to"]
    ]
    assert matching_csv_rows == [
        {
            "convert_from": correction["from"],
            "to": correction["to"],
            "rule": correction["corrected_rule"],
        }
    ]


def test_raises_for_incompatible_bundled_nist_units() -> None:
    with pytest.raises(IncompatibleUnitError):
        convert(1, "meter (m)", "second (s)")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
