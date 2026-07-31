# nist-unit-converter

`nist-unit-converter` is a Python package for standards-backed unit conversion.
The bundled data comes from NIST Special Publication 811 (2008), Appendix B.9.

Documentation: <https://kennyzhou2022.github.io/unit-converter/>

## Usage

Install the prepared release from its Git tag:

```bash
python -m pip install \
  "nist-unit-converter @ git+https://github.com/KennyZhou2022/unit-converter.git@v2.0.0"
```

The distribution name used with `pip` is `nist-unit-converter`. The Python
import package remains `unit_converter`. The release workflow also attaches a
wheel and source distribution to the matching GitHub Release.

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

Use `list_categories()` and the optional `category` argument to browse one
category at a time:

```python
from unit_converter import list_categories, list_unit_ids, list_units

categories = list_categories()
length_units = list_units("LENGTH")
length_unit_ids = list_unit_ids("LENGTH")
```

Category matching ignores leading and trailing whitespace and is
case-insensitive.

Check a potential pair or build a target-unit list without attempting a
conversion:

```python
from unit_converter import can_convert, compatible_units

can_convert("meter (m)", "mile (mi)")  # True
length_targets = compatible_units("meter (m)")
```

`can_convert()` returns `False` for unknown or incompatible units.
`compatible_units()` returns sorted display names, includes the requested unit,
and raises `UnitNotFoundError` for an unknown unit.

UI code can query the display taxonomy directly:

```python
from unit_converter import (
    list_ui_categories,
    list_ui_subcategories,
    list_ui_unit_ids,
    list_ui_units,
)

ui_categories = list_ui_categories()
dimension_groups = list_ui_subcategories("Dimension Converters")
length_units = list_ui_units("Dimension Converters", "Length")
length_unit_ids = list_ui_unit_ids("Dimension Converters", "Length")
```

Use `get_unit_catalog()` and `get_ui_unit_catalog()` only when an application
needs the complete machine-readable metadata. Every unit record includes a
stable `unit_id`, physical `quantity_id`, display name, aliases, NIST source
categories, and reviewed UI mappings.

Display names remain valid conversion inputs. Stable IDs are recommended for
stored configuration and integrations because display wording can evolve:

```python
from unit_converter import convert, get_unit_catalog

meter = next(
    unit
    for unit in get_unit_catalog()["units"]
    if unit["display_name"] == "meter (m)"
)
kilometer = next(
    unit
    for unit in get_unit_catalog()["units"]
    if unit["display_name"] == "kilometer (km)"
)
result = convert(1, meter["unit_id"], kilometer["unit_id"])
```

`ui_categories[*].match_method` records whether a mapping came from a direct
full-list match, NIST context, or an explicit reviewed override. A unit with no
semantically correct UI category is marked `ui_mapping_status: "unmapped"`
instead of being placed in a merely dimensionally similar category.

The supported unit list is documented in `docs/supported-units.md`, with a
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

## Decimal Arithmetic

`convert()` returns `Decimal`, and arithmetic follows the active
`decimal` context. The package does not accept a precision argument and does
not infer significant figures from the input.

Use `localcontext()` when an application needs an explicit working precision:

```python
from decimal import localcontext

from unit_converter import convert

with localcontext() as context:
    context.prec = 12
    result = convert(
        1,
        "British thermal unitIT (BtuIT)",
        "calorieIT (calIT)",
    )
```

The package reads the active context but does not modify it.

## Data Notes

- Appendix B.8 and Appendix B.9 contain the same conversion factors in
  different order. This project extracts Appendix B.9 because it preserves the
  source grouping from the standard.
- The source PDF lives under `standards/raw/`.
- The review CSV is generated at
  `data/interim/nist_sp811_appendix_b9_conversions.csv`.
- The development-only physical-quantity view is generated at
  `data/interim/nist_sp811_appendix_b9_by_quantity.json`; it is not included in
  the wheel.
- Runtime data under `src/unit_converter/data/` contains conversion rules, the
  supported-unit catalog, and the UI taxonomy.
- `src/unit_converter/data/ui_unit_catalog.json` is the installed runtime UI
  category tree loaded by `get_ui_unit_catalog()`.
- `data/external/full_list_categories.json` is the development source copy of
  the UI category tree.
- `data/external/full_list_unit_catalog.json` is a development reference list
  of candidate unit labels for future coverage work. It is not used by runtime
  conversion.
- `src/unit_converter/data/unit_catalog.json` stores direct unit metadata in
  `units`; every unit record includes stable identity, display, alias, NIST,
  and UI metadata.
- `data/registry/unit_registry.json` is the development source of truth for
  stable `unit_id` and `quantity_id` values. Runtime identity metadata is
  included directly in the supported-unit catalog, so the registry is not
  duplicated in the wheel.
- Confirmed corrections to published source rows are recorded under
  `data/overrides/` and applied during extraction.
- The runtime converter can use direct rules, reversible rules, and connected
  intermediate units. Numerically equivalent factor paths are resolved
  automatically; conflicting paths remain an error.
- Convertible-pair totals in the catalog are calculated with the same
  `UnitConverter.can_convert()` model used at runtime.
- Source labels with different meanings are qualified during data generation so
  runtime unit names are globally unique. Temperature values use
  `[temperature]`; temperature intervals use `[temperature interval]`.

## Documentation

The GitHub Pages site is intentionally user-facing. It covers installation,
basic conversion, supported units, API signatures, and error handling.

Open it here: <https://kennyzhou2022.github.io/unit-converter/>

The site is built with MkDocs from `docs/` and deployed by
`.github/workflows/pages.yml`.

## Development

Install directly from `pyproject.toml`:

```bash
python -m pip install -e ".[dev,docs]"
```

For a reproducible contributor environment, use the generated lock:

```bash
python -m pip install -r requirements/dev.lock
python -m pip install --no-build-isolation --no-deps -e .
```

Run the complete local quality checks:

```bash
python -m pip check
python -m pytest
python -m ruff check .
python -m mypy src
python -m mkdocs build --strict
python -m build --no-isolation
python -m twine check dist/*
```

Regenerate derived data from the source PDF:

```bash
python scripts/extract_nist_sp811_appendix_b9.py
python scripts/generate_unit_registry.py
python scripts/map_ui_categories_to_units.py
python scripts/generate_supported_units_doc.py
```

Regenerate the external full-list reference and UI category tree only when
their source data changes:

```bash
python scripts/generate_full_list_unit_catalog.py --home-url <full-list-home-url>
python scripts/generate_ui_unit_catalog.py
```

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

Exactly one of `factor` or `formula` must be provided. Formulas can use `x`,
numeric constants, parentheses, unary signs, and `+`, `-`, `*`, `/`, or `**`.
Factors, affine formulas, and constant-over-`x` formulas can be used in the
opposite direction when mathematically valid.

`Conversion` accepts only the two unit names and exactly one rule. Category and
subcategory metadata are not part of the conversion API.
