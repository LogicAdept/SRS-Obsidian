$ErrorActionPreference = "Stop"

$image = "srs-fill-tag:local"
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

if ([string]::IsNullOrWhiteSpace($positionalTag)) {
    throw "Choose a tag first: ./.cursor/sdk/run_fill_tag.ps1 Java/Spring/Transactions --limit 10"
}

function Sync-AgentControlFiles([string]$Workspace) {
    $paths = @(
        ".cursor/sdk/fill_tag_loop.py",
        ".cursor/skills/fill-tag/SKILL.md",
        ".cursor/skills/process-topic/scripts/rebuild-coverage-index.py",
        ".cursor/skills/process-topic/scripts/vault_cards.py"
    )
    foreach ($relative in $paths) {
        $source = Join-Path $repo $relative
        if (-not (Test-Path -LiteralPath $source)) {
            throw "Missing agent control file: $relative"
        }
        $destination = Join-Path $Workspace $relative
        $parent = Split-Path $destination -Parent
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
        Copy-Item -LiteralPath $source -Destination $destination -Force
    }
}

$isDryRun = $forwardArgs.Contains("--dry-run")

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
    throw "Failed to build the isolated SRS fill image."
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
    $agentBranch = "agent/fill-$runName"

    & git clone --no-local --no-hardlinks --single-branch --branch $sourceBranch $repo $runWorkspace
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create the disposable repository clone."
    }
    & git -C $runWorkspace switch -c $agentBranch
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create the isolated fill branch."
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
    if ($LASTEXITCODE -ne 0 -or -not $agentBranch.StartsWith("agent/fill-")) {
        throw "--workspace is not on an agent/fill-* branch."
    }
    $runName = Split-Path $runWorkspace -Leaf
    Sync-AgentControlFiles $runWorkspace
}

Write-Host "Agent branch:    $agentBranch"
Write-Host "Agent workspace: $runWorkspace"

$target = @{
    tag = $positionalTag
    id = $runName
    kind = "fill"
}
$targetJson = ($target | ConvertTo-Json) + "`n"
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText(
    (Join-Path $runWorkspace "fill-target.json"),
    $targetJson,
    $utf8
)

$rebuild = Join-Path $PSScriptRoot "..\skills\process-topic\scripts\rebuild-coverage-index.py"
& python $rebuild --repo $repo --clones-js-only
if ($LASTEXITCODE -ne 0) {
    throw "Failed to refresh coverage-clones.js"
}

$containerName = "srs-fill-$runName"
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
    "--env", "SRS_FILL_ISOLATED_CONTAINER=1"
)

if (-not [string]::IsNullOrWhiteSpace($env:CURSOR_API_KEY)) {
    $dockerArgs += @("--env", "CURSOR_API_KEY")
}

$dockerArgs += @(
    "--entrypoint", "python",
    $image,
    "/workspace/.cursor/sdk/fill_tag_loop.py",
    $positionalTag
)
$dockerArgs += $forwardArgs.ToArray()

$logFile = Join-Path $runWorkspace "fill-run.log"

function Write-ReviewHints {
    Write-Host ""
    Write-Host "The source vault is not modified."
    Write-Host "Progress:"
    Write-Host "  Get-Content `"$logFile`" -Wait"
    Write-Host "  Get-Content `"$(Join-Path $runWorkspace 'fill-progress.json')`""
    Write-Host "Review this tag's clone:"
    Write-Host "  ./.cursor/sdk/switch_review.ps1 -Kind Fill $positionalTag"
    Write-Host "Accept (cherry-pick and delete clone):"
    Write-Host "  ./.cursor/sdk/switch_review.ps1 -Kind Fill -Accept $positionalTag"
    Write-Host "Drop clone without merging:"
    Write-Host "  ./.cursor/sdk/switch_review.ps1 -Kind Fill -Drop $positionalTag"
    Write-Host "Back to this vault:"
    Write-Host "  ./.cursor/sdk/switch_review.ps1 -Source"
    Write-Host "Stop and reject manually:"
    Write-Host "  docker rm -f $containerName; Remove-Item -LiteralPath `"$runWorkspace`" -Recurse -Force"
}

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
