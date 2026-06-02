# Quickstart

## Install

```bash
python -m pip install unit-converter
```

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
from unit_converter import list_categories, list_units

units = list_units()
categories = list_categories()
length_units = list_units("LENGTH")
```

When a category is provided, `list_units()` returns only units in that category.
Category matching ignores leading and trailing whitespace and is
case-insensitive.

The category argument uses the source category names from the bundled standard.

## Build A Unit Picker

Use `get_ui_unit_catalog()` for the display category tree:

```python
from unit_converter import get_ui_unit_catalog

ui_catalog = get_ui_unit_catalog()

for category in ui_catalog["categories"]:
    print(category["name"])
    for subcategory in category["subcategories"]:
        print("  ", subcategory)
```

Use `get_unit_catalog()["units"]` when the UI needs unit labels together with
their display categories:

```python
from unit_converter import get_unit_catalog

catalog = get_unit_catalog()

meter = next(unit for unit in catalog["units"] if unit["label"] == "meter (m)")

print(meter["label"])
print(meter["nist_categories"])
print(meter["ui_categories"])
```

Each unit record has:

- `label`: the exact label to pass to `convert()`.
- `nist_categories`: source category metadata from the bundled standard.
- `ui_categories`: display category and subcategory metadata for user
  interfaces.

`ui_categories[*].match_method` is `full_list_unit` when the supported unit
matched a full-list unit label directly. It is `nist_context` when the supported
unit was placed into the closest UI group from its source category context.
