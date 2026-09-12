<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is the difference between clone fork and branch

> [!abstract] Short answer
> Three different levels of isolation. A **branch** is a pointer inside one repository — the lightweight way to separate lines of work ([[How would you explain what a Git branch is]]). A **clone** is a *copy of the whole repository* (history included) onto another machine or user — Git's native concept, created by `git clone`. A **fork** is a *platform-level* copy of someone's repository into your own account — Git does not know forks exist; the hosting (GitHub/GitLab) makes a second server-side repo and links the two. Work flows: branch for everyday tasks inside a repo you can push to; fork + clone *your* fork + branch when you cannot.

## What each one actually is

- **Branch** — a 41-byte ref in the shared repository. Zero setup, instant creation; used for features, fixes, experiments ([[What are Git branches for]]). Requires *write access* to the repository you branch in.
- **Clone** — a full copy of a repository's history on your machine: `git clone <url>` also configures `origin` automatically ([[How do you add a remote to a local Git repository]]). Every developer works in a clone — cloning is not an alternative to branching, it is the environment branches live in.
- **Fork** — a server-side clone under *your account* on the hosting. It exists because open-source and multi-team models deny direct write access: you cannot create a branch in a repo you cannot push to. The workflow: fork on the platform → `git clone` *your fork* (that becomes `origin`) → `git remote add upstream <original>` to keep pulling updates → branch in your fork → open a pull request *from your fork's branch to the upstream repo* ([[What is a pull request and why is it not a push request]]'s mechanics — cross-repo PRs are the fork's whole point).

```text
$ git remote -v
origin  /home/z/dev/shared.git (fetch)
origin  /home/z/dev/shared.git (push)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): after cloning, Git knows `origin` — the same wiring a fork-based setup gives your fork. Note what Git does *not* know: nothing here mentions forks; that relationship lives entirely on the platform.

## Choosing the isolation level

Same repository, write access → **branch** (the default in product teams; protection rules guard the main line). Write access denied, or third-party open-source contribution → **fork** (isolation is *organizational*: your fork's branches cannot touch upstream; your CI in Actions runs on your copy). Whole new machine or teammate → **clone** (plus a shallow variant for CI — `--depth 1` — see [[How do you download changes from a remote Git repository]]). Fork-also-for-teams appears where access boundaries mirror team boundaries: each team owns its fork, changes travel as PRs — heavier, but auditable.

> [!warning] Forks drift from upstream, and "I forked it" is not a contribution
> A fork is a *value snapshot at fork time*: without a recurring `fetch upstream && merge` (or rebase) loop it accumulates divergence until its PRs become archaeology — and issues/CI/secrets do *not* copy over; forks start bare of the upstream's conversation. Fork-based contribution etiquette: one feature branch per PR from *current* upstream state, never committing straight to your fork's main. And the trap interviewers enjoy: a fork is *not* a Git concept — `git://` knows nothing of it; `git clone` from a fork is indistinguishable from cloning any other repository, and "fork" operations (sync, compare) are platform UI, not Git commands ([[What is the difference between Git and GitHub]] — the boundary again).

```d2
direction: right
up: "upstream repo\n(team-owned, protected)" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
fork: "fork\n(your account, server-side copy)" {
  width: 340
  height: 100
  style.fill: "#fff3e0"
}
clone: "your clone\n(full history, origin = fork)" {
  width: 340
  height: 100
  style.fill: "#e3f2fd"
}
pr: "pull request\nfork branch -> upstream" {
  width: 320
  height: 100
  style.fill: "#f3e5f5"
}
up -> fork: "fork (platform action)"
fork -> clone: "git clone"
clone -> pr: "push branch"
pr -> up
```

**Fig. 1.** Fork workflow topology: the platform copies upstream into your account, your clone tracks the fork, and PRs carry changes across the ownership boundary.

> [!tip] Interview answer
> **A branch is a pointer inside one repository; a clone is a full copy of the repository on your machine with origin wired; a fork is a hosting-level copy of someone else's repo into your account — invisible to Git itself. Everyday team work is branches in a repo you can push to; forks are for write-less contribution: clone your fork, add upstream as second remote, branch there, PR back across the boundary. Forks drift without a sync loop and start without upstream's issues and CI — they are platform state, not Git state.**

