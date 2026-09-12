<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How would you explain the Git merge command

> [!abstract] Short answer
> `git merge <branch>` integrates the commits of the named branch into your *current* branch. If history has not diverged, Git **fast-forwards** — just moves the branch pointer. If both branches have commits, Git computes a **three-way merge** against the common ancestor and records a **merge commit with two parents**, tying the lines of history together. Files both sides touched can conflict and must be resolved by hand ([[What is a merge conflict and how do you resolve it]]).

## The three outcomes

```text
$ git log --oneline --graph main feature      # divergent tips
* a007554 Main: add OrderRepository
| * 8efdc49 Feature: add OrderValidator
|/
* dbe5cb2 Base: OrderService skeleton
$ git merge main                              # on feature: three-way
Merge made by the 'ort' strategy.
 OrderRepository.java | 1 +
 1 file changed, 1 insertion(+)
$ git log --oneline --graph -3
*   1943e28 Merge main into feature
|\
| * a007554 Main: add OrderRepository
* | 8efdc49 Feature: add OrderValidator
|/
* dbe5cb2 Base: OrderService skeleton
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): the merge commit carries two parents — first parent is where you stand (`feature`), second is what you merged in. Tooling and `git log --first-parent` rely on that order.

- **Fast-forward** (no divergence): target is a direct descendant — Git moves the pointer and *creates no commit*. History stays linear; see the full demo in [[What kinds of Git branch merges exist]].
- **Three-way merge** (diverged): Git finds the **merge base** (common ancestor), diffs both sides against it, and combines non-overlapping changes automatically; the `ort` strategy is the default engine in modern Git and is noticeably better at renames than the old `recursive` default.
- **Conflict** (both sides changed the same lines): Git stops mid-merge, marks files unmerged, and waits for a human — abort cleanly with `merge --abort` if you are not ready ([[What is a merge conflict and how do you resolve it]] walks the resolution).

## Options that change the shape of history

`--no-ff` forces a merge commit even when fast-forward is possible — the merge becomes an explicit, revertible record "this feature existed" (teams use it to keep feature granularity on the main line). `--ff-only` refuses to create merge commits — the gatekeeper for "linear history" policies (CI often enforces it; my fetch-integrate demo uses it in [[How do you download changes from a remote Git repository]]). `--squash` collapses the branch's changes into *staged* edits without a merge commit and without parent links — you then commit once yourself; convenient for noise-free history, at the price of losing branch identity (`git log` will not show it was a branch). `--abort` rolls back a conflicted merge to the pre-merge state.

> [!warning] Merging is not a backup of the feature branch, and merge commits reorder nothing
> After merging feature into main, the feature branch still exists and still points at its own tip; teams that forget this accumulate zombie branches. A merge commit does not "update" the merged branch — main moves, feature stays. Revert semantics differ too: reverting a *merge commit* undoes the whole line in one commit, but re-merging that branch later requires reverting the revert or rebasing first — a classic production trap. And `--squash` produces unlinked history: later re-merge of the same branch will conflict with its own squashed content.

```d2
direction: right
base: "merge base\n(common ancestor)" {
  width: 250
  height: 80
  style.fill: "#e3f2fd"
}
a: "main commits" {
  width: 200
  height: 70
}
b: "feature commits" {
  width: 220
  height: 70
}
m: "merge commit\nparents: main, feature" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
base -> a
base -> b
a -> m: "first parent"
b -> m: "second parent"
```

**Fig. 1.** Three-way merge: diff main vs base, diff feature vs base, combine — the merge commit joins both tips and names the base implicitly.

> [!tip] Interview answer
> **git merge integrates another branch into the current one. With no divergence it fast-forwards the pointer; when history diverged it three-way-merges against the common ancestor with the ort strategy and records a merge commit with two parents — first the branch you were on. Conflicts stop the merge for manual resolution. The flags that matter: --no-ff to force an explicit merge commit, --ff-only for linear-history policies, --squash for one summary commit without links, --abort to bail out.**

