import sys
from decimal import Decimal, getcontext, localcontext
from pathlib import Path

import pytest

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from unit_converter import (
    AmbiguousConversionError,
    Conversion,
    ConversionError,
    IncompatibleUnitError,
    UnitConverter,
    UnitNotFoundError,
    can_convert,
    compatible_units,
)


def test_converts_using_factor() -> None:
    converter = UnitConverter([Conversion("m", "cm", factor="100")])

    assert converter.convert(Decimal("1.25"), "m", "cm") == Decimal("125.00")


def test_converts_using_reverse_factor() -> None:
    converter = UnitConverter([Conversion("m", "cm", factor="100")])

    assert converter.convert(250, "cm", "m") == Decimal("2.5")


def test_converts_using_formula() -> None:
    converter = UnitConverter([Conversion("degC", "degF", formula="x * 9 / 5 + 32")])

    assert converter.convert(0, "degC", "degF") == Decimal("32")


def test_converts_using_inverse_formula() -> None:
    converter = UnitConverter([Conversion("degC", "degF", formula="x * 9 / 5 + 32")])

    assert converter.convert(32, "degF", "degC") == Decimal("0")


@pytest.mark.parametrize(
    "factor",
    ["0", "-0", "NaN", "Infinity", "-Infinity", "not-a-number"],
)
def test_rejects_invalid_factors_when_conversion_is_created(factor: str) -> None:
    with pytest.raises(ConversionError):
        Conversion("from", "to", factor=factor)


@pytest.mark.parametrize(
    "formula",
    ["", "x +", "y + 1", "abs(x)", "x // 2", "True", "x.__class__"],
)
def test_rejects_invalid_formulas_when_conversion_is_created(formula: str) -> None:
    with pytest.raises(ConversionError):
        Conversion("from", "to", formula=formula)


def test_requires_exactly_one_rule_using_package_error_type() -> None:
    with pytest.raises(ConversionError):
        Conversion("from", "to")
    with pytest.raises(ConversionError):
        Conversion("from", "to", factor="1", formula="x")


@pytest.mark.parametrize(
    "value",
    [True, False, "not-a-number", "NaN", "Infinity", object()],
)
def test_wraps_invalid_values_in_conversion_error(value: object) -> None:
    converter = UnitConverter([Conversion("m", "cm", factor="100")])

    with pytest.raises(ConversionError):
        converter.convert(value, "m", "cm")  # type: ignore[arg-type]


def test_wraps_formula_division_by_zero_in_conversion_error() -> None:
    converter = UnitConverter(
        [Conversion("mpg", "liters-per-100-km", formula="235.215 / x")]
    )

    with pytest.raises(ConversionError, match="formula"):
        converter.convert(0, "mpg", "liters-per-100-km")
    with pytest.raises(ConversionError, match="inverse"):
        converter.convert(0, "liters-per-100-km", "mpg")


def test_converts_through_shared_intermediate_unit() -> None:
    converter = UnitConverter(
        [
            Conversion("BtuIT", "J", factor="1055.056"),
            Conversion("calIT", "J", factor="4.1868"),
        ]
    )

    assert converter.convert(1, "BtuIT", "calIT") == Decimal(
        "251.9957963122193560714626923"
    )


def test_converts_when_multiple_factor_paths_are_equivalent() -> None:
    converter = UnitConverter(
        [
            Conversion("source", "bridge-a", factor="2"),
            Conversion("bridge-a", "target", factor="3"),
            Conversion("source", "bridge-b", factor="4"),
            Conversion("bridge-b", "target", factor="1.5"),
        ]
    )

    assert converter.convert(1, "source", "target") == Decimal("6")


def test_raises_when_multiple_factor_paths_disagree() -> None:
    converter = UnitConverter(
        [
            Conversion("source", "bridge-a", factor="2"),
            Conversion("bridge-a", "target", factor="3"),
            Conversion("source", "bridge-b", factor="4"),
            Conversion("bridge-b", "target", factor="2"),
        ]
    )

    with pytest.raises(AmbiguousConversionError):
        converter.convert(1, "source", "target")


def test_raises_when_unit_is_unknown() -> None:
    converter = UnitConverter([Conversion("m", "cm", factor="100")])

    with pytest.raises(UnitNotFoundError, match="Unknown unit"):
        converter.convert(1, "m", "s")

    with pytest.raises(UnitNotFoundError, match="Unknown unit"):
        converter.convert(1, "s", "s")


def test_raises_when_units_are_not_connected() -> None:
    converter = UnitConverter(
        [
            Conversion("m", "cm", factor="100"),
            Conversion("s", "ms", factor="1000"),
        ]
    )

    with pytest.raises(IncompatibleUnitError, match="different physical quantities"):
        converter.convert(1, "m", "s")


def test_reports_convertibility_without_performing_arithmetic() -> None:
    converter = UnitConverter(
        [
            Conversion("m", "cm", factor="100"),
            Conversion("s", "ms", factor="1000"),
        ]
    )

    assert converter.can_convert("m", "cm")
    assert converter.can_convert("m", "m")
    assert not converter.can_convert("m", "s")
    assert not converter.can_convert("m", "unknown")


def test_conflicting_paths_are_not_reported_as_convertible() -> None:
    converter = UnitConverter(
        [
            Conversion("source", "bridge-a", factor="2"),
            Conversion("bridge-a", "target", factor="3"),
            Conversion("source", "bridge-b", factor="4"),
            Conversion("bridge-b", "target", factor="2"),
        ]
    )

    assert not converter.can_convert("source", "target")


def test_lists_compatible_units_including_the_requested_unit() -> None:
    converter = UnitConverter(
        [
            Conversion("m", "cm", factor="100"),
            Conversion("s", "ms", factor="1000"),
        ]
    )

    assert converter.compatible_units("m") == ("cm", "m")
    with pytest.raises(UnitNotFoundError, match="Unknown unit"):
        converter.compatible_units("unknown")


def test_top_level_compatibility_helpers_use_bundled_data() -> None:
    assert can_convert("meter (m)", "mile (mi)")
    assert not can_convert("meter (m)", "second (s)")
    assert not can_convert("unknown", "meter (m)")

    length_units = compatible_units("meter (m)")
    assert "meter (m)" in length_units
    assert "mile (mi)" in length_units
    assert "second (s)" not in length_units


def test_conversion_honors_active_decimal_context_without_mutating_it() -> None:
    converter = UnitConverter(
        [
            Conversion("Btu", "J", factor="1055.056"),
            Conversion("cal", "J", factor="4.1868"),
        ]
    )
    original_precision = getcontext().prec

    with localcontext() as context:
        context.prec = 6
        assert converter.convert(1, "Btu", "cal") == Decimal("251.997")
        assert context.prec == 6

    with localcontext() as context:
        context.prec = 12
        assert converter.convert(1, "Btu", "cal") == Decimal("251.995796312")
        assert context.prec == 12

    assert getcontext().prec == original_precision


def test_raises_when_conversion_path_is_ambiguous() -> None:
    converter = UnitConverter(
        [
            Conversion("degF", "degC", factor="0.5555556"),
            Conversion("degF", "degC", formula="(x - 32) / 1.8"),
        ]
    )

    with pytest.raises(AmbiguousConversionError):
        converter.convert(32, "degF", "degC")

    with pytest.raises(TypeError):
        converter.convert(32, "degF", "degC", category="TEMPERATURE")


def test_conversion_rejects_category_metadata() -> None:
    with pytest.raises(TypeError):
        Conversion("m", "cm", factor="100", category="LENGTH")  # type: ignore[call-arg]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
