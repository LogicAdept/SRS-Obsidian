# Cover vault

The orchestrator refines the technical taxonomy and adds compact `#New` question
drafts. It never calls `/fill-tag`.

Real execution is only allowed inside the hardened Docker launcher. The launcher
creates a disposable Git clone, mounts only that clone read/write, keeps the
container root read-only, and does not mount the source vault or Docker socket.
The source vault changes only when you explicitly accept the reviewed clone diff.

## Run

From the repository root (the source repository must be clean):

```powershell
$env:CURSOR_API_KEY = "cursor_..."
./.cursor/sdk/run_cover_vault.ps1 --dry-run --max-tags 3
./.cursor/sdk/run_cover_vault.ps1 --max-tags 1
```

Resume the same disposable clone:

```powershell
./.cursor/sdk/run_cover_vault.ps1 --workspace "<run-dir>" --max-tags 1
```

Defaults are `grok-4.6` with `reasoning_effort=high`, `--prefix Java`,
`--cover-limit 50`, and `--max-passes-per-tag 5`. The limit of 50 is an upper
budget, never a target. Career, EngineeringLeadership, and ProjectManagement are
excluded unless `--include-nontechnical` is supplied. Use `--prefix ""` to cover
all technical paths.

## Queue and completion

The queue is derived on every run; it is never persisted. Scope filters remain
`--prefix`, repeatable `--only`, repeatable `--exclude`, and the default
nontechnical exclusions.

Order is deterministic:

1. dirty/new leaves;
2. leaves with zero directly assigned cards;
3. fewer direct cards;
4. deeper leaves;
5. lexical tie-breaker;
6. branches after leaves, only when their relevant children have converged.

`--max-tags N` selects N seed leaves. If refining a selected leaf creates children,
those descendants are added and processed before the selected node. Unrelated
siblings are not added. Branch work is taxonomy and aggregate validation; cover
does not create child-topic cards on a parent.

Refine runs at most once for a taxonomy fingerprint. Later work logs that refine
was skipped while the fingerprint is unchanged. A taxonomy change invalidates the
node; new children block and requeue their parent.

An eligible leaf receives at most one cover call per run. Cover writes a validated
repository-local structured result declaring created cues, coverage dimensions,
sources searched, candidate exhaustion, and budget status. Completion requires:

- the current taxonomy fingerprint was refined;
- relevant children are complete;
- all required finite coverage dimensions are satisfied;
- the strong-candidate search is exhausted;
- the card budget was not hit.

No empty verification call is required. A missing or invalid structured result
fails closed. If exactly 50 cards are created at the default cap, the node becomes
`review_required` and no second automatic batch runs. After review, continue it
explicitly:

```powershell
./.cursor/sdk/run_cover_vault.ps1 --workspace "<run-dir>" `
  --continue-tag "Java/Example"
```

## Tracked progress and review safety

Progress lives in the Git-tracked
`SRS/NamesHistory/coverage-progress.json`. It stores only seen nodes, not the
runtime queue. Each record includes taxonomy and card-assignment fingerprints,
children, status, dimensions, refine fingerprint, pass information, and the last
cover outcome.

The coverage fingerprint uses card basenames and thematic tag assignments. Editing
only a card body does not invalidate progress; adding/removing a card or changing
its thematic tags does. The progress file changes inside the disposable clone and
is accepted or rejected with the cards.

This also makes partial acceptance safe: if accepted cards or `Tags.md` differ from
the clone's progress record, the next run detects the fingerprint mismatch and
marks the node dirty. Rejecting the clone leaves source progress unchanged. The old
ignored `.cursor/sdk/cover-state.json` is not trusted as complete.

An empty initial progress file does not infer completion from the existing
thousands of cards. Nodes begin pending/dirty and can be advanced through scoped
runs.

## Review a run

The launcher prints the clone path and `agent/cover-*` branch:

```powershell
$run = "C:\Users\V\ObsidianVaults\SRS\.cursor\sdk\runs\<stamp-id>"
git -C $run status --short
git -C $run diff --stat
git -C $run diff
```

Review card names, tag ownership, `Tags.md`, and the tracked progress record.
Cover is forbidden from retagging existing cards or mutating siblings. Remove weak
or duplicate drafts before acceptance, then rebuild generated indexes:

```powershell
python "$run\.cursor\skills\process-topic\scripts\rebuild-coverage-index.py"
```

If selective review changes the accepted cards or taxonomy but leaves a stale
progress record, that is safe: fingerprints invalidate it on the next run. You may
also remove the affected node record before committing the clone.

Reject by deleting the run directory:

```powershell
Remove-Item -LiteralPath $run -Recurse -Force
```

To accept, commit only after review inside the clone, then fetch/cherry-pick that
clone branch into a clean source repository.
