# Errors

All package-specific conversion errors inherit from `ConversionError`.

## `UnitNotFoundError`

Raised when a requested unit does not exist in the bundled data.

```python
from unit_converter import UnitNotFoundError, convert

try:
    convert(1, "unknown", "second (s)")
except UnitNotFoundError as error:
    print(error)
```

## `IncompatibleUnitError`

Raised when both units are known, but no conversion path connects them.

```python
from unit_converter import IncompatibleUnitError, convert

try:
    convert(1, "meter (m)", "second (s)")
except IncompatibleUnitError as error:
    print(error)
```

## `AmbiguousConversionError`

Raised when multiple equal-length conversion paths match a request. The bundled
data qualifies known same-label conflicts such as temperature values versus
temperature intervals, so this should be uncommon for normal package data.

```python
from unit_converter import AmbiguousConversionError, convert

try:
    convert(1, "unit a", "unit b")
except AmbiguousConversionError as error:
    print(error)
```

## `ConversionNotFoundError`

Base class for not-found or not-connected conversion failures. It is useful if
calling code wants to handle missing units and incompatible units together.
