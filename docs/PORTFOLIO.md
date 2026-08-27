# Portfolio Notes

## What this project says about my engineering

I built c0miX to solve a real modelling problem: a comic collection is not just a list of issues. Publication order, variants and reprints need to be represented separately from whether a particular copy is owned or read.

That led to a small Flask application with a relational SQLite model, server-rendered pages and JSON endpoints. The repository also includes tests, a container build and engineering notes.

## Engineering decisions worth discussing

### Domain model
Canonical issue identity is kept separate from collection state. This means buying, reading or selling a copy does not mutate the publication record.

### API boundary
The JSON endpoints expose collection summaries and missing-issue calculations without requiring a separate frontend stack. This keeps the project simple while leaving room for a future client or CLI.

### Test isolation
Tests use a temporary SQLite database so they do not depend on a developer's local data. Core behaviour is tested through Flask's HTTP test client.

### Containerisation
The Docker image uses a non-root application account and a health check. SQLite data is stored under `/app/data` and is intentionally excluded from source control.

## What I would improve next

- Move from `app.py` to a package layout as the application grows.
- Add a migration tool instead of creating tables at request time.
- Expand the domain model for richer variant relationships.
- Add pagination/search and import validation.
- Add CI checks for formatting and dependency/security scanning.
