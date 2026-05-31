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
from unit_converter import get_unit_catalog, list_categories, list_units

catalog = get_unit_catalog()
units = list_units()
categories = list_categories()
length_units = list_units("LENGTH")
```

When a category is provided, `list_units()` returns only units in that category.
Category matching ignores leading and trailing whitespace and is
case-insensitive.
