# Agent sandboxes

## Chat fill (no SDK)

Disposable clone + a second Cursor window. You run `/fill-tag` in chat yourself.
No `CURSOR_API_KEY`, no Docker agent. Source vault stays clean until Accept.

```powershell
# Source repo must be clean/committed first.
./.cursor/sdk/open_chat_sandbox.ps1 Networking/OSI
```

In the new window:

```
/fill-tag Networking/OSI --limit 1
```

Resume the same clone later:

```powershell
./.cursor/sdk/open_chat_sandbox.ps1 --workspace .cursor/sdk/runs/<id> Networking/OSI
```

Accept / Drop / Source — same as Cover (`switch_review.ps1 -Kind Fill …`).
Optional: push the clone branch and open a GitHub PR instead of local Accept.

This isolates the vault copy only. Cursor still runs on the host; for hard
filesystem isolation use a VM.

## Cover vault

You pick a tag. Docker runs `/refine-tags` and `/cover-tag` on that leaf, or on
the leaves under that parent — never on parent nodes or ancestors. The source
vault is untouched until you accept the clone.

## Run

In a shell with a clean repo and `CURSOR_API_KEY` set:

```powershell
./.cursor/sdk/run_cover_vault.ps1 Java/Language/Primitives/ShortType
```

HTML **Agent ▾ → General** copies that command. **Agent ▾ → Focused** copies
the same command with empty `--focus ''`; fill the quotes in the terminal.
After a run, **Clone ▾** appears on the **launched** tag only (Open / Continue /
Focused / Accept / Drop), even if Focused created a new descendant leaf. Chat
skills are under **…**. **Source** returns to this vault.

```powershell
Get-Content .cursor/sdk/runs/<id>/cover-run.log -Wait
```

`--wait` keeps the launcher attached.

## Review

```powershell
./.cursor/sdk/switch_review.ps1 Java/Spring/Transactions
./.cursor/sdk/switch_review.ps1 -Source
```

Clone rebuilds that run's coverage index and opens a second Cursor window.

Another pass in the same clone:

```powershell
./.cursor/sdk/run_cover_vault.ps1 --workspace .cursor/sdk/runs/<id> Java/Spring/Transactions
```

`Continue` only resumes unfinished state. To add a specific missing angle even
when the broad leaf is already complete, use **Clone ▾ → Focused** and fill
`--focus` in the terminal:

```powershell
./.cursor/sdk/run_cover_vault.ps1 --workspace .cursor/sdk/runs/<id> Java/Spring/Transactions --focus 'Calls between @Transactional methods'
```

Focused mode first maps the request to one honest leaf under the selected tag.
It may create that leaf and retag relevant parent cards, then covers only the
selected leaf. It fails closed if no valid target leaf is reported.
When resuming an older clone, the launcher first copies the current committed
control scripts and relevant skills from the clean source vault into that clone.

Accept (cherry-pick into this repo, delete the clone, hide the Clone button):

```powershell
./.cursor/sdk/switch_review.ps1 -Accept Java/Spring/Transactions
```

Drop without merging:

```powershell
./.cursor/sdk/switch_review.ps1 -Drop Java/Spring/Transactions
```

Source Control in the clone window shows the uncommitted cover diff. The source
repository must be clean before `-Accept`.

## Defaults

`grok-4.6` high, `--cover-limit 50` (cap, not a target), `--max-passes-per-tag 5`.
A real run requires a chosen tag. Cover is leaf-only: a leaf is covered by itself;
a parent covers its descendant leaves only. Hitting the 50-card cap marks
`review_required`; continue with `--continue-tag`.
