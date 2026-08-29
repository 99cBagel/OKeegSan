"""HTTP bridge from the O'KeegSan MCP tool to the append-only helper."""
from __future__ import annotations
import os
from typing import Any
import httpx
from app import UpdateRequest

DEFAULT_HELPER_URL = "http://127.0.0.1:8082/okeegsan/update"

class HelperBridgeError(RuntimeError):
    """A safe, user-facing error raised when the helper cannot save a log."""

async def save_via_helper(entry: str, request_id: str, *, helper_url: str | None = None, api_token: str | None = None, transport: httpx.AsyncBaseTransport | None = None) -> dict[str, Any]:
    """Validate an entry locally, then append it through OKeegSan_helper."""
    request = UpdateRequest(entry=entry, request_id=request_id)
    token = api_token if api_token is not None else os.getenv("OKEEGSAN_API_TOKEN", "")
    if not token:
        raise HelperBridgeError("OKEEGSAN_API_TOKEN is not configured on the MCP host")
    url = helper_url or os.getenv("OKEEGSAN_HELPER_URL", DEFAULT_HELPER_URL)
    try:
        async with httpx.AsyncClient(transport=transport, timeout=10) as client:
            response = await client.post(url, headers={"Authorization": f"Bearer {token}"}, json=request.model_dump())
    except httpx.RequestError as exc:
        raise HelperBridgeError("O'KeegSan helper is unavailable") from exc
    if not response.is_success:
        raise HelperBridgeError(f"O'KeegSan helper rejected the save ({response.status_code})")
    try:
        result = response.json()
    except ValueError as exc:
        raise HelperBridgeError("O'KeegSan helper returned an invalid response") from exc
    return {"status": result.get("status", "ok"), "appended": bool(result.get("appended")), "entry": result.get("entry", request.entry)}
