import sys
from decimal import Decimal
from pathlib import Path

import pytest

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from unit_converter import (
    IncompatibleUnitError,
    UnitNotFoundError,
    convert,
    get_unit_catalog,
    list_categories,
    list_units,
)


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


def test_exposes_supported_unit_catalog() -> None:
    catalog = get_unit_catalog()

    assert catalog["totals"]["direct_conversion_count"] == 451
    assert catalog["totals"]["unit_count"] == 467
    assert "calorieIT (calIT)" in list_units()
    assert "degree Fahrenheit (°F) [temperature]" in list_units()
    assert "degree Fahrenheit (°F) [temperature interval]" in list_units()


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


def test_converts_corrected_mass_per_area_and_length_rows() -> None:
    assert convert(
        1,
        "pound per square inch (not pound force) (lb / in2)",
        "kilogram per square meter (kg / m2)",
    ) == Decimal("703.0696")
    assert convert(1, "denier", "kilogram per meter (kg / m)") == Decimal(
        "1.111111E-7"
    )


def test_raises_for_incompatible_bundled_nist_units() -> None:
    with pytest.raises(IncompatibleUnitError):
        convert(1, "meter (m)", "second (s)")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
