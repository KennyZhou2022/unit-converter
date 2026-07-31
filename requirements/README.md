# Development dependency lock

`pyproject.toml` is the authoritative dependency declaration. The
`dev.lock` file pins the build system plus the combined `dev` and `docs` extras
for a reproducible contributor environment.

Regenerate it after changing either extra:

```bash
python -m piptools compile \
  --strip-extras \
  --all-build-deps \
  --extra dev \
  --extra docs \
  --output-file requirements/dev.lock \
  pyproject.toml
```

Install the locked dependencies and this checkout:

```bash
python -m pip install -r requirements/dev.lock
python -m pip install --no-build-isolation --no-deps -e .
```
