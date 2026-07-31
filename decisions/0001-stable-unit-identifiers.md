# ADR 0001: Stable Unit Identifiers

Status: Accepted

## Context

NIST display labels are useful for people but can change when typography or OCR
errors are corrected. Using those labels as graph keys made a presentation edit
look like a breaking API change.

## Decision

- Persist opaque `unit_id` and `quantity_id` values in
  `data/registry/unit_registry.json`.
- Use `unit_id` values as nodes in the bundled conversion graph.
- Treat `display_name` as presentation text and retain reviewed former names in
  `aliases`.
- Keep display names valid as conversion inputs for compatibility.
- Copy the identity fields into the runtime unit catalog and keep the source
  registry out of the wheel to avoid duplicate package data.
- Preserve existing IDs during registry generation and fail when a data change
  would silently remove, merge, or split an identity.

## Consequences

Applications can store stable IDs without depending on display wording. New or
renamed units require an explicit registry update, and quantity graph changes
that affect identity fail generation until they are reviewed. Source
distributions retain the registry for maintainers; installed wheels need only
the composed unit catalog.
