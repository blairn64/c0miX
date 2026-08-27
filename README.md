# c0miX — Comic Collection & Run Tracker

A Flask + SQLite application for organising comic series, canonical issue runs and personal collection state.

The useful problem here is not simply storing a list of comics. The application keeps **canonical publication data** separate from **personal ownership/reading state**, which makes reprints, variants and missing issues easier to reason about.

## What it demonstrates

- Python and Flask application development
- Relational data modelling with SQLite
- REST-style JSON endpoints
- Server-rendered HTML with Jinja templates
- Input validation and explicit error handling
- Testable application structure with pytest
- Containerisation with Docker
- Separation of canonical data from user state

## Architecture

```text
                    +------------------+
                    | Browser / API    |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | Flask application |
                    | views + JSON API  |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | SQLite data model |
                    +------------------+
                      /      |       \
                 series    issues   collection
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the data-model and API decisions.

## Current functionality

- Create comic series
- Add numbered issues
- Represent variants and reprints without changing the canonical issue number
- Track owned/read state
- Show collection summaries
- Query missing canonical issues through the API
- Browse series and runs through the web interface

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the local Flask address shown in the terminal.

Run the tests with:

```bash
pytest -q
```

Windows PowerShell setup is documented in [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md).

## Docker

```bash
docker build -t comix .
docker run --rm -p 5000:5000 comix
```

For persistent data, mount `/app/data` to a local volume. SQLite files are excluded from Git.

## Project direction

The next useful development steps are richer issue/run calculation, search and pagination, deterministic external-data imports, stronger validation and a more complete collection UI.

## Portfolio note

This is a personal software project. It contains no employer, customer or production infrastructure. Any external comic data used with the application should be sourced and redistributed according to its licence.
