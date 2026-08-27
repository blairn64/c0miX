# Development

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The application listens on Flask's default development port. Set `COMIX_DB` to choose another SQLite database path.

## Tests

```bash
pytest -q
```

## API smoke test

Create a series:

```bash
curl -X POST http://127.0.0.1:5000/series \
  -H 'Content-Type: application/json' \
  -d '{"name":"Demo Series","publisher":"Example Comics"}'
```

Inspect the collection summary:

```bash
curl http://127.0.0.1:5000/api/series
```

## Docker

```bash
docker build -t comix .
docker run --rm -p 5000:5000 comix
```

The database is intentionally kept outside source control. For persistent container use, mount `/app/data` to a host volume.
