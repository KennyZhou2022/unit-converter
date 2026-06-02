# API Reference

## `convert`

```python
convert(
    value,
    from_unit,
    to_unit,
)
```

Converts `value` from `from_unit` to `to_unit` using bundled package data.

Arguments:

- `value`: `int`, `float`, `str`, or `Decimal`.
- `from_unit`: exact unit label from the catalog.
- `to_unit`: exact unit label from the catalog.

Returns:

- `Decimal`

## `UnitConverter`

Most users should call the top-level `convert()` function. Use
`UnitConverter.from_package_data()` when making many conversions in one process
and you want to reuse the loaded converter.

```python
from unit_converter import UnitConverter

converter = UnitConverter.from_package_data()
result = converter.convert(
    1,
    "watt hour (W · h)",
    "kilowatt hour (kW · h)",
)
```

The top-level `convert()` function also caches the package converter.

## Catalog Helpers

```python
from unit_converter import (
    get_ui_unit_catalog,
    get_unit_catalog,
    list_categories,
    list_units,
)
```

`get_unit_catalog()` returns the full bundled catalog dictionary from
`unit_catalog.json`. Its `units` array contains one record per supported unit,
including direct `nist_categories` and `ui_categories` metadata.

Example unit record:

```python
{
    "label": "meter (m)",
    "nist_categories": [{"category": "LENGTH"}],
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

`ui_categories[*].match_method` is either `full_list_unit` for a direct
full-list label match or `nist_context` for a fallback placement into the
closest full-list UI group.

`get_ui_unit_catalog()` returns the bundled UI-oriented catalog dictionary from
`ui_unit_catalog.json`. It provides the full-list UI category tree only; unit
membership is stored directly on unit records in `unit_catalog.json`.

`list_categories()` returns the supported source category names from the bundled
catalog.

`list_units()` returns all globally supported unit labels.

`list_units(category)` returns only unit labels in the requested category.
Category matching ignores leading and trailing whitespace and is
case-insensitive. Unknown categories raise `ValueError`.

Use `list_units()` when you only need exact unit labels for conversion. Use
`get_unit_catalog()["units"]` when a UI needs labels plus category metadata.

## Advanced: Custom Conversions

`Conversion` represents one direct rule. This is an advanced escape hatch for
building a temporary converter with your own rules.

```python
from unit_converter import Conversion, UnitConverter

converter = UnitConverter(
    [
        Conversion("m", "cm", factor="100"),
        Conversion("degC", "degF", formula="x * 9 / 5 + 32"),
    ]
)

print(converter.convert(2, "m", "cm"))
print(converter.convert(0, "degC", "degF"))
```

Exactly one of `factor` or `formula` must be provided.
For `factor`, the input value is multiplied by the factor. For `formula`, use
`x` as the input value. Reversible factors and supported reversible formulas
can also be used in the opposite direction.
