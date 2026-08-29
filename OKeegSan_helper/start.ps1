$ErrorActionPreference = "Stop"

$serviceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $serviceRoot ".venv\Scripts\python.exe"
$envFile = Join-Path $serviceRoot ".env"
$hostAddress = if ($env:OKEEGSAN_HELPER_HOST) { $env:OKEEGSAN_HELPER_HOST } else { "127.0.0.1" }
$port = if ($env:OKEEGSAN_HELPER_PORT) { $env:OKEEGSAN_HELPER_PORT } else { "8082" }

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "Virtual environment not found at $python."
}
if (-not (Test-Path -LiteralPath $envFile -PathType Leaf)) {
    throw "Environment file not found at $envFile. Copy .env.example to .env and set a token."
}

Set-Location $serviceRoot
& $python -m uvicorn app:app --host $hostAddress --port $port --env-file $envFile