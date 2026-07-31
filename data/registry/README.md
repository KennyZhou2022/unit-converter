# Stable unit registry

`unit_registry.json` is the development source of truth for stable `unit_id`
and `quantity_id` values. It is used when regenerating the runtime unit catalog
and is included in the source distribution, but not in the wheel.

Run the consistency check after changing conversion data or aliases:

```bash
python scripts/generate_unit_registry.py --check
```

Run without `--check` only after reviewing an intentional unit or physical-
quantity change.
