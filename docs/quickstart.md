# Quickstart

## Install

```bash
python -m pip install \
  "nist-unit-converter @ git+https://github.com/KennyZhou2022/unit-converter.git@v2.0.0"
```

The install name is `nist-unit-converter`; Python code imports
`unit_converter`. The same release is also available as a wheel on its GitHub
Release page.

## Convert a Value

```python
from unit_converter import convert

speed = convert(
    1,
    "mile per hour (mi / h)",
    "kilometer per hour (km / h)",
)

print(speed)  # 1.609344
```

`convert()` returns `Decimal` so decimal factors from the standard are not
immediately collapsed into binary floating point values.

## Convert Another Unit Pair

```python
from unit_converter import convert

energy = convert(
    1,
    "British thermal unitIT (BtuIT)",
    "calorieIT (calIT)",
)

print(energy)  # 251.9957963122193560714626923
```

## Decimal Context

Conversion arithmetic follows the active `decimal` context. There is no
precision argument.

```python
from decimal import localcontext

from unit_converter import convert

with localcontext() as context:
    context.prec = 12
    energy = convert(
        1,
        "British thermal unitIT (BtuIT)",
        "calorieIT (calIT)",
    )

print(energy)  # 251.995796312
```

Use `Decimal` or a string input when the exact decimal representation of the
input matters. The package does not modify the caller's decimal context.

## Temperature Values And Intervals

Temperature values and temperature intervals use different explicit unit
labels:

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

## Browse Supported Units

```python
from unit_converter import list_categories, list_unit_ids, list_units

units = list_units()
categories = list_categories()
length_units = list_units("LENGTH")
length_unit_ids = list_unit_ids("LENGTH")
```

When a category is provided, `list_units()` returns only units in that category.
Category matching ignores leading and trailing whitespace and is
case-insensitive.

The category argument uses the source category names from the bundled standard.

## Check Compatible Units

```python
from unit_converter import can_convert, compatible_units

assert can_convert("meter (m)", "mile (mi)")
assert not can_convert("meter (m)", "second (s)")

length_targets = compatible_units("meter (m)")
```

`can_convert()` returns `False` for unknown and incompatible units.
`compatible_units()` returns sorted display names, includes the selected unit,
and raises `UnitNotFoundError` when the unit is unknown.

## Build A Unit Picker

Use the UI helpers to build category, subcategory, and unit controls:

```python
from unit_converter import (
    list_ui_categories,
    list_ui_subcategories,
    list_ui_unit_ids,
    list_ui_units,
)

categories = list_ui_categories()
subcategories = list_ui_subcategories("Dimension Converters")
length_units = list_ui_units("Dimension Converters", "Length")
length_unit_ids = list_ui_unit_ids("Dimension Converters", "Length")
```

Omit the subcategory to get every mapped unit in one UI category. A valid
subcategory with no units in the current data returns an empty tuple. Unknown
UI categories or subcategories raise `ValueError`.

Use `get_unit_catalog()["units"]` only when the UI also needs the complete
metadata record:

```python
from unit_converter import get_unit_catalog

catalog = get_unit_catalog()

meter = next(
    unit for unit in catalog["units"] if unit["display_name"] == "meter (m)"
)

print(meter["unit_id"])
print(meter["display_name"])
print(meter["nist_categories"])
print(meter["ui_categories"])
```

Each unit record has:

- `unit_id`: the stable identifier recommended for stored application data.
- `quantity_id`: the physical-quantity identity shared by convertible units.
- `display_name`: the user-facing name, also accepted by `convert()`.
- `aliases`: older accepted names retained for compatibility.
- `nist_categories`: source category metadata from the bundled standard.
- `ui_categories`: display category and subcategory metadata for user
  interfaces.

`ui_mapping_status` is `mapped` or `unmapped`. An unmapped unit stays available
for conversion but is not assigned to a semantically incorrect UI group.
