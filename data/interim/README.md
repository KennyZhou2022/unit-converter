# Interim data

Put generated review artifacts extracted from the source standard here.

Current generated review files:

```text
nist_sp811_appendix_b9_conversions.csv
nist_sp811_appendix_b9_by_quantity.json
```

The expected minimum CSV columns are:

```csv
convert_from,to,rule
m,cm,100
degC,degF,x * 9 / 5 + 32
```

For NIST SP 811, use `scripts/extract_nist_sp811_appendix_b9.py` to regenerate
the CSV, runtime conversion JSON, unit-catalog base, and development-only
physical-quantity JSON from the source PDF. The physical-quantity JSON remains
outside `src/` because runtime code does not consume it.

The extractor applies reviewed entries from
`data/overrides/nist_sp811_appendix_b9_errata.json` and fails if an override no
longer matches the published row.

`scripts/convert_csv_to_package_data.py` is a generic CSV-to-package-data
helper for future standards.
