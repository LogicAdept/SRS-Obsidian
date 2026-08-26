$ErrorActionPreference = "Stop"

# Disposable clone + Cursor window for chat /fill-tag (no SDK, no Docker agent).
# Source vault stays untouched until switch_review -Accept.

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$runsRoot = Join-Path $PSScriptRoot "runs"
$resumeWorkspace = $null
$positionalTag = $null
$openOnly = $false

for ($i = 0; $i -lt $args.Count; $i++) {
    $arg = [string]$args[$i]
    if ($arg -eq "--workspace") {
        if ($i + 1 -ge $args.Count) {
            throw "--workspace requires a run directory."
        }
        $i++
        $resumeWorkspace = [string]$args[$i]
        continue
    }
    if ($arg -eq "--open-only") {
        $openOnly = $true
        continue
    }
    if (-not $arg.StartsWith("-") -and $null -eq $positionalTag -and $arg -ne "--") {
        $positionalTag = $arg.TrimStart("#")
        continue
    }
    throw "Unknown argument: $arg"
}

if ([string]::IsNullOrWhiteSpace($positionalTag)) {
    throw "Choose a tag first: ./.cursor/sdk/open_chat_sandbox.ps1 Networking/OSI"
}

function Get-CursorCli {
    $cmd = Get-Command cursor -ErrorAction SilentlyContinue
    if ($null -ne $cmd) {
        return $cmd.Source
    }
    $fallback = Join-Path $env:LOCALAPPDATA "Programs\cursor\resources\app\bin\cursor.cmd"
    if (Test-Path -LiteralPath $fallback) {
        return $fallback
    }
    throw "Cursor CLI not found. Install Cursor or add cursor.cmd to PATH."
}

function Open-CursorFolder([string]$Path) {
    $cursor = Get-CursorCli
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    & $cursor -n $resolved
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
        throw "Cursor CLI failed with exit code $LASTEXITCODE."
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is required to create an isolated disposable clone."
}

$dirty = @(& git -C $repo status --porcelain)
if ($LASTEXITCODE -ne 0) {
    throw "Cannot read the source repository state."
}
if ($dirty.Count -ne 0 -and $null -eq $resumeWorkspace) {
    throw "The source repository must be clean and committed before creating a chat sandbox."
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
}

$target = @{
    tag = $positionalTag
    id = $runName
    kind = "fill"
    mode = "chat"
}
$targetJson = ($target | ConvertTo-Json) + "`n"
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText(
    (Join-Path $runWorkspace "fill-target.json"),
    $targetJson,
    $utf8
)

$rebuild = Join-Path $PSScriptRoot "..\skills\process-topic\scripts\rebuild-coverage-index.py"
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $rebuild --repo $repo --clones-js-only
}

Write-Host "Chat sandbox (no SDK / no Docker agent)"
Write-Host "  Tag:       #$positionalTag"
Write-Host "  Branch:    $agentBranch"
Write-Host "  Workspace: $runWorkspace"
Write-Host ""
Write-Host "This isolates the *vault copy*. Cursor still runs on this machine;"
Write-Host "shell auto-run can reach outside the clone. For hard isolation use a VM."
Write-Host ""
Write-Host "In the new Cursor window, Agent chat (Local, Auto/Composer is fine):"
Write-Host "  /fill-tag $positionalTag --limit 1"
Write-Host "Repeat until the tag batch is done. Accuracy over speed."
Write-Host ""
Write-Host "Bring changes into the source vault:"
Write-Host "  ./.cursor/sdk/switch_review.ps1 -Kind Fill -Accept $positionalTag"
Write-Host "Discard:"
Write-Host "  ./.cursor/sdk/switch_review.ps1 -Kind Fill -Drop $positionalTag"
Write-Host "Back to source:"
Write-Host "  ./.cursor/sdk/switch_review.ps1 -Source"
Write-Host ""
Write-Host "Optional GitHub PR from the clone instead of local Accept:"
Write-Host "  git -C `"$runWorkspace`" push -u origin HEAD"
Write-Host "  (then open a PR to main on LogicAdept/SRS-Obsidian)"

if (-not $openOnly) {
    Open-CursorFolder $runWorkspace
}

exit 0
