# ChatGPT to O'KeegSan MCP example

This example gives ChatGPT one write-capable MCP tool:
`save_activity_summary(entry, request_id)`. The tool sends an approved summary
to the existing FastAPI helper, which validates and appends it to
`daily_log.md`.

## What works on iPhone

Ordinary ChatGPT Voice on iPhone cannot currently invoke apps or MCP tools.
Therefore, saying "Save O'KeegSan" in ordinary Voice can prepare and confirm the
summary, but it cannot directly call this MCP server.

Use this practical handoff:

1. In Voice, say "Open O'KeegSan", choose a mode, and complete the activity.
2. Say "Close O'KeegSan".
3. Say "Save O'KeegSan" and approve the exact proposed one-line summary.
4. Leave Voice and send this text message in the same chat:
   "Use the O'KeegSan app to save the approved summary."
5. ChatGPT calls `save_activity_summary`; the MCP bridge calls the local helper;
   the helper appends the line and returns `ok` or `already_saved`.

A supported desktop Work or Codex voice host may make the tool call during the
voice session. The repository prompt must still require explicit approval before
every save.

## Data flow

```text
iPhone ChatGPT conversation
        |
        | approved entry + request_id
        v
ChatGPT O'KeegSan MCP app
        |
        | Streamable HTTP MCP
        v
mcp_server.py on 127.0.0.1:8083/mcp
        |
        | Bearer token, stored only in HomeLab .env
        v
FastAPI helper on 127.0.0.1:8082/okeegsan/update
        |
        v
daily_log.md
```

The MCP bridge is loopback-only. For private development, connect ChatGPT with
OpenAI's Secure MCP Tunnel rather than publishing an unauthenticated,
write-capable MCP endpoint.

## Install and run

From `OKeegSan_helper`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-mcp.txt
powershell -ExecutionPolicy Bypass -File .\start_mcp.ps1
```

The example MCP endpoint is `http://127.0.0.1:8083/mcp`. The existing helper
must also be running on port 8082, with the same private `.env` providing
`OKEEGSAN_API_TOKEN`.

## Connect through Secure MCP Tunnel

Install and initialize OpenAI's `tunnel-client`, then use placeholders supplied
by the OpenAI platform:

```powershell
$env:CONTROL_PLANE_API_KEY = "<runtime-api-key>"
tunnel-client init --profile okeegsan --tunnel-id "<tunnel-id>" --mcp-server-url "http://127.0.0.1:8083/mcp"
tunnel-client doctor --profile okeegsan
tunnel-client run --profile okeegsan
```

In ChatGPT developer mode, create an app using **Tunnel**, then select that
tunnel ID. Do not commit the runtime API key, helper bearer token, or generated
tunnel credentials.

For a publicly distributed app, replace this private-development arrangement
with a stable HTTPS MCP endpoint and the OAuth requirements described in the
OpenAI authentication documentation.

## Tool contract

Example approved arguments:

```json
{
  "entry": "2026/08/29 RUN mode, goal 15 minutes, actual not recorded, chat topics not recorded",
  "request_id": "voice-20260829-run"
}
```

Use a unique, stable `request_id` for the activity. Retrying the same request
returns `already_saved` instead of appending a duplicate. Never send a draft
until the user has approved its exact wording.
