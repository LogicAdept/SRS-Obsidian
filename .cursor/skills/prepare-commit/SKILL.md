---
name: prepare-commit
description: >-
  Summarizes the current git working tree and drafts a copy-paste PowerShell
  git add + git commit command with the message already filled in. Use when
  the user invokes /prepare-commit or asks for a commit message, a summary of
  current changes, or a command they can copy to commit.
disable-model-invocation: true
---

# Prepare a copy-paste commit command

## Purpose

Read the working tree, summarize what changed, and **stop**. The deliverable is
one PowerShell block the user can paste. Do **not** `git add`, `git commit`, or
`git push`.

## Invoke

```
/prepare-commit
```

No arguments. Inspect whatever repository the workspace is (source vault or a
cover clone).

Chat may follow the user's language. The **commit message is English**.

## Read first (run in parallel)

From the repository root:

```powershell
git status
git diff --stat
git diff
git diff --cached --stat
git diff --cached
git log -12 --format="%s"
```

If `status` shows untracked files that look like real work, `git diff --
<path>` will be empty — read those files instead of guessing.

## Message

Match this repo: imperative subject, no `feat:` / `fix:` prefix.

- One line if that is enough; a second sentence only when the why is not obvious.
- Focus on **why**, not a file list.
- Accurate: "add" for new work, "update" for an existing feature, "fix" for a
  bug. Do not claim a refactor unless that is the change.

Examples of the local style: `Add per-tag open, accept, and drop for agent clones`,
`Improve interface flow`.

## What to include

Stage only files that belong in the commit. List them explicitly in `git add --`.
Never tell the user to `git add -A`.

Leave out:

- secrets (`.env`, `credentials.json`, API keys)
- `__pycache__/`, `*.pyc`
- gitignored noise (`coverage-clones.js`, `.cursor/sdk/runs/`, `cover-run.log`)

If something is already staged, keep it in the commit unless it is junk — then
say so and omit it from the command.

If there is nothing to commit, say that. Do not invent a command.

## Chat result

1. Short grouped summary of the diff (what actually changed).
2. **Last**, one fenced `powershell` block and nothing after it. That block is
   the product: only runnable lines, no comments.

Unstaged leftover that you intentionally skipped: mention it **above** the
block, not inside it.

Chat copy-paste often flattens the fence into one line. Do **not** use
backtick line continuation or a here-string (`@' … '@`): both need real
newlines and fail with `UnexpectedCharactersAfterHereStringHeader`.

Use one paste-safe line: spaces between `git add` paths, `;` before
`git commit`, a PowerShell single-quoted `-m` string. If the message
contains `'`, double it (`'it''s'`).

```powershell
git add -- "path/one" "path/two"; git commit -m 'Subject line here.'
```

If everything to commit is already staged:

```powershell
git commit -m 'Subject line here.'
```

One `git add --` plus one `git commit`. Do not add `git push`.
