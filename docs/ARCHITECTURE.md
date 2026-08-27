# c0miX architecture

## Purpose

c0miX is a small full-stack Flask application for modelling comic series and issues while keeping canonical issue data separate from personal collection state.

## Application layers

```text
Browser / API client
        |
        v
     Flask app
   /      |      \
 views   JSON API  validation
   |       |         |
   +-------+---------+
           |
           v
        SQLite
```

## Domain model

- **Series** stores canonical series identity and high-level metadata.
- **Issues** belong to a series and store issue number, title, cover date and variant information.
- **Collection** stores personal state such as ownership, reading status and notes.

Keeping collection state separate means canonical issue metadata does not change simply because a copy is bought, read or sold.

## API surface

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/series` | Return series and collection summary |
| GET | `/api/series/<id>/missing` | Find unowned canonical issues |
| POST | `/series` | Add a series |
| POST | `/series/<id>/issues` | Add an issue |
| POST | `/issues/<id>/collection` | Update ownership/read state |

## Design choices

SQLite keeps the project easy to run locally and makes the data model visible. Flask keeps the HTTP layer small and explicit. JSON endpoints are separate from HTML views so the same data model can support a future CLI or frontend.

## Future direction

Potential next steps are external data import, richer variant modelling, pagination/search, migration tooling and automated tests around issue ordering, duplicate detection and missing-run calculations.
