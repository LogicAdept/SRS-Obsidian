<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is HEAD and what is a detached HEAD

> [!abstract] Short answer
> **HEAD** is Git's pointer to "where you are right now": normally a *symbolic reference* to the current branch (the file `.git/HEAD` contains `ref: refs/heads/main`), which in turn points at the latest commit of that branch. Commits extend the branch under HEAD. **Detached HEAD** is the state after checking out a raw commit, tag, or other non-branch reference: HEAD holds the commit id directly, so new commits are built on *no branch* and become orphaned the moment you switch away — recoverable only through the reflog.

## Normal state: HEAD rides a branch

When HEAD → `main` → commit C, `git commit` creates a new commit D whose parent is C and moves `main` (and HEAD along with it) to D. Every branch operation you know is expressed in these terms: `status` reports "on branch main" because HEAD is symbolic; [[How would you explain what a Git branch is]] builds on the fact that a branch is just a ref file HEAD can point to.

## Detached state: standing on a commit, not a branch

```text
$ git checkout main~0
Note: switching to 'main~0'.
...detached HEAD advice...
HEAD is now at 2b5a507 Second commit
$ git status
HEAD detached from 2b5a507
nothing to commit, working tree clean
$ git commit -m "Commit made while detached"
$ git checkout main
Warning: you are leaving 1 commit behind, not connected to
any of your branches:

  54cc51a Commit made while detached
Switched to branch 'main'
$ git log --oneline -1 'HEAD@{1}'   # still reachable via reflog
54cc51a Commit made while detached
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): committing while detached works fine — but switching back leaves the commit with no ref pointing to it, and only the reflog ([[What is git reflog and how do you recover lost commits]]) remembers it.

Legitimate uses of detached HEAD: inspecting or building an exact historical revision (`checkout v2.3.1` to reproduce a release), running a one-off experiment you intend to throw away, or bisecting — [[What is git bisect and how do you use it]] deliberately parks you on bare commits while hunting a regression. CI systems often check out a commit by hash and work detached by design.

> [!warning] The trap is committing *accidentally* in detached state
> It usually happens via `git checkout <tag-or-commit>` followed by normal work. Two commits later you `git switch main` and the work "disappears" — nothing is deleted, but nothing references it, and garbage collection prunes unreachable commits eventually (weeks, not minutes). Rescue is `git branch fix/<topic> <sha>` from the warning output or the reflog. Submodule checkouts are the other common source of detached HEADs — [[What are Git submodules and when do you use them]] keeps them intentional by pinning a commit on purpose.

```d2
direction: right
main: "branch ref\nrefs/heads/main -> C2" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
head: "HEAD\nref: refs/heads/main" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
det: "HEAD (detached)\ndirect -> 54cc51a" {
  width: 290
  height: 90
  style.fill: "#ffebee"
}
c2: "C2" {
  width: 130
  height: 70
}
orphan: "54cc51a\nno ref points here" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
head -> main: "symbolic"
main -> c2
det -> orphan: "you are here"
```

**Fig. 1.** Attached HEAD delegates to a branch ref; a detached HEAD pins a raw commit — and whatever it builds there is unreachable from any branch.

> [!tip] Interview answer
> **HEAD is the pointer to the current position: normally a symbolic ref to a branch, so commits extend that branch. In detached HEAD it points straight at a commit — useful for inspecting or building a specific revision — but commits made there belong to no branch, and switching away orphans them; the reflog or the checkout warning's suggested branch command is the rescue. Detached state is expected with tags, CI checkouts and bisect — dangerous only when accidental.**

