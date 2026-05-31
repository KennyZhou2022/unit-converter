# unit-converter

`unit-converter` is a general-purpose Python package for standards-backed unit
conversion. The current data source is NIST Special Publication 811 (2008),
Appendix B.9.

## Current Data Set

| Metric | Count |
|---|---:|
| Source groups | 30 |
| Direct conversion rules | 451 |
| Unique supported units | 467 |
| Ordered convertible unit pairs | 5926 |

## Usage

Install the package:

```bash
python -m pip install unit-converter
```

Convert values with the top-level `convert()` function:

```python
from unit_converter import convert

result = convert(
    1,
    "mile per hour (mi / h)",
    "kilometer per hour (km / h)",
)

print(result)  # 1.609344
```

The package can convert between units that are not directly listed as a pair,
as long as they are connected through supported package data:

```python
from unit_converter import convert

btu_in_calorie = convert(
    1,
    "British thermal unitIT (BtuIT)",
    "calorieIT (calIT)",
)

print(btu_in_calorie)  # 251.9957963122193560714626923
```

Temperature values and temperature intervals use different unit labels, so no
category argument is needed:

```python
from unit_converter import convert

temperature = convert(
    32,
    "degree Fahrenheit (°F) [temperature]",
    "degree Celsius (°C) [temperature]",
)

temperature_interval = convert(
    18,
    "degree Fahrenheit (°F) [temperature interval]",
    "degree Celsius (°C) [temperature interval]",
)
```

## Supported Units

Use `list_units()` to get the full set of supported unit labels:

```python
from unit_converter import list_units

units = list_units()
```

Use `get_unit_catalog()` when an application needs the full machine-readable
catalog:

```python
from unit_converter import get_unit_catalog

catalog = get_unit_catalog()
```

The generated catalog is also documented in `docs/supported-units.md`, with a
category filter for the GitHub Pages site.

## Error Handling

```python
from unit_converter import IncompatibleUnitError, UnitNotFoundError, convert

try:
    convert(1, "meter (m)", "second (s)")
except IncompatibleUnitError:
    ...

try:
    convert(1, "unknown", "second (s)")
except UnitNotFoundError:
    ...
```

## Data Notes

- Appendix B.8 and Appendix B.9 contain the same conversion factors in
  different order. This project extracts Appendix B.9 because it preserves the
  source grouping from the standard.
- The source PDF lives under `standards/raw/`.
- The review CSV is generated at
  `data/interim/nist_sp811_appendix_b9_conversions.csv`.
- Runtime data is packaged as JSON under `src/unit_converter/data/`.
- The runtime converter can use direct rules, reversible rules, and connected
  intermediate units.
- Source labels with different meanings are qualified during data generation so
  runtime unit names are globally unique. Temperature values use
  `[temperature]`; temperature intervals use `[temperature interval]`.

## Documentation

The GitHub Pages site is intentionally user-facing. It covers installation,
basic conversion, supported units, API signatures, and error handling.

The site is built with MkDocs from `docs/` and deployed by
`.github/workflows/pages.yml`.

## Development

```bash
python -m pip install -e ".[dev,docs]"
python -m pytest
python -m ruff check .
python -m mypy src
```

Regenerate derived data from the source PDF:

```bash
python scripts/extract_nist_sp811_appendix_b9.py
python scripts/generate_supported_units_doc.py
```

## Roadmap

1. Manually review complex conversions, especially temperature, fuel
   consumption, and compound heat units.
2. Decide from real usage whether to add unit aliases, input normalization,
   dimensional validation, or multi-standard version support.
3. After publishing the wheel, update the documentation install command from
   editable development install to stable package install.

## Advanced: Custom Conversions

Most users should use the bundled data through `convert()`. If you need a
temporary converter with your own rules, create a `UnitConverter` from
`Conversion` objects:

```python
from unit_converter import Conversion, UnitConverter

converter = UnitConverter(
    [
        Conversion(from_unit="m", to_unit="cm", factor="100"),
        Conversion(from_unit="degC", to_unit="degF", formula="x * 9 / 5 + 32"),
    ]
)

print(converter.convert(2, "m", "cm"))       # 200
print(converter.convert(0, "degC", "degF"))  # 32
```

Exactly one of `factor` or `formula` must be provided. For `formula`, use `x`
as the input value. Reversible factors and supported reversible formulas can
also be used in the opposite direction.
