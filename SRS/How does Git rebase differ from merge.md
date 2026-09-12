<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How does Git rebase differ from merge

> [!abstract] Short answer
> Both integrate changes from one line of history into another. **Merge** creates a merge commit joining the two lines — history keeps its real shape. **Rebase** *replays* your commits one by one on top of the target tip, creating **new commits with new ids** and leaving history linear. Practical rule: rebase your own unpushed/unshared work for clean history; merge (or rely on the PR merge button) when the history is shared and rewriting it would hurt others.

## Same branches, two outcomes

```text
$ git log --oneline --graph --all        # before: diverged
* 77f74bb wip: more scratch
| * 86123b1 Main moves on independently
|/
* 1df7631 Base commit
$ git rebase main                        # on feature
Rebasing (1/3)...Successfully rebased and updated refs/heads/feature.
$ git log --oneline --graph --all        # after: linear
* 34b5221 wip: more scratch              <- new ids, same changes
* f40353e wip: scratch notes
* 6ac3c2f Add order flow: validator
* 86123b1 Main moves on independently    <- main tip
* 1df7631 Base commit
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): after rebase there is no merge commit and no fork — the three feature commits exist as *new* commits (new SHAs) stacked on main's tip. The old feature commits are orphaned, recoverable via [[What is git reflog and how do you recover lost commits]].

What each choice preserves and costs:

- **Merge** keeps true history (when things actually happened), records integration explicitly, and never rewrites ids — safe on any branch. Cost: non-linear graph and merge-commit noise; the integration is a real commit ([[How would you explain the Git merge command]]).
- **Rebase** produces readable linear history and defers conflict resolution to *your* commits — each replay step may stop with a conflict you fix once for that commit ([[What is a merge conflict and how do you resolve it]]). Cost: every replayed commit is a new object — shared ids change, which is exactly the "rewriting history" hazard.

## When rebase is the right tool

Updating a feature branch against a moving main before opening a PR (`git fetch && git rebase origin/main`) — the branch is yours, nobody builds on its ids, and the PR arrives conflict-free and readable. Cleaning local history before review: `rebase -i` to fixup/squash ([[How does interactive rebase work and how do you squash commits]]). Teams running **linear history** (rebase-then-fast-forward merges, enforced `--ff-only`) rebase *always* as the intake step.

> [!warning] The golden rule — and the exceptions people quote at interview
> Never rebase commits others may have pulled: their branch references old ids, and reconciling becomes a manual hunt. Nuances worth stating: rebasing *your own already-pushed* feature branch is fine if you are the only committer and you `push --force-with-lease` ([[Why should you not rewrite history of shared branches]]); hostings often offer "rebase and merge" as the *merge button's* strategy — the platform rebases for you, preserving the no-rewrite property for contributors. After rebasing over a conflicted replay, `git rebase --abort` restores the pre-rebase state exactly — the escape hatch to know under pressure.

```d2
direction: right
before: {
  b1: "A -> B -> C (main)" {
    width: 240
    height: 70
  }
  b2: "D -> E (feature)" {
    width: 220
    height: 70
  }
}
after: {
  a1: "A -> B -> C" {
    width: 200
    height: 70
  }
  a2: "D' -> E'\nnew ids, linear" {
    width: 240
    height: 80
    style.fill: "#e8f5e9"
  }
  a1 -> a2: "rebase replays"
}
before -> after: "merge would add M(A..E); rebase rebuilds"
```

**Fig. 1.** Merge would produce commit M with two parents; rebase produces D′ and E′ — same changes, new ids, straight line.

> [!tip] Interview answer
> **Merge joins two lines with a two-parent merge commit and keeps history as it happened; rebase replays my commits onto the target tip, producing new commit ids and a linear history. I rebase my own unshared work — updating a feature branch on main, cleaning history interactively — and merge or let the PR button integrate shared lines, because rebasing commits others already pulled forces everyone to reconcile rewritten ids. Conflicts during rebase resolve per replayed commit, and rebase --abort is the clean way out.**

