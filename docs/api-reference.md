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
from unit_converter import get_unit_catalog, list_units
```

`get_unit_catalog()` returns the full bundled catalog dictionary from
`unit_catalog.json`.

`list_units()` returns all globally supported unit labels.

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
