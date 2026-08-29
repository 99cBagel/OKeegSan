# O'KeegSan Helper

Small FastAPI service for appending approved activity summaries to a HomeLab
`daily_log.md`. It follows the same FastAPI/Uvicorn and PowerShell launch pattern
as the existing `D:\Qwen-Paddle\docuk.ps1` services.

## API

- `GET /healthz` or `GET /okeegsan/healthz`: liveness and write-configuration
  status; does not expose the token or filesystem path.
- `POST /update` or `POST /okeegsan/update`: append one approved activity summary.

Example request:

```powershell
$headers = @{ Authorization = "Bearer $env:OKEEGSAN_API_TOKEN" }
$body = @{
    entry = "2026/08/30 RUN mode, goal 20 minutes, actual 15 minutes (07:32 AM - 07:47 AM), chat topics not recorded"
    request_id = "run-20260830-0732"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "https://lenovo.keeg.uk/okeegsan/update" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $body
```

The API requires a line beginning with `YYYY/MM/DD RUN mode`, `BWT mode`, or
`BIKE mode`. Newlines and repeated whitespace are collapsed. A repeated
`request_id` returns `already_saved` without appending the entry again.

## Local setup

```powershell
cd OKeegSan_helper
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Replace the token in `.env` with a long random value and choose a runtime data
path. Do not commit `.env`, the token, `daily_log.md`, or its request-ID journal.

Start with `powershell -ExecutionPolicy Bypass -File .\start.ps1`. The default
listener is private on `127.0.0.1:8082`; expose it only through the HTTPS tunnel.

Run tests with:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Cloudflare Tunnel routing

The HomeLab runs a remotely managed tunnel, so configure this route in the
Cloudflare dashboard rather than creating a local YAML file:

1. Go to **Networking > Tunnels** and open the tunnel used by `lenovo.keeg.uk`.
2. Under **Routes**, add a **Published application** route.
3. Use hostname `lenovo.keeg.uk`, path `/okeegsan/.*`, and service URL
   `http://127.0.0.1:8082`.
4. Keep the existing `lenovo.keeg.uk` catch-all route to `http://127.0.0.1:8080`
   after the new path-specific route.
5. Verify `https://lenovo.keeg.uk/okeegsan/healthz` before enabling callers.

Keep the bearer token in the calling tool's secret store. Never put it in an
audio prompt, activity log, repository file, or URL query string.
## Existing launcher integration

Start this helper as another hidden child process from `docuk.ps1`, just as it
starts the private Paddle worker. Point it at the deployed helper folder and run
`.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8082
--env-file .env`. Verify the process remains running and stop it in the launcher's
`finally` block.

Before editing the live launcher, confirm the deployed helper path and active
Cloudflare Tunnel configuration on the HomeLab machine.
## ChatGPT MCP bridge example

The optional MCP bridge exposes one tool, `save_activity_summary`, and forwards
approved entries to this helper without exposing its bearer token to the phone
or model. Install `requirements-mcp.txt`, then run `start_mcp.ps1`; it serves
Streamable HTTP MCP at `http://127.0.0.1:8083/mcp`.

See [the iPhone and MCP workflow](../docs/iphone-mcp-workflow.md) for the data
flow, Secure MCP Tunnel setup, and the current ordinary-Voice limitation.
