<!--
reps: 0
priority: 0
-->
#DevOps/VCS #SRS

# What are version control systems for

> [!abstract] Short answer
> A version control system (VCS) records the history of a set of files as a sequence of snapshots, so a team can develop in parallel, review and integrate each other's work, walk back to any earlier state, and answer *who changed what, when, and why*. For a backend engineer it is the backbone of collaboration: branches isolate experiments, commits carry context, and the repository is the single source of truth that CI/CD and code review are built on.

## The four jobs a VCS does

**History.** Every saved state (a *commit*) is stored with its author, timestamp, and pointer to the previous state, so nothing that was ever committed is truly lost. When a bug appears in production, you can compare today's code against the last known good release and find the exact change that broke it. This is the "undo button" for entire projects, not just single files.

**Parallel work.** Without a VCS, two people editing the same project would have to take turns or email files back and forth. A VCS lets everyone work in their own *branch* and merge the results, detecting which edits genuinely clash. See [[What kinds of version control systems exist]] for how centralized and distributed systems differ in who owns the history.

**Integration and review.** Modern teams do not commit straight to the main line: changes go through pull requests where peers read the diff, CI runs the tests, and only then is the branch merged. The VCS is the platform this whole process rides on — [[What is CI]] describes the automation that is triggered on every push.

**Traceability.** Because every commit names its author and links to an issue or ticket, the repository doubles as project documentation: [[What is git blame and how is it used]] shows how to ask "who last touched this line", and release tags answer "what exactly shipped to the customer".

## What a VCS is not

> [!warning] A VCS is not a backup, a build system, or a secret store
> Backups protect against hardware loss; a VCS protects against *human* loss of context — but a corrupted server still needs real backups. Build tools like [[Which build tools for Java do you know]] compile and package code — running them from a repo does not make the repo a build system. And anything committed stays in history forever: passwords in a commit remain recoverable even after the file is deleted, so secrets belong in a vault, not in version control.

Database changes are a special case — schema definitions are versioned like code, but with dedicated tooling ([[Which database schema versioning tools do you know]]), because applying "version 14" to a live database is very different from checking out an old file.

```d2
direction: right
work: "Developers\nwork in branches" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
vcs: "VCS repository\nhistory + merge + review" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
ci: "CI/CD builds and tests\nevery change" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
ops: "Releases, tags,\ntraceability, rollback" {
  width: 260
  height: 90
  style.fill: "#f3e5f5"
}
work -> vcs: "commits"
vcs -> ci: "push triggers"
ci -> ops: "green build"
vcs -> work: "merge + history"
```

**Fig. 1.** The VCS sits between developers and the delivery pipeline: it collects parallel work, hands it to CI, and keeps the history both depend on.

> [!tip] Interview answer
> **A version control system records file history as snapshots so a team can work in parallel, review and merge each other's changes, roll back to any state, and trace who changed what and why. It is the foundation for code review and CI/CD — and it is not a backup, not a build tool, and never a place for secrets, because committed history is permanent.**

