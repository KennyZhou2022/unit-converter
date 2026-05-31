"""Standards-backed unit conversion."""

from importlib.metadata import PackageNotFoundError, version

from unit_converter.catalog import get_unit_catalog, list_categories, list_units
from unit_converter.converter import Conversion, UnitConverter, convert
from unit_converter.exceptions import (
    AmbiguousConversionError,
    ConversionError,
    ConversionNotFoundError,
    IncompatibleUnitError,
    UnitNotFoundError,
)

try:
    __version__ = version("unit-converter")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "Conversion",
    "AmbiguousConversionError",
    "ConversionError",
    "ConversionNotFoundError",
    "IncompatibleUnitError",
    "UnitConverter",
    "UnitNotFoundError",
    "__version__",
    "convert",
    "get_unit_catalog",
    "list_categories",
    "list_units",
]
