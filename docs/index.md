# unit-converter

`unit-converter` is a standards-backed Python package for converting values
between supported units.

The package currently uses conversion factors extracted from NIST Special
Publication 811 (2008), Appendix B.9. The data is bundled with the package, so
runtime conversion does not depend on a local PDF or CSV file.

## What You Can Do

- Convert values with `convert(value, from_unit, to_unit)`.
- Browse supported unit labels by category.
- Use explicit labels for temperature values and temperature intervals.
- Handle unknown units and incompatible units with package-specific errors.

## Current Data Set

| Metric | Count |
|---|---:|
| Source groups | 30 |
| Direct conversion rules | 451 |
| Unique supported units | 467 |
| Ordered convertible unit pairs | 5926 |

## Start Here

- New users should begin with [Quickstart](quickstart.md).
- To browse the full supported unit catalog, see
  [Supported Units](supported-units.md).
- To see function signatures and errors, use
  [API Reference](api-reference.md) and [Errors](errors.md).
