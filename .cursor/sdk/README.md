# Cover vault

You pick a tag. Docker runs `/refine-tags` and `/cover-tag` on that leaf, or on
the leaves under that parent — never on parent nodes or ancestors. The source
vault is untouched until you accept the clone.

## Run from the HTML tree

In a shell with a clean repo:

```powershell
$env:CURSOR_API_KEY = "cursor_..."
python .cursor/sdk/cover_ui.py
```

Open `SRS/NamesHistory/coverage-index.html` and click **Agent** on a tag.
If the helper is not running, the button copies:

```powershell
./.cursor/sdk/run_cover_vault.ps1 Java/Language/Primitives/ShortType
```

Watch the log if you want:

```powershell
Get-Content .cursor/sdk/runs/<id>/cover-run.log -Wait
```

`--wait` keeps the launcher attached.

## Review

```powershell
$run = "C:\Users\V\ObsidianVaults\SRS\.cursor\sdk\runs\<id>"
git -C $run status --short
git -C $run diff
```

Reject:

```powershell
Remove-Item -LiteralPath $run -Recurse -Force
```

Accept: commit in the clone, then fetch/cherry-pick `agent/cover-<id>`.

## Defaults

`grok-4.6` high, `--cover-limit 50` (cap, not a target), `--max-passes-per-tag 5`.
A real run requires a chosen tag. Cover is leaf-only: a leaf is covered by itself;
a parent covers its descendant leaves only. Hitting the 50-card cap marks
`review_required`; continue with `--continue-tag`.
