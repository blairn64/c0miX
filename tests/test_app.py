import os
import tempfile

import pytest

from app import app, get_db, init_db


@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    old_db = app.config.get("TEST_DB")
    app.config["TESTING"] = True
    import app as app_module
    original = app_module.DB_PATH
    app_module.DB_PATH = path
    init_db()
    with app.test_client() as test_client:
        yield test_client
    app_module.DB_PATH = original
    if old_db is not None:
        app.config["TEST_DB"] = old_db
    os.unlink(path)


def test_create_series_and_list(client):
    response = client.post("/series", json={"name": "Example Series", "publisher": "Example Comics"})
    assert response.status_code == 201

    response = client.get("/api/series")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload[0]["name"] == "Example Series"
    assert payload[0]["issue_count"] == 0


def test_missing_issue_excludes_reprints(client):
    series = client.post("/series", json={"name": "Run Test"}).get_json()
    series_id = series["id"]
    client.post(f"/series/{series_id}/issues", json={"issue_number": 1, "title": "First"})
    client.post(f"/series/{series_id}/issues", json={"issue_number": 2, "title": "Reprint", "is_reprint": True})

    response = client.get(f"/api/series/{series_id}/missing")
    assert response.status_code == 200
    missing = response.get_json()
    assert [item["issue_number"] for item in missing] == [1]
