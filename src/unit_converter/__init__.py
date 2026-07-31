"""Standards-backed unit conversion."""

from importlib.metadata import PackageNotFoundError, version

from unit_converter.catalog import (
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
from unit_converter.converter import (
    Conversion,
    UnitConverter,
    can_convert,
    compatible_units,
    convert,
)
from unit_converter.exceptions import (
    AmbiguousConversionError,
    ConversionError,
    ConversionNotFoundError,
    IncompatibleUnitError,
    UnitNotFoundError,
)

try:
    __version__ = version("nist-unit-converter")
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
    "can_convert",
    "compatible_units",
    "convert",
    "get_ui_unit_catalog",
    "get_unit_catalog",
    "list_categories",
    "list_ui_categories",
    "list_ui_subcategories",
    "list_ui_unit_ids",
    "list_ui_units",
    "list_unit_ids",
    "list_units",
]
