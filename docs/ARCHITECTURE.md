# Architecture

## Domain model

The application treats a comic run as a canonical sequence of issues rather than as a flat list of inventory records. This allows ownership, reading progress and gaps to be tracked independently from variant or reprint metadata.

## Suggested boundaries

- **Ingestion** — imports source data and normalises fields.
- **Domain** — determines canonical ordering, run membership and gap state.
- **Persistence** — stores series, issues, variants and user state.
- **API/UI** — exposes search, run progress and collection views.

## Core workflow

```text
Source data
   ↓
Normalization
   ↓
Canonical issue model
   ↓
Run calculation
   ├── owned
   ├── read
   └── missing
   ↓
API / interface
```

## Design principles

1. Keep source-specific identifiers separate from canonical issue identifiers.
2. Do not treat variants and reprints as separate canonical issues unless the user explicitly chooses to do so.
3. Store user state independently from imported metadata so source refreshes do not overwrite collection history.
4. Keep data import repeatable and deterministic.

## Testing priorities

The most important tests are ordering, duplicate detection, run membership, gap calculation and preservation of user state during re-imports.
