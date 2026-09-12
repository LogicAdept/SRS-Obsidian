<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What kinds of Git branch merges exist

> [!abstract] Short answer
> Four shapes matter in interviews and practice: **fast-forward** (pointer move, no commit — possible only when the target has no new commits), **three-way merge with a merge commit** (`--no-ff` or forced by divergence — records both parents), **squash merge** (`--squash` — all branch changes become one new commit *without* parent links to the branch), and the rarely-named **octopus merge** (a merge commit with three or more parents; `git merge a b c`). Which shape a team picks is policy: linear-history policies ban default merge commits; feature-tracking policies require them.

## Fast-forward vs three-way, verbatim

```text
$ git merge ff-line            # main has no new commits of its own
Updating a007554..c208ed1
Fast-forward
 Order.java | 2 ++
 1 file changed, 2 insertions(+)

$ git merge --no-ff noff       # forcing a merge commit instead
Merge made by the 'ort' strategy.
 Audit.java | 1 +
 1 file changed, 1 insertion(+)
$ git log --oneline -3
92bfe8a Merge Audit feature
86ef9b0 Noff: add Audit
c208ed1 FF candidate: append line
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): same kind of change, two shapes — fast-forward leaves no trace of the branch, `--no-ff` writes an explicit merge commit naming it.

- **Fast-forward** keeps history strictly linear but loses the fact that the work happened on a branch — CI built it, PR reviewed it, yet `git log` shows plain commits. Fine for personal or tiny-team flow.
- **Three-way / `--no-ff`** keeps a navigable record: the merge commit is a natural revert point for the whole feature and `--first-parent` walks show release history cleanly. Cost: graph noise on busy main lines, and reverting a merge later interacts with re-merges ([[How would you explain the Git merge command]] warns about revert-of-merge).
- **Squash merge** gives each PR exactly one commit on main — the GitHub/GitLab "Squash and merge" button is this. History reads like a changelog; but branch identity is gone and the branch's own commits are *not* ancestors of main, so blindly deleting + re-merging the branch, or rebasing it later, fights its ghost. Best for short-lived branches with messy in-progress commits.
- **Octopus** (`git merge b1 b2 b3`) is legal and occasionally used to integrate several tested topic branches at once, but it is mostly a curiosity — conflicts in multi-head merges are hard to reason about.

```d2
direction: right
ff: {
  a: "A -> B -> C" {
    width: 220
    height: 70
  }
  b: "main moves to C\n(no merge commit)" {
    width: 280
    height: 80
    style.fill: "#e8f5e9"
  }
  a -> b: "fast-forward"
}
noff: {
  x: "A -> B" {
    width: 160
    height: 70
  }
  y: "C" {
    width: 120
    height: 70
  }
  m: "M\nparents B, C" {
    width: 200
    height: 80
    style.fill: "#fff3e0"
  }
  x -> m
  y -> m
}
```

**Fig. 1.** Same two divergent situations, two shapes: a pointer move (top) versus an explicit two-parent merge commit (bottom).

> [!warning] The kinds are not interchangeable on shared branches
> A fast-forward policy ("rebase then ff-only") means every feature branch must be *rewritten* onto main before merging — pleasant linear history, but it requires the rebase discipline of [[How does Git rebase differ from merge]] and breaks on teams without it. A merge-commit policy preserves real history but means `git log` needs `--graph` literacy and revert-of-merge care. Squash merges quietly break `git blame`'s history depth (everything points at the one squashed commit) — archaeology moves to the PR URL instead ([[What is git blame and how is it used]]). Pick one policy per repository and enforce it on the hosting layer, not by convention.

> [!tip] Interview answer
> **Fast-forward is a pointer move with no commit, possible when the target has no new commits; a three-way merge records an explicit merge commit with both parents, --no-ff forces it even when ff is possible; squash merge turns the branch into a single new commit with no parent links — the Squash-and-merge button; octopus merges three-plus heads and is rare. The choice is team policy: linear history vs explicit feature record vs one-commit-per-PR changelog — each with its own revert and archaeology tradeoffs.**

