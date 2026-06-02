# Release Notes

This directory stores release notes for published versions.

Use one Markdown file per version:

```text
release/v1.0.0.md
release/v1.1.0.md
release/v1.2.0.md
release/v1.3.0.md
```

Keep the version in `VERSION` and `pyproject.toml` aligned before tagging a
release.

## GitHub Release Assets

Pushing a version tag builds the package and uploads the wheel and source
distribution to the matching GitHub Release.

```bash
git tag v1.3.0
git push origin v1.3.0
```

The workflow checks that:

- `VERSION` matches `pyproject.toml`.
- The tag matches the package version.
- `release/vX.Y.Z.md` exists.
- Generated catalog data and supported-unit documentation are up to date.
- Tests, MkDocs, package build, and `twine check` pass.

The release workflow can also be run manually from GitHub Actions with a tag
input such as `v1.3.0`.
