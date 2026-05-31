"""Exception types raised by unit_converter."""


class ConversionError(Exception):
    """Base exception for conversion failures."""


class ConversionNotFoundError(ConversionError):
    """Raised when no suitable conversion rule exists."""


class UnitNotFoundError(ConversionNotFoundError):
    """Raised when a requested unit is not present in the conversion data."""


class IncompatibleUnitError(ConversionNotFoundError):
    """Raised when units are known but no conversion path connects them."""


class AmbiguousConversionError(ConversionError):
    """Raised when multiple conversion rules match a request."""
