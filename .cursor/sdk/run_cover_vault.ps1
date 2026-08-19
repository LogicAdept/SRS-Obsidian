$ErrorActionPreference = "Stop"

$image = "srs-cover-vault:local"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$dockerfile = Join-Path $PSScriptRoot "Dockerfile"
$runsRoot = Join-Path $PSScriptRoot "runs"
$resumeWorkspace = $null
$wait = $false
$forwardArgs = [System.Collections.Generic.List[string]]::new()
$positionalTag = $null

for ($i = 0; $i -lt $args.Count; $i++) {
    $arg = $args[$i]
    if ($arg -eq "--workspace") {
        if ($i + 1 -ge $args.Count) {
            throw "--workspace requires a run directory."
        }
        $i++
        $resumeWorkspace = $args[$i]
        continue
    }
    if ($arg -eq "--wait") {
        $wait = $true
        continue
    }
    if (-not $arg.StartsWith("-") -and $null -eq $positionalTag -and $arg -ne "--") {
        $positionalTag = $arg.TrimStart("#")
        continue
    }
    $forwardArgs.Add($arg)
}

if ($null -ne $positionalTag) {
    $forwardArgs.Add("--only")
    $forwardArgs.Add($positionalTag)
}

$isDryRun = $forwardArgs.Contains("--dry-run")
$hasOnly = $forwardArgs.Contains("--only")
$hasContinue = $forwardArgs.Contains("--continue-tag")
if (-not $isDryRun -and -not $hasOnly -and -not $hasContinue) {
    throw "Choose a tag: ./.cursor/sdk/run_cover_vault.ps1 Java/Language/Primitives/ShortType"
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker Desktop is required. Install it, start the engine, and retry."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is required to create an isolated disposable clone."
}

& docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Docker Desktop is installed but its engine is not running."
}

if (-not $isDryRun -and [string]::IsNullOrWhiteSpace($env:CURSOR_API_KEY)) {
    throw "Set CURSOR_API_KEY before a real run."
}

$dirty = @(& git -C $repo status --porcelain)
if ($LASTEXITCODE -ne 0) {
    throw "Cannot read the source repository state."
}
if ($dirty.Count -ne 0) {
    throw "The source repository must be clean and committed before creating or resuming an agent run."
}

& docker build --tag $image --file $dockerfile $PSScriptRoot
if ($LASTEXITCODE -ne 0) {
    throw "Failed to build the isolated SRS coverage image."
}

New-Item -ItemType Directory -Force -Path $runsRoot | Out-Null
$runsRoot = (Resolve-Path $runsRoot).Path

if ($null -eq $resumeWorkspace) {
    $sourceBranch = (& git -C $repo branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($sourceBranch)) {
        throw "The source repository must be on a named branch."
    }
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $suffix = [guid]::NewGuid().ToString("N").Substring(0, 8)
    $runName = "$stamp-$suffix"
    $runWorkspace = Join-Path $runsRoot $runName
    $agentBranch = "agent/cover-$runName"

    & git clone --no-local --no-hardlinks --single-branch --branch $sourceBranch $repo $runWorkspace
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create the disposable repository clone."
    }
    & git -C $runWorkspace switch -c $agentBranch
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create the isolated agent branch."
    }
}
else {
    $runWorkspace = (Resolve-Path $resumeWorkspace).Path
    $runsPrefix = $runsRoot.TrimEnd("\") + "\"
    if (-not $runWorkspace.StartsWith(
        $runsPrefix,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw "--workspace must point inside $runsRoot"
    }
    if (-not (Test-Path (Join-Path $runWorkspace ".git"))) {
        throw "--workspace is not a disposable Git clone."
    }
    $agentBranch = (& git -C $runWorkspace branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $agentBranch.StartsWith("agent/cover-")) {
        throw "--workspace is not on an agent/cover-* branch."
    }
    $runName = Split-Path $runWorkspace -Leaf
}

Write-Host "Agent branch:    $agentBranch"
Write-Host "Agent workspace: $runWorkspace"

$containerName = "srs-cover-$runName"
$repoMount = "type=bind,source=$runWorkspace,target=/workspace"
$dockerArgs = @(
    "run",
    "--rm",
    "--name", $containerName,
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
$dockerArgs += $forwardArgs.ToArray()

function Write-ReviewHints {
    Write-Host ""
    Write-Host "The source vault is not modified."
    Write-Host "Log:"
    Write-Host "  Get-Content `"$logFile`" -Wait"
    Write-Host "Review:"
    Write-Host "  git -C `"$runWorkspace`" status --short"
    Write-Host "  git -C `"$runWorkspace`" diff"
    Write-Host "Reject:"
    Write-Host "  docker rm -f $containerName; Remove-Item -LiteralPath `"$runWorkspace`" -Recurse -Force"
    Write-Host "Accept after reviewing: commit in the clone, then fetch/cherry-pick $agentBranch."
}

$logFile = Join-Path $runWorkspace "cover-run.log"
if ($isDryRun -or $wait) {
    & docker @dockerArgs
    $containerExitCode = $LASTEXITCODE
    Write-ReviewHints
    exit $containerExitCode
}

$quoted = foreach ($item in $dockerArgs) {
    if ($item -match '[\s"]') {
        '"' + ($item -replace '"', '\"') + '"'
    }
    else {
        $item
    }
}
$command = "docker $($quoted -join ' ') > `"$logFile`" 2>&1"
Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $command -WindowStyle Hidden | Out-Null
Write-Host "Started in background as $containerName"
Write-ReviewHints
exit 0
