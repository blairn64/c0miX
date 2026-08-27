# c0miX — Personal Comic Collection POC

A personal Flask + SQLite proof of concept for organising comic series, canonical issue runs and collection state.

This is intentionally a **personal POC**, not a commercial product. I keep it as a small end-to-end software example showing data modelling, web routes, JSON APIs, testing and containerisation.

## What it demonstrates

- Python and Flask application development
- Relational data modelling with SQLite
- Series, issues, variants and reprints
- HTML views and JSON API endpoints
- Input validation and explicit error handling
- Automated tests with pytest
- Docker-based local deployment
- Separation of canonical publication data from personal collection state

## Architecture

```text
Browser / API client
        |
        v
     Flask app
     /       \
 HTML views  JSON API
        |
        v
     SQLite
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/TESTING.md`](docs/TESTING.md).

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Run the tests with:

```bash
python -m pytest -q
```

## Docker

```bash
docker build -t comix .
docker run --rm -p 5000:5000 comix
```

Mount `/app/data` when persistent local SQLite storage is required.

## Portfolio position

This project is deliberately secondary to the infrastructure and automation work in my portfolio. It demonstrates software engineering breadth without pretending to be enterprise production software.
