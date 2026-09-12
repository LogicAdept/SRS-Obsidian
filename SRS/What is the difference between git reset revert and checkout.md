<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is the difference between git reset revert and checkout

> [!abstract] Short answer
> Three tools for three targets. **`checkout`/`switch`/`restore` move *you* (or a file) between states without changing history**: switch changes branches, restore discards file-level edits. **`reset` moves a *branch pointer* backward (or to any commit)** and optionally rewires index and worktree — history after the pointer is abandoned on that branch. **`revert` writes a *new commit* that inverses an old one** — history keeps growing, nothing is rewritten. The shared/unsafe dimension: revert is safe anywhere; reset rewrites shared history; restore/checkout touch no history at all.

## The decision table

| You want to… | Tool | History rewritten? |
|---|---|---|
| Look at another branch | `git switch <branch>` | no |
| Discard uncommitted file edits | `git restore <file>` | no |
| Unstage (index → worktree) | `git restore --staged <file>` / `git reset` | no |
| Drop the last commit *locally* | `git reset --soft/--mixed/--hard HEAD~1` | yes, branch only |
| Undo a *pushed* commit, visibly | `git revert <sha>` | no (adds a commit) |
| Park uncommitted work temporarily | `git stash` ([[How would you explain git stash]]) | no |

```text
$ git log --oneline            # three commits: v3, v2, v1
1170dae v3
$ git reset --soft HEAD~1      # pointer only; change sits staged
$ git reset --mixed HEAD~1     # + index reset; change unstaged
$ git reset --hard 'HEAD@{2}'  # back to v3 via reflog; worktree reset too
HEAD is now at 1170dae v3
$ git revert HEAD --no-edit
[shared bf07dcc] Revert "v3"
 1 file changed, 1 deletion(-)
$ git show HEAD:app.txt        # content v2 again — but v3 still in history
v1
v2
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim, abridged): reset walks pointer→index→worktree as its mode escalates ([[What is the difference between git reset soft mixed and hard]] has the full matrix); revert leaves the graph intact and appends the inverse.

## Checkout's double life

`checkout` historically did *two* jobs: move HEAD between branches and copy file versions around — which is why modern Git split it: `switch` for branches, `restore` for files. Interview-safe mapping: `checkout <branch>` ≈ `switch`; `checkout -- <file>` ≈ `restore <file>`; `checkout <sha>` detaches HEAD ([[What is HEAD and what is a detached HEAD]]) — inspecting history, not undoing it.

## Why revert is the production answer

Shared branches are consumed by teammates and CI; removing commits from under them ([[Why should you not rewrite history of shared branches]]) breaks every clone. Revert communicates *negation in the open*: everyone sees v3 arrive and be undone, deployments diff cleanly, and re-landing v3 later means reverting the revert or cherry-picking the original ([[What is git cherry-pick and when do you use it]]). Reset is for local messes: undoing your last unpushed commit, unstaging everything, wiping the worktree to a known state.

> [!warning] reset --hard deletes uncommitted work with no prompt — and "I already pushed it" makes reset a team problem
> Uncommitted changes (and untracked files) are not in any commit; `reset --hard` cannot restore them, and neither can the reflog — only *committed* states are recoverable ([[What is git reflog and how do you recover lost commits]]). The second trap is reset on a *shared* branch: your push afterwards needs `--force`, which is exactly the history-rewriting incident the force-with-lease guard exists for. `checkout -- <file>` and `restore <file>` share the same data-loss property at file level: the discarded edits never existed in Git's world.

```d2
direction: right
r: "restore / switch\nmoves files or YOU" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
rs: "reset\nmoves the BRANCH POINTER" {
  width: 290
  height: 100
  style.fill: "#ffebee"
}
rv: "revert\nappends an inverse commit" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
r -> rs: "deeper: touches recorded history"
rs -> rv: "shared branch? use this"
```

**Fig. 1.** Escalation ladder: file/position ops are harmless; reset rewrites a branch's future; revert changes nothing already published.

> [!tip] Interview answer
> **Restore and switch are the safe layer — they move files or me between existing states without touching history. Reset moves a branch pointer and, by mode, the index and worktree — right tool for undoing unpushed commits, dangerous on shared lines and fatal to uncommitted changes. Revert appends a new commit that inverses an old one — nothing rewritten, so it is the answer for anything already pushed. I reach for reset locally, revert in public, and switch/restore for pure navigation and file-level undo.**

