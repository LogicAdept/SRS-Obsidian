<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What are the working directory the staging area and the repository in Git

> [!abstract] Short answer
> Git sees your project through three areas. The **working directory** is the files on disk you actually edit. The **staging area (index)** is the draft of the *next* commit — exactly what `git add` puts there. The **repository** (`.git`) is the permanent history of committed snapshots. Changes flow worktree → index → repository: `git add` moves a file's current content into the index, `git commit` records the index as a snapshot. `git status` is the command that shows all three states at once.

## Why the index exists at all

Most systems track files individually; Git commits *whole snapshots*, and the index is the mechanism that lets you compose one. Without staging, every commit would include every pending change. With it, you can edit five files, then commit two of them as a coherent change and leave the other three in progress — a commit becomes a deliberate review unit, not a folder dump. The index is also what makes partial commits possible: `git add -p` stages interactive hunks, so even inside one file you can choose which lines belong to this commit.

The second job of the index is speed and integrity. Instead of hashing every file on every `status`, Git compares stat metadata recorded in the index; the content of each staged file is already stored as a blob object in `.git/objects`. That is why `git status` is instant even in huge repositories. Internally the index is the single file `.git/index` — a binary list of paths, blob hashes, and metadata; [[How does Git store data internally]] describes what those blobs are.

## Reading `git status` as a map of the three areas

```text
$ git status --short          # fresh file, not tracked yet
?? report.md
$ git add report.md
$ git status --short          # staged: index differs from HEAD
A  report.md
$ git commit -m "Add weekly report stub"
$ git status --short          # all three areas agree
$ echo 'second line' >> report.md
$ git status --short          # worktree differs from index
 M report.md
$ git diff --stat             # worktree vs index
 report.md | 1 +
 1 file changed, 1 insertion(+)
$ git diff --staged --stat    # index vs HEAD (after re-add)
 report.md | 1 +
 1 file changed, 1 insertion(+)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): one file walking the full path — untracked (`??`), staged (`A `), committed (clean), modified again (` M`). Two spaces before `M` would mean staged; one leading space means only the worktree changed.

Short codes worth memorizing: `??` untracked, `A` added to index, `M` modified (position of the letter tells you which area changed), `D` deleted, `UU` unmerged during a conflict ([[What is a merge conflict and how do you resolve it]]).

> [!warning] `git add` does not "add a file" — it snapshots its current content
> If you edit a file again after `git add` but before `commit`, the commit takes the *staged* version and quietly leaves the newer edit in the worktree. This is the classic "but I fixed that!" surprise; re-run `git add` after every change you want included. Also: a file already tracked is *not* protected from this flow, but it is also not hidden by [[What is .gitignore]] — that only affects untracked files.

Undo happens at each boundary with a different tool: `git restore <file>` (worktree), `git restore --staged <file>` or `git reset` (index), `git revert`/`git reset` (history) — [[What is the difference between git reset revert and checkout]] sorts them out.

```d2
direction: right
wt: "Working directory\nfiles you edit" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
idx: "Staging area (index)\n.git/index — next commit draft" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
repo: "Repository (.git)\ncommitted snapshots" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
wt -> idx: "git add"
idx -> repo: "git commit"
wt -> wt: "git restore  (discard edits)" {
  curve: 2
}
repo -> idx: "git restore --staged"
```

**Fig. 1.** `git status` diffs adjacent pairs: worktree↔index and index↔HEAD. Every everyday command moves content between these three areas.

> [!tip] Interview answer
> **The working directory is the files on disk; the staging area (index) is the draft of the next commit that `git add` composes; the repository is the committed history in `.git`. The index lets you build a commit deliberately — partially, file by file, hunk by hunk — and gives Git fast status checks because staged content is already hashed. Committing snapshots the index, not the worktree, so changes edited after `git add` are silently left out.**

