<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How do you inspect the previous Git commit

> [!abstract] Short answer
> For the commit *before* HEAD, Git gives you three lenses: **navigation** — `git show HEAD~1` prints the whole commit (message + patch), `git log -2` lists it, `git diff HEAD~1` compares the working state against it; **objects** — `git cat-file -p HEAD~1` dumps the raw commit object (tree, parent, author, message) for when you need fields, not prose; **ranges** — `git log HEAD~1..HEAD` shows exactly what the last step added. Abbreviations compose with the ancestry syntax of [[How can you refer to a commit in Git]].

## The everyday commands

```text
$ git log --oneline -2
96826df Add weekly report stub
$ git show HEAD~0 --stat           # --stat: which files, not the full diff
commit 96826df4eb2d18fe7a4a7d5f26cec18d89a24edb
Author: SRS Demo <srs-demo@example.com>
Date:   Tue Sep 1 09:01:00 2026 +0000

    Add weekly report stub

 report.md | 1 +
 1 file changed, 1 insertion(+)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): `show` = commit metadata + diff in one screen; `--stat` is the fast "what did it touch" view, drop it for the full patch.

Command-by-command intent:

- **`git show HEAD~1`** — "what did the previous commit change": message, author, and the patch. Add `-p` for merges (by default `show` on a merge prints only the combined diff view), `--name-only` for a bare file list (the classic "list files changed in commit X" interview ask).
- **`git diff HEAD~1`** — "how does the *current worktree* differ from the previous commit" — includes your uncommitted edits; `git diff HEAD~1 HEAD` is strictly committed-content comparison. This worktree flavor is how you answer "did my last change do what I think".
- **`git log -p -2`** — the last two commits *with* patches in one page; `git log --stat --oneline -5` for a compact overview.
- **`git cat-file -p HEAD~1`** — the raw object: tree id, parent id, author/committer, message ([[What does a commit object contain]] decodes it) — the debug view when `show` output is not enough.
- **Before *you* commit**: `git diff --staged` previews what the *next* commit will contain — the mirror-image inspection ([[What are the working directory the staging area and the repository in Git]]).

> [!warning] HEAD~1 depends on what HEAD is — and merges change the arithmetic
> On a branch that just merged, `HEAD~1` is the *first parent* (your branch's previous tip), not "the feature's last commit"; the feature tip is `HEAD^2` — walking `~` through merge-heavy history skips whole lines ([[How can you refer to a commit in Git]] details the operators). `show`/`diff` on a merge commit are the other surprise: a merge introduces no new *content* of its own, so `git show <merge>` shows only the conflict-resolution diff unless asked otherwise. And inspection is read-only by definition — but a *detached* HEAD from careless `checkout <sha>` is not ([[What is HEAD and what is a detached HEAD]]).

```d2
direction: right
c1: "HEAD~1\nprevious commit" {
  width: 220
  height: 90
  style.fill: "#fff3e0"
}
c2: "HEAD\ncurrent commit" {
  width: 200
  height: 90
  style.fill: "#e3f2fd"
}
wt: "worktree\nyour edits" {
  width: 200
  height: 90
  style.fill: "#e8f5e9"
}
c1 -> c2: "show: what c2 changed"
c1 -> wt: "diff HEAD~1\n(committed + edits)"
c2 -> wt: "diff\n(only edits)"
```

**Fig. 1.** Three inspection distances: commit-to-commit, commit-to-worktree, and the pre-commit preview — each answers a different question.

> [!tip] Interview answer
> **git show HEAD~1 for the previous commit's message and patch — --stat or --name-only for quick overviews; git diff HEAD~1 for how the current worktree differs from it, or diff HEAD~1 HEAD for pure committed comparison; log -p -2 to page through recent history; cat-file -p when I need raw fields. One caveat I keep in mind: after a merge, HEAD~1 follows the first parent, and merge commits print only their resolution diff unless -p is given.**

