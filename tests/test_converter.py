import sys
from decimal import Decimal
from pathlib import Path

import pytest

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from unit_converter import (
    AmbiguousConversionError,
    Conversion,
    IncompatibleUnitError,
    UnitConverter,
    UnitNotFoundError,
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


def test_converts_through_shared_intermediate_unit() -> None:
    converter = UnitConverter(
        [
            Conversion("BtuIT", "J", factor="1055.056", category="ENERGY"),
            Conversion("calIT", "J", factor="4.1868", category="ENERGY"),
        ]
    )

    assert converter.convert(1, "BtuIT", "calIT") == Decimal(
        "251.9957963122193560714626923"
    )


def test_raises_when_unit_is_unknown() -> None:
    converter = UnitConverter([Conversion("m", "cm", factor="100")])

    with pytest.raises(UnitNotFoundError, match="Unknown unit"):
        converter.convert(1, "m", "s")

    with pytest.raises(UnitNotFoundError, match="Unknown unit"):
        converter.convert(1, "s", "s")


def test_raises_when_units_are_not_connected() -> None:
    converter = UnitConverter(
        [
            Conversion("m", "cm", factor="100", category="LENGTH"),
            Conversion("s", "ms", factor="1000", category="TIME"),
        ]
    )

    with pytest.raises(IncompatibleUnitError, match="different physical quantities"):
        converter.convert(1, "m", "s")


def test_raises_when_conversion_path_is_ambiguous() -> None:
    converter = UnitConverter(
        [
            Conversion("degF", "degC", factor="0.5555556", category="INTERVAL"),
            Conversion(
                "degF",
                "degC",
                formula="(x - 32) / 1.8",
                category="TEMPERATURE",
            ),
        ]
    )

    with pytest.raises(AmbiguousConversionError):
        converter.convert(32, "degF", "degC")

    with pytest.raises(TypeError):
        converter.convert(32, "degF", "degC", category="TEMPERATURE")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
