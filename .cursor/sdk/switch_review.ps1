param(
    [switch]$Source,
    [switch]$Accept,
    [switch]$Drop,
    [Parameter(Position = 0)]
    [string]$Tag
)

$ErrorActionPreference = "Stop"

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$runsRoot = Join-Path $PSScriptRoot "runs"
$rebuild = Join-Path $PSScriptRoot "..\skills\process-topic\scripts\rebuild-coverage-index.py"

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

function Get-NormalizedPath([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path)) {
        return $null
    }
    $raw = $Path.Trim().Trim('"')
    if ($raw -match '^/([A-Za-z]):(/|\\)') {
        $raw = ($raw.Substring(1) -replace '/', '\')
    }
    try {
        return [System.IO.Path]::GetFullPath($raw).TrimEnd('\').ToLowerInvariant()
    }
    catch {
        return $null
    }
}

function ConvertFrom-FolderUri([string]$Uri) {
    if ([string]::IsNullOrWhiteSpace($Uri)) {
        return $null
    }
    try {
        $parsed = [Uri]$Uri
        if ($parsed.IsAbsoluteUri -and $parsed.Scheme -ne "file") {
            return $null
        }
        return $parsed.LocalPath
    }
    catch {
        return $null
    }
}

function Test-CursorFolderOpen([string]$Path) {
    $want = Get-NormalizedPath $Path
    if ($null -eq $want) {
        return $false
    }
    $storage = Join-Path $env:APPDATA "Cursor\User\globalStorage\storage.json"
    if (Test-Path -LiteralPath $storage) {
        $json = Get-Content -LiteralPath $storage -Raw -Encoding UTF8 | ConvertFrom-Json
        $windows = @()
        if ($null -ne $json.windowsState.lastActiveWindow) {
            $windows += $json.windowsState.lastActiveWindow
        }
        if ($null -ne $json.windowsState.openedWindows) {
            $windows += @($json.windowsState.openedWindows)
        }
        foreach ($win in $windows) {
            if (-not $win.folder) {
                continue
            }
            $local = ConvertFrom-FolderUri ([string]$win.folder)
            $have = Get-NormalizedPath $local
            if ($null -ne $have -and $have -eq $want) {
                return $true
            }
        }
    }
    $leaf = Split-Path $Path -Leaf
    foreach ($proc in @(Get-Process -Name "Cursor" -ErrorAction SilentlyContinue)) {
        $title = $proc.MainWindowTitle
        if (-not $title) {
            continue
        }
        if ($title -like "*$leaf*") {
            return $true
        }
    }
    return $false
}

function Open-CursorFolder([string]$Path) {
    $cursor = Get-CursorCli
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    # Do not use cursor -r: it replaces the last active window (source or clone).
    if (Test-CursorFolderOpen $resolved) {
        & $cursor $resolved
    }
    else {
        & $cursor -n $resolved
    }
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
        throw "Cursor CLI failed with exit code $LASTEXITCODE."
    }
}

function Get-Python {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $cmd) {
        throw "python is required to rebuild the coverage index."
    }
    return $cmd.Source
}

function Update-ClonesIndex {
    $script = (Resolve-Path -LiteralPath $rebuild).Path
    & (Get-Python) $script --repo $repo --clones-js-only
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to refresh coverage-clones.js"
    }
}

function Rebuild-CloneIndex([string]$ClonePath) {
    $script = (Resolve-Path -LiteralPath $rebuild).Path
    Write-Host "Rebuilding coverage index in clone..."
    & (Get-Python) $script --repo $ClonePath
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to rebuild coverage index in $ClonePath"
    }
}

function Read-CloneTag([string]$ClonePath) {
    $meta = Join-Path $ClonePath "cover-target.json"
    if (Test-Path -LiteralPath $meta) {
        $data = Get-Content -LiteralPath $meta -Raw -Encoding UTF8 | ConvertFrom-Json
        $value = [string]$data.tag
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return $value.TrimStart("#")
        }
    }
    $log = Join-Path $ClonePath "cover-run.log"
    if (Test-Path -LiteralPath $log) {
        foreach ($line in Get-Content -LiteralPath $log -Encoding UTF8) {
            if ($line -match '^=== #([A-Za-z0-9]+(?:/[A-Za-z0-9]+)*) pass') {
                return $Matches[1]
            }
        }
        foreach ($line in Get-Content -LiteralPath $log -Encoding UTF8) {
            if ($line -match '#([A-Za-z0-9]+(?:/[A-Za-z0-9]+)*) direct=') {
                return $Matches[1]
            }
        }
    }
    return $null
}

function Get-CloneForTag([string]$Wanted) {
    if (-not (Test-Path -LiteralPath $runsRoot)) {
        return $null
    }
    $want = $Wanted.TrimStart("#")
    $foundClones = Get-ChildItem -LiteralPath $runsRoot -Directory -ErrorAction SilentlyContinue |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName ".git") } |
        ForEach-Object {
            $found = Read-CloneTag $_.FullName
            if ($found -eq $want) { $_ }
        }
    return $foundClones | Sort-Object LastWriteTime -Descending | Select-Object -First 1
}

function Remove-Clone([string]$ClonePath, [string]$RunName) {
    docker rm -f "srs-cover-$RunName" 2>$null | Out-Null
    if (Test-Path -LiteralPath $ClonePath) {
        Remove-Item -LiteralPath $ClonePath -Recurse -Force
    }
    Update-ClonesIndex
}

function Accept-Clone([string]$ClonePath, [string]$CoverTag) {
    $dirty = @(& git -C $repo status --porcelain)
    if ($LASTEXITCODE -ne 0) {
        throw "Cannot read the source repository state."
    }
    if ($dirty.Count -ne 0) {
        throw "The source repository must be clean before -Accept."
    }
    $cloneDirty = @(& git -C $ClonePath status --porcelain)
    if ($cloneDirty.Count -ne 0) {
        & git -C $ClonePath add -A
        if ($LASTEXITCODE -ne 0) {
            throw "git add in the clone failed."
        }
        & git -C $ClonePath commit -m "Cover $CoverTag"
        if ($LASTEXITCODE -ne 0) {
            throw "git commit in the clone failed."
        }
    }
    $branch = (& git -C $ClonePath branch --show-current).Trim()
    if (-not $branch.StartsWith("agent/cover-")) {
        throw "Clone is not on an agent/cover-* branch."
    }
    & git -C $repo fetch $ClonePath $branch
    if ($LASTEXITCODE -ne 0) {
        throw "git fetch from the clone failed."
    }
    $fetched = (& git -C $repo rev-parse FETCH_HEAD).Trim()
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & git -C $repo merge-base --is-ancestor $fetched HEAD
    $owned = ($LASTEXITCODE -eq 0)
    $ErrorActionPreference = $prev
    if (-not $owned) {
        & git -C $repo cherry-pick FETCH_HEAD
        if ($LASTEXITCODE -ne 0) {
            throw "cherry-pick failed; clone kept at $ClonePath"
        }
    }
}

if ($Accept -and $Drop) {
    throw "Use either -Accept or -Drop, not both."
}
if ($Source -and ($Accept -or $Drop)) {
    throw "-Source cannot be combined with -Accept or -Drop."
}

if ($Source) {
    Write-Host "Source vault: $repo"
    Open-CursorFolder $repo
    exit 0
}

if ([string]::IsNullOrWhiteSpace($Tag)) {
    throw "Pass the tag: ./.cursor/sdk/switch_review.ps1 Java/Spring/Transactions"
}

$Tag = $Tag.TrimStart("#")
$clone = Get-CloneForTag $Tag
if ($null -eq $clone) {
    throw "No agent clone for #$Tag under $runsRoot"
}

if ($Drop) {
    Write-Host "Dropping clone for #$Tag : $($clone.FullName)"
    Remove-Clone $clone.FullName $clone.Name
    Open-CursorFolder $repo
    exit 0
}

if ($Accept) {
    Write-Host "Accepting clone for #$Tag : $($clone.FullName)"
    Accept-Clone $clone.FullName $Tag
    Remove-Clone $clone.FullName $clone.Name
    Open-CursorFolder $repo
    exit 0
}

Write-Host "Review clone for #$Tag : $($clone.FullName)"
Rebuild-CloneIndex $clone.FullName
Open-CursorFolder $clone.FullName
exit 0
