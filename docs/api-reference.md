# API Reference

## `convert`

```python
convert(value, from_unit, to_unit)
```

Converts `value` with the bundled conversion data.

- `value`: `int`, `float`, `str`, or `Decimal`.
- `from_unit`: stable unit ID, exact display name, or registered alias.
- `to_unit`: stable unit ID, exact display name, or registered alias.
- Returns: `Decimal`.

Unknown units, incompatible units, and invalid arithmetic raise package-specific
errors described on the [Errors](errors.md) page.

## Package Version

```python
from unit_converter import __version__
```

`__version__` contains the installed distribution version, such as `"2.0.0"`.

## Compatibility Helpers

```python
can_convert(from_unit, to_unit)
compatible_units(unit)
```

`can_convert()` returns whether the bundled graph has a usable conversion path.
It returns `False` when either unit is unknown, the units are incompatible, or
available paths conflict. It does not evaluate a numeric value, so a particular
value can still fail a formula domain check such as division by zero.

`compatible_units()` returns a sorted tuple of display names that can be
reached from the requested source unit. The tuple includes the source unit's
display name. Stable IDs, display names, and registered aliases are accepted;
an unknown source raises `UnitNotFoundError`.

```python
from unit_converter import can_convert, compatible_units

assert can_convert("meter (m)", "mile (mi)")
length_targets = compatible_units("meter (m)")
```

## `UnitConverter`

Most users should call the top-level helpers. Create one package converter when
an application wants to reuse the same object explicitly:

```python
from unit_converter import UnitConverter

converter = UnitConverter.from_package_data()
result = converter.convert(
    1,
    "watt hour (W · h)",
    "kilowatt hour (kW · h)",
)
```

`UnitConverter` provides `convert()`, `can_convert()`, and
`compatible_units()`. `available_units()` returns display names,
`available_unit_ids()` returns stable IDs for the bundled converter and the
supplied unit names for a custom converter, and `available()` returns the
direct rule pairs registered on that converter. The top-level helpers cache
their own package converter.

## Source Catalog Helpers

```python
from unit_converter import list_categories, list_unit_ids, list_units

categories = list_categories()
all_units = list_units()
length_units = list_units("LENGTH")
length_unit_ids = list_unit_ids("LENGTH")
```

`list_categories()` returns NIST source category names. `list_units()` and
`list_unit_ids()` return all supported display names or stable IDs when no
category is supplied, and the requested source category when one is supplied.

Category matching ignores leading and trailing whitespace and is
case-insensitive. Unknown source categories raise `ValueError`.

## UI Catalog Helpers

```python
from unit_converter import (
    list_ui_categories,
    list_ui_subcategories,
    list_ui_unit_ids,
    list_ui_units,
)

categories = list_ui_categories()
subcategories = list_ui_subcategories("Dimension Converters")
units = list_ui_units("Dimension Converters", "Length")
unit_ids = list_ui_unit_ids("Dimension Converters", "Length")
```

`list_ui_units(category)` returns the mapped units across every subcategory in
that UI category. Supplying `subcategory` narrows the result. Category and
subcategory matching ignores leading and trailing whitespace and is
case-insensitive.

The UI taxonomy can contain a valid subcategory for which the current NIST data
has no units; in that case the unit helpers return an empty tuple. Unknown UI
categories or subcategories raise `ValueError`.

## Catalog Metadata

`get_unit_catalog()` returns an isolated copy of the complete supported-unit
catalog. Its `units` array contains stable identity, aliases, NIST source
categories, and direct UI mappings:

```python
{
    "unit_id": "unit.u0271",
    "quantity_id": "quantity.q0022",
    "display_name": "meter (m)",
    "aliases": [],
    "nist_categories": [{"category": "LENGTH"}],
    "ui_mapping_status": "mapped",
    "ui_categories": [
        {
            "category": "Dimension Converters",
            "subcategory": "Length",
            "match_method": "full_list_unit",
            "matched_full_list_units": ["meter [m]"],
        }
    ],
}
```

`get_ui_unit_catalog()` returns an isolated copy of the UI taxonomy. Unit
membership is available through the UI helper functions and on unit records in
`get_unit_catalog()`. Mutating either returned dictionary does not affect later
calls.

Use display names in user interfaces and stable IDs in stored settings or
database records.

## Decimal Context

Conversion arithmetic follows the active `decimal` context. There is no
precision argument, and the package does not infer significant figures from
the input.

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

The active context can change rounding and the number of returned digits. The
package does not modify the caller's context.

## Advanced: Custom Conversions

`Conversion` represents one direct custom rule. Use it to build a temporary
`UnitConverter` when the bundled standard does not cover an application-specific
unit.

```python
from unit_converter import Conversion, UnitConverter

converter = UnitConverter(
    [
        Conversion("m", "cm", factor="100"),
        Conversion("degC", "degF", formula="x * 9 / 5 + 32"),
    ]
)

print(converter.convert(2, "m", "cm"))       # 200
print(converter.convert(0, "degC", "degF"))  # 32
```

Exactly one of `factor` or `formula` must be provided. Formulas can use `x`,
numeric constants, parentheses, unary signs, and `+`, `-`, `*`, `/`, or `**`.
Factors are reversible. Affine formulas and constant-over-`x` formulas are
reversible when mathematically valid.

The constructor accepts `from_unit`, `to_unit`, and exactly one of `factor` or
`formula`. Category and subcategory metadata are not accepted.
