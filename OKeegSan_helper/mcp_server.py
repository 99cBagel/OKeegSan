"""Example Streamable HTTP MCP server for the O'KeegSan helper."""
from __future__ import annotations
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from mcp_bridge import HelperBridgeError, save_via_helper

mcp = FastMCP("okeegsan-helper", instructions="Save only an explicitly approved O'KeegSan one-line activity summary. Never invent activity details.", stateless_http=True, json_response=True)

@mcp.tool(
    name="save_activity_summary",
    title="Save O'KeegSan activity summary",
    description="Append one user-approved RUN, BWT, or BIKE summary to daily_log.md. Reusing request_id makes retries idempotent.",
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=True),
)
async def save_activity_summary(entry: str, request_id: str) -> dict[str, object]:
    """Append an explicitly approved activity summary through the local helper."""
    try:
        return await save_via_helper(entry, request_id)
    except HelperBridgeError as exc:
        raise ValueError(str(exc)) from exc

app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
