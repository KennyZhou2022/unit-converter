# Errors

All package-specific conversion errors inherit from `ConversionError`.

## `ConversionError`

Raised for invalid numeric values, non-finite or zero factors, unsupported
formula syntax, and arithmetic failures such as division by zero. Catch this
base type when one response is appropriate for every package conversion error.

```python
from unit_converter import ConversionError, convert

try:
    convert(True, "meter (m)", "kilometer (km)")
except ConversionError as error:
    print(error)
```

## `UnitNotFoundError`

Raised when a requested unit does not exist in the bundled data. The
`can_convert()` helper returns `False` instead of raising for unknown units;
`convert()` and `compatible_units()` raise this error.

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

Raised when multiple shortest conversion paths conflict. The bundled data uses
explicit labels for known same-label conflicts and resolves equivalent rounded
factor paths, so this is primarily relevant to custom converters.

```python
from unit_converter import AmbiguousConversionError, Conversion, UnitConverter

converter = UnitConverter(
    [
        Conversion("source", "bridge-a", factor="2"),
        Conversion("bridge-a", "target", factor="3"),
        Conversion("source", "bridge-b", factor="4"),
        Conversion("bridge-b", "target", factor="2"),
    ]
)

try:
    converter.convert(1, "source", "target")
except AmbiguousConversionError as error:
    print(error)
```

## `ConversionNotFoundError`

Base class for not-found or not-connected conversion failures. It is useful if
calling code wants to handle missing units and incompatible units together.
