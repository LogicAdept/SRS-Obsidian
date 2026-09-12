<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How would you explain what a Git branch is

> [!abstract] Short answer
> A Git branch is a **movable pointer to a single commit** — a 41-byte file in `.git/refs/heads/` containing a commit id. That is the entire mechanism. Commits themselves already know their parents, so the branch gives a *name to a line of work's latest state* and advances automatically when you commit on top of it. Branches cost nothing to create, which is why Git workflows branch constantly.

## The mechanism, verbatim

```text
$ git rev-parse main
dbe5cb28c59ee3ce3a9f285ad7ae660e1712ecaf
$ git cat-file -p refs/heads/main     # reading the ref file through git
tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
author SRS Demo <srs-demo@example.com> 1788253260 +0000
committer SRS Demo <srs-demo@example.com> 1788253260 +0000

Base: OrderService skeleton
$ git log --oneline --graph --all     # two branches, one root
* a007554 Main: add OrderRepository
| * 8efdc49 Feature: add OrderValidator
|/
* dbe5cb2 Base: OrderService skeleton
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): `rev-parse main` prints what the ref file contains — a commit id; the ref *file* resolves to the commit object. After `checkout -b feature` and one commit, `feature` and `main` are two ids sharing a parent — no copies of files were made.

What follows from the pointer design:

- **Creating a branch** = writing one small file (`git branch feature`); switching = moving HEAD ([[What is HEAD and what is a detached HEAD]]). No directory copies, no locks, nothing proportional to project size — the reason people say "branches are free".
- **Committing advances the branch**: the new commit's parent is the id the branch holds, then the branch file is rewritten to the new id.
- **History is a graph, not a line**: two branches are two named tips into one DAG. Merging connects them ([[How would you explain the Git merge command]]); rebase rewrites one tip onto another ([[How does Git rebase differ from merge]]).
- **Comparison with SVN** frames the interview answer: a Subversion branch is a *server-side directory copy* of the whole tree — creating is cheap, but merging and tooling treat it as heavyweight; in Git the default workflow assumes a branch per task ([[What are Git branches for]]).

```d2
direction: right
main: "refs/heads/main\n-> a007554" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
feat: "refs/heads/feature\n-> 8efdc49" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
base: "dbe5cb2\nBase" {
  width: 190
  height: 70
}
m: "a007554\nMain: OrderRepository" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
f: "8efdc49\nFeature: OrderValidator" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
main -> m
feat -> f
f -> base
m -> base
```

**Fig. 1.** Two ref files, one shared base commit. The "branches" you see in tools are just the commits reachable from each tip.

> [!warning] "Pointer" means cheap — and means nothing protects a branch by default
> Any ref can be moved, deleted or force-pushed: `git branch -D`, `git push --force`, history rewriting — all operate on the same 41-byte files. Deleting a branch does *not* delete commits (they linger reflog-recoverable until GC), but it does remove the only *named* path to them. Default branches carry extra weight: protection rules on `main` exist precisely because a branch is just a name that CI and teammates trust ([[Why should you not rewrite history of shared branches]]).

> [!tip] Interview answer
> **A branch is a movable pointer to a commit — literally a text file holding a commit id — while the commits themselves already chain through parent pointers. Creating or switching a branch costs nothing, committing just advances the pointer, and history stays one graph with multiple named tips. That cheapness is what enables branch-per-task workflows; the flip side is that nothing technically protects a ref, so deletions and force-pushes are policy problems, enforced on the hosting layer.**

