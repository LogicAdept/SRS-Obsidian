$ErrorActionPreference = "Stop"

$image = "srs-cover-vault:local"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$dockerfile = Join-Path $PSScriptRoot "Dockerfile"
$isDryRun = $args -contains "--dry-run"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker Desktop is required. Install it, start the engine, and retry."
}

& docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Docker Desktop is installed but its engine is not running."
}

if (-not $isDryRun -and [string]::IsNullOrWhiteSpace($env:CURSOR_API_KEY)) {
    throw "Set CURSOR_API_KEY before a real run."
}

& docker build --tag $image --file $dockerfile $PSScriptRoot
if ($LASTEXITCODE -ne 0) {
    throw "Failed to build the isolated SRS coverage image."
}

$repoMount = "type=bind,source=$repo,target=/workspace"
$dockerArgs = @(
    "run",
    "--rm",
    "--init",
    "--read-only",
    "--network", "bridge",
    "--cap-drop", "ALL",
    "--security-opt", "no-new-privileges:true",
    "--pids-limit", "512",
    "--memory", "4g",
    "--cpus", "2",
    "--mount", $repoMount,
    "--tmpfs", "/tmp:rw,exec,nosuid,nodev,size=1073741824,uid=10001,gid=10001",
    "--tmpfs", "/home/agent:rw,exec,nosuid,nodev,size=536870912,uid=10001,gid=10001",
    "--env", "SRS_COVER_ISOLATED_CONTAINER=1"
)

if (-not [string]::IsNullOrWhiteSpace($env:CURSOR_API_KEY)) {
    $dockerArgs += @("--env", "CURSOR_API_KEY")
}

$dockerArgs += $image
$dockerArgs += $args

& docker @dockerArgs
exit $LASTEXITCODE
