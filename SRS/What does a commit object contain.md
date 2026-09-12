<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What does a commit object contain

> [!abstract] Short answer
> A commit object holds five things: a pointer to the **tree** (the snapshot of the whole project at that moment), pointers to **parent commit(s)** (one for normal commits, two for merges, zero for the root), **author** name/email/date, **committer** name/email/date, and the **commit message**. The commit id is the SHA-1 of exactly this content — so any change to any of these fields produces a different commit.

## Reading a real one

```text
$ git cat-file -p HEAD
tree 71ab9f3d9dfc2afcc1959aba3ecb32abea592f4b
author SRS Demo <srs-demo@example.com> 1788253260 +0000
committer SRS Demo <srs-demo@example.com> 1788253260 +0000

First commit
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim, root commit): no parent line — a commit with parents has one `parent <sha>` line per parent, merge commits have two.

Field-by-field:

- **tree** — the id of the root tree object: the complete, deduplicated snapshot of every file and directory ([[How does Git store data internally]] walks the whole chain). The commit does not contain file content; it names the tree that does.
- **parent(s)** — the backbone of history. A regular commit has one parent; a merge commit has two or more (first parent = the branch you were on, second = what was merged in — [[How would you explain the Git merge command]] uses this to read graphs); the very first commit has none.
- **author vs committer** — the two can differ: author wrote the change, committer applied it. Rebasing, cherry-picking and applying patches keep the original author but put the rewriter in committer (and the *committer* date changes while the author date is preserved — [[How does interactive rebase work and how do you squash commits]] shows the effect).
- **message** — free text; conventions like imperative subject line + blank line + body exist because tooling (releases, changelogs, `git log --oneline`) treats the first line as an identifier.

## Why this shape matters

Because the id hashes all five fields together, a commit is immutable: amending, rebasing, or even re-committing with a different timestamp creates a *new* commit id — the foundation of Git's integrity guarantees and the reason shared-history rewriting is disruptive ([[Why should you not rewrite history of shared branches]]). Because parents chain backwards, "history" is a directed acyclic graph, not a line: branches are just named tips into that graph, which is what makes [[How would you explain what a Git branch is]] so cheap to implement.

> [!warning] A commit does not contain your working-directory state
> Unstaged and untracked files are not part of any commit — the tree only reflects what was in the index at commit time (see [[What are the working directory the staging area and the repository in Git]]). Also the commit stores *metadata as given*: timestamps can be anything (they are data, not truth — empirics scripts fix them for deterministic ids), and author identity comes straight from config with no verification unless signing is enforced. Empty commits exist too (`--allow-empty`) and are legitimate markers in release flows.

```d2
direction: down
c1: "commit A\ntree TA\nauthor · message" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
c2: "commit B (merge)\ntree TB · parents: A, C" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
c3: "commit C\ntree TC" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
t: "tree TB\nfull snapshot of the worktree" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
c2 -> c1: "parent 1"
c2 -> c3: "parent 2"
c2 -> t: "tree"
```

**Fig. 1.** A merge commit carries two parents and one tree; the graph, not the files, is what history operations traverse.

> [!tip] Interview answer
> **A commit object stores a pointer to the tree snapshot, one parent per parent commit (two for merges, none for root), author and committer identity with dates, and the message — and its id is the SHA-1 of exactly those fields, so commits are immutable. File content lives in blobs behind the tree, not in the commit. Author vs committer differ after rebase or cherry-pick, and because the graph is parent-linked, branches are just names pointing into it.**

