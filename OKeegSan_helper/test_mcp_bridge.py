import asyncio
import httpx
import pytest
from mcp_bridge import HelperBridgeError, save_via_helper

def test_save_via_helper_posts_authenticated_normalized_entry():
    seen = {}
    def handler(request: httpx.Request) -> httpx.Response:
        seen["authorization"] = request.headers["Authorization"]
        seen["body"] = request.content
        return httpx.Response(200, json={"status": "ok", "appended": True, "entry": "2026/08/29 RUN mode, goal 15 minutes, actual not recorded"})
    result = asyncio.run(save_via_helper("  2026/08/29 RUN mode, goal 15 minutes, actual not recorded  ", "voice-20260829-run", helper_url="http://helper.test/okeegsan/update", api_token="test-token", transport=httpx.MockTransport(handler)))
    assert seen["authorization"] == "Bearer test-token"
    assert b'"request_id":"voice-20260829-run"' in seen["body"]
    assert result["appended"] is True

def test_save_via_helper_requires_server_side_token():
    with pytest.raises(HelperBridgeError, match="not configured"):
        asyncio.run(save_via_helper("2026/08/29 BWT mode, goal not recorded, actual not recorded", "voice-20260829-bwt", api_token=""))

def test_save_via_helper_reports_rejection_without_response_details():
    transport = httpx.MockTransport(lambda request: httpx.Response(401, text="secret detail"))
    with pytest.raises(HelperBridgeError, match=r"rejected the save \(401\)") as exc_info:
        asyncio.run(save_via_helper("2026/08/29 BIKE mode, goal not recorded, actual not recorded", "voice-20260829-bike", api_token="test-token", transport=transport))
    assert "secret detail" not in str(exc_info.value)
