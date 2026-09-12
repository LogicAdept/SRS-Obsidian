<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is git reflog and how do you recover lost commits

> [!abstract] Short answer
> The **reflog** is Git's local journal of *where each reference has pointed*: every commit, checkout, reset, rebase, and merge appends a line (default 90 days for reachable, 30 for unreachable entries — per ref, local-only). "Lost" commits — after `reset --hard`, a failed rebase, a deleted branch, or work committed in detached HEAD — are **not deleted**, they are merely unreferenced; the reflog remembers their ids, and `git reset --hard HEAD@{N}` (or `git branch <name> <id>`) makes them live again. Nothing in the reflog is ever pushed: it is per-machine insurance.

## Reading the journal and rescuing work

```text
$ git reflog
dc4cbae HEAD@{0}: reset: moving to HEAD~1
1170dae HEAD@{1}: reset: moving to HEAD@{2}
180b208 HEAD@{2}: reset: moving to HEAD~1
dc4cbae HEAD@{3}: reset: moving to HEAD~1
1170dae HEAD@{4}: commit: v3
dc4cbae HEAD@{5}: commit: v2
180b208 HEAD@{6}: commit (initial): v1
$ git reset --hard 'HEAD@{1}'      # v3 was dropped by HEAD~1 — bring it back
HEAD is now at 1170dae v3
$ git log --oneline
1170dae v3
dc4cbae v2
180b208 v1
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): each line = where HEAD pointed *after* that move. `reset --hard HEAD~1` orphaned v3, but entry `HEAD@{4}` (and `HEAD@{1}` after later moves) still holds it — reset there and the branch points at v3 again.

The three everyday rescues:

- **Undone by reset**: `git reset --hard HEAD@{N}` — walk the journal, find the pre-reset state ([[What is the difference between git reset soft mixed and hard]] shows the reset that created the problem).
- **Deleted branch**: `git branch -D feature` prints the last id, and so does `git reflog`; `git branch feature <id>` recreates it — branch deletion removes only the pointer ([[How would you explain what a Git branch is]]), not the commits.
- **Detached-HEAD work**: commits made while detached are orphaned on checkout; the checkout warning suggests `git branch <name> <sha>` — the sha is also `HEAD@{1}` ([[What is HEAD and what is a detached HEAD]]).

Behind the syntax: `HEAD@{N}` is "the N-th *previous* value of HEAD" — a reflog of the reflog; `main@{yesterday}` and `--date=iso` make the journal readable in time terms. During botched rebases the *old* commits live in `ORIG_HEAD` and the reflog of the branch itself (`git reflog show feature`), which is how [[How does interactive rebase work and how do you squash commits]] promises recovery.

> [!warning] The reflog is not a backup — it is local, expiring, and blind to never-added work
> Uncommitted changes destroyed by `reset --hard` or `checkout -- <file>` never entered a commit: no reflog entry can bring them back (stashed work has its own reflog, `git stash` — see [[How would you explain git stash]]). The journal expires (gc prunes unreachable entries), it exists only on the machine where the moves happened, and `--bare`/CI clones may have it disabled (`core.logAllRefUpdates`). The production lesson: reflog is your second chance, not your storage strategy — push early, push branches you care about, and treat "I'll commit later" as the real data-loss risk.

```d2
direction: down
ops: "commit · reset · rebase · checkout\nmerge · branch -D" {
  width: 340
  height: 100
  style.fill: "#e3f2fd"
}
journal: "reflog per ref\nHEAD@{0..N}: every past position" {
  width: 360
  height: 100
  style.fill: "#fff3e0"
}
lost: "branch tip moved away\ncommit unreferenced but alive" {
  width: 360
  height: 100
  style.fill: "#ffebee"
}
fix: "reset --hard HEAD@{N}\nor branch <name> <id>" {
  width: 360
  height: 100
  style.fill: "#e8f5e9"
}
ops -> journal
journal -> lost: "find the orphan id"
lost -> fix
```

**Fig. 1.** The reflog turns "lost" into "find the entry": every move of a ref is journaled locally, and any old position can be re-anchored.

> [!tip] Interview answer
> **The reflog is Git's local journal of where every ref has pointed — commits, resets, rebases, checkouts all append to it. Unreachable commits keep living until gc, so recovery is: read git reflog, find the pre-disaster position, reset --hard to that HEAD@{N} or branch a name at the id. It saves hard resets, deleted branches and detached-HEAD work — but it is local-only, expires after weeks, and never covers changes that were never committed, so it is recovery insurance, not a backup.**

