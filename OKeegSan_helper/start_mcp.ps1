$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) { throw "Missing .venv. Create it and install requirements-mcp.txt first." }
& $python -c "import mcp" 2>$null
if ($LASTEXITCODE -ne 0) { throw "Missing MCP SDK. Run: .\.venv\Scripts\python.exe -m pip install -r requirements-mcp.txt" }
Push-Location $root
try { & $python -m uvicorn mcp_server:app --host 127.0.0.1 --port 8083 --env-file .env } finally { Pop-Location }
