$ErrorActionPreference = "Stop"

$image = "srs-cover-vault:local"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$dockerfile = Join-Path $PSScriptRoot "Dockerfile"
$runsRoot = Join-Path $PSScriptRoot "runs"
$resumeWorkspace = $null
$wait = $false
$forwardArgs = [System.Collections.Generic.List[string]]::new()
$positionalTag = $null
$focus = $null

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
    if ($arg -eq "--focus") {
        if ($i + 1 -ge $args.Count) {
            throw "--focus requires a description of the missing coverage."
        }
        $i++
        $focus = $args[$i].Trim()
        if ([string]::IsNullOrWhiteSpace($focus)) {
            throw "--focus cannot be empty."
        }
        $forwardArgs.Add("--focus")
        $forwardArgs.Add($focus)
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

function Get-RequestedTag {
    if (-not [string]::IsNullOrWhiteSpace($positionalTag)) {
        return $positionalTag.TrimStart("#")
    }
    for ($i = 0; $i -lt $forwardArgs.Count; $i++) {
        if (
            ($forwardArgs[$i] -eq "--only" -or $forwardArgs[$i] -eq "--continue-tag") -and
            ($i + 1 -lt $forwardArgs.Count)
        ) {
            return $forwardArgs[$i + 1].TrimStart("#")
        }
    }
    return $null
}

function Sync-AgentControlFiles([string]$Workspace) {
    $paths = @(
        ".cursor/sdk/fill_vault.py",
        ".cursor/skills/cover-tag/SKILL.md",
        ".cursor/skills/refine-tags/SKILL.md",
        ".cursor/skills/refine-tags/scripts/write-focus-target.py",
        ".cursor/skills/process-topic/scripts/rebuild-coverage-index.py"
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
    Sync-AgentControlFiles $runWorkspace
}

Write-Host "Agent branch:    $agentBranch"
Write-Host "Agent workspace: $runWorkspace"

$requestedTag = Get-RequestedTag
if (-not [string]::IsNullOrWhiteSpace($requestedTag)) {
    $target = @{ tag = $requestedTag; id = $runName }
    if (-not [string]::IsNullOrWhiteSpace($focus)) {
        $target.focus = $focus
    }
    $target | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runWorkspace "cover-target.json") -Encoding utf8
    $rebuild = Join-Path $PSScriptRoot "..\skills\process-topic\scripts\rebuild-coverage-index.py"
    & python $rebuild --repo $repo --clones-js-only
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to refresh coverage-clones.js"
    }
}

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
    if (-not [string]::IsNullOrWhiteSpace($requestedTag)) {
        Write-Host "Review that tag's clone:"
        Write-Host "  ./.cursor/sdk/switch_review.ps1 $requestedTag"
        Write-Host "Accept (cherry-pick, delete clone, hide Clone button):"
        Write-Host "  ./.cursor/sdk/switch_review.ps1 -Accept $requestedTag"
        Write-Host "Drop clone without merging:"
        Write-Host "  ./.cursor/sdk/switch_review.ps1 -Drop $requestedTag"
    }
    Write-Host "Back to this vault:"
    Write-Host "  ./.cursor/sdk/switch_review.ps1 -Source"
    Write-Host "Reject:"
    Write-Host "  docker rm -f $containerName; Remove-Item -LiteralPath `"$runWorkspace`" -Recurse -Force"
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
