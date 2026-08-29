import os
import re
import secrets
import threading
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, field_validator

ENTRY_PATTERN = re.compile(r"^\d{4}/\d{2}/\d{2} (RUN|BWT|BIKE) mode, .+")
REQUEST_ID_PATTERN = r"^[A-Za-z0-9_.:-]{1,128}$"
_write_lock = threading.Lock()


class UpdateRequest(BaseModel):
    entry: str = Field(min_length=1, max_length=2000)
    request_id: str | None = Field(default=None, pattern=REQUEST_ID_PATTERN)

    @field_validator("entry")
    @classmethod
    def normalize_entry(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not ENTRY_PATTERN.fullmatch(normalized):
            raise ValueError(
                "entry must start with YYYY/MM/DD followed by RUN, BWT, or BIKE mode"
            )
        try:
            datetime.strptime(normalized[:10], "%Y/%m/%d")
        except ValueError as exc:
            raise ValueError("entry must start with a valid calendar date") from exc
        return normalized


class UpdateResponse(BaseModel):
    status: str
    appended: bool
    entry: str


def _configured_log_path() -> Path:
    configured = os.getenv("OKEEGSAN_DAILY_LOG_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path(__file__).resolve().parent / "data" / "daily_log.md").resolve()


def _authenticate(authorization: str | None, api_token: str | None) -> None:
    if not api_token:
        raise HTTPException(status_code=503, detail="Helper API token is not configured.")
    scheme, separator, supplied = (authorization or "").partition(" ")
    if (
        separator != " "
        or scheme.lower() != "bearer"
        or not secrets.compare_digest(supplied, api_token)
    ):
        raise HTTPException(status_code=401, detail="Invalid or missing bearer token.")


def _append_entry(log_path: Path, entry: str, request_id: str | None) -> bool:
    request_log = log_path.with_suffix(log_path.suffix + ".requests")
    with _write_lock:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        if request_id and request_log.exists():
            completed_ids = set(request_log.read_text(encoding="utf-8").splitlines())
            if request_id in completed_ids:
                return False
        if not log_path.exists():
            log_path.write_text("# O'KeegSan Daily Log\n\n", encoding="utf-8")
        with log_path.open("a", encoding="utf-8", newline="\n") as daily_log:
            daily_log.write(f"- {entry}\n")
            daily_log.flush()
            os.fsync(daily_log.fileno())
        if request_id:
            with request_log.open("a", encoding="utf-8", newline="\n") as requests:
                requests.write(f"{request_id}\n")
        return True


def create_app(*, log_path: Path | None = None, api_token: str | None = None) -> FastAPI:
    resolved_log_path = (log_path or _configured_log_path()).resolve()
    resolved_api_token = api_token if api_token is not None else os.getenv("OKEEGSAN_API_TOKEN")
    service = FastAPI(
        title="O'KeegSan Helper",
        version="0.1.0",
        description="Authenticated append-only activity summary service.",
    )

    @service.get("/healthz")
    @service.get("/okeegsan/healthz")
    def healthz() -> dict[str, str | bool]:
        return {"status": "ok", "write_configured": bool(resolved_api_token)}

    @service.post("/update", response_model=UpdateResponse)
    @service.post("/okeegsan/update", response_model=UpdateResponse)
    def update(payload: UpdateRequest, authorization: str | None = Header(default=None)) -> UpdateResponse:
        _authenticate(authorization, resolved_api_token)
        appended = _append_entry(resolved_log_path, payload.entry, payload.request_id)
        return UpdateResponse(
            status="saved" if appended else "already_saved",
            appended=appended,
            entry=payload.entry,
        )

    return service


app = create_app()