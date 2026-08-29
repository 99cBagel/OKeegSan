from pathlib import Path

from fastapi.testclient import TestClient

from app import create_app

TOKEN = "test-token"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
ENTRY = (
    "2026/08/30 RUN mode, goal 20 minutes, actual 15 minutes "
    "(07:32 AM - 07:47 AM), chat topics not recorded"
)


def make_client(tmp_path: Path) -> tuple[TestClient, Path]:
    log_path = tmp_path / "daily_log.md"
    return TestClient(create_app(log_path=log_path, api_token=TOKEN)), log_path


def test_health_does_not_expose_secrets_or_paths(tmp_path: Path) -> None:
    client, _ = make_client(tmp_path)
    response = client.get("/okeegsan/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "write_configured": True}


def test_update_requires_bearer_token(tmp_path: Path) -> None:
    client, log_path = make_client(tmp_path)
    response = client.post("/okeegsan/update", json={"entry": ENTRY})
    assert response.status_code == 401
    assert not log_path.exists()


def test_update_appends_normalized_one_line_entry(tmp_path: Path) -> None:
    client, log_path = make_client(tmp_path)
    spoken_entry = ENTRY.replace(", actual", ",\nactual")
    response = client.post(
        "/okeegsan/update",
        headers=HEADERS,
        json={"entry": spoken_entry, "request_id": "run-20260830-0732"},
    )
    assert response.status_code == 200
    assert response.json()["appended"] is True
    assert log_path.read_text(encoding="utf-8") == f"# O'KeegSan Daily Log\n\n- {ENTRY}\n"


def test_request_id_makes_retry_idempotent(tmp_path: Path) -> None:
    client, log_path = make_client(tmp_path)
    payload = {"entry": ENTRY, "request_id": "run-20260830-0732"}
    first = client.post("/update", headers=HEADERS, json=payload)
    retry = client.post("/update", headers=HEADERS, json=payload)
    assert first.json()["appended"] is True
    assert retry.json() == {
        "status": "already_saved",
        "appended": False,
        "entry": ENTRY,
    }
    assert log_path.read_text(encoding="utf-8").count(ENTRY) == 1


def test_update_rejects_unstructured_entry(tmp_path: Path) -> None:
    client, _ = make_client(tmp_path)
    response = client.post(
        "/update", headers=HEADERS, json={"entry": "Had a good run."}
    )
    assert response.status_code == 422

def test_update_rejects_invalid_calendar_date(tmp_path: Path) -> None:
    client, _ = make_client(tmp_path)
    response = client.post(
        "/update",
        headers=HEADERS,
        json={"entry": "2026/02/30 RUN mode, goal not recorded, actual not recorded"},
    )
    assert response.status_code == 422