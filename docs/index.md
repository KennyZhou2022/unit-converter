# unit-converter

`unit-converter` is a standards-backed Python package for converting values
between supported units.

The package currently uses conversion factors extracted from NIST Special
Publication 811 (2008), Appendix B.9. The data is bundled with the package, so
runtime conversion does not depend on a local PDF or CSV file.

## What You Can Do

- Convert values with `convert(value, from_unit, to_unit)`.
- Browse supported unit labels by category.
- Load a UI category tree for building unit picker interfaces.
- Read direct unit metadata with both source categories and UI categories.
- Use explicit labels for temperature values and temperature intervals.
- Handle unknown units and incompatible units with package-specific errors.

## Minimal Example

```python
from unit_converter import convert

speed = convert(
    1,
    "mile per hour (mi / h)",
    "kilometer per hour (km / h)",
)

print(speed)  # 1.609344
```

## Start Here

- New users should begin with [Quickstart](quickstart.md).
- To browse the full supported unit catalog, see
  [Supported Units](supported-units.md).
- To build a unit picker or inspect catalog metadata, see
  [Quickstart](quickstart.md#build-a-unit-picker).
- To see function signatures and errors, use [API Reference](api-reference.md)
  and [Errors](errors.md).
