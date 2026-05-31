# Interim data

Put reviewed CSV files extracted from the source standard here.

Current generated file:

```text
nist_sp811_appendix_b9_conversions.csv
```

The expected minimum CSV columns are:

```csv
convert_from,to,rule
m,cm,100
degC,degF,x * 9 / 5 + 32
```

For NIST SP 811, use `scripts/extract_nist_sp811_appendix_b9.py` to regenerate the CSV, package JSON, and physical-quantity category JSON from the source PDF.

`scripts/convert_csv_to_package_data.py` is kept as a generic CSV-to-package-data helper for future standards.
