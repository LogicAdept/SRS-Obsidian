<!--
reps: 0
priority: 0
-->
#DevOps/VCS #SRS

# What kinds of version control systems exist

> [!abstract] Short answer
> There are two families: **centralized VCS** (CVS, Subversion/SVN, Perforce) where the history lives on one server and developers check out working copies, and **distributed VCS** (Git, Mercurial, Fossil) where every developer holds a *full copy of the whole history*, so committing, branching and history browsing work offline and the server is only a synchronization point. Git is the dominant distributed system today; the key practical difference is that distributed systems make branching and merging cheap, while centralized systems make them slow and heavyweight.

## Centralized: one server owns the history

In CVS and SVN the repository is a single database on a server. A developer runs `svn checkout`, gets a *working copy* of one revision, edits, and commits — a network operation that writes straight into the central history. Consequences follow from that shape:

- The server is a **single point of failure**; unless it is backed up, off-machine history is gone.
- Only the server knows the past: `svn log`, diffing old revisions, and branching need the network.
- Branches are directory copies (`svn copy`) — cheap to create but historically expensive to merge, which trained teams to branch rarely and integrate painfully.
- Access control is natural: the server can grant per-directory read/write permissions, which is why some enterprises still keep Perforce for huge monolithic assets.

## Distributed: everyone owns the whole history

Git (and Mercurial) clone the *entire repository* — every commit, every branch, every tag — onto your machine. Committing is a purely local operation; `git push` and `git pull` merely exchange commits with another copy, usually a shared "origin" server. This is why [[What is Git for]] describes Git as a content-addressed database first and a synchronization tool second.

- History work is instant and offline: log, blame, and diffs never touch the network.
- Branches are a pointer to a commit — creating one is a one-file write (see [[How would you explain what a Git branch is]]), so feature branches, experiments, and rework are routine.
- There is no single point of truth *by design*: any clone is a valid backup, and hosting platforms (GitHub, GitLab) are merely the copy everyone agrees to watch — see [[What is the difference between Git and GitHub]].
- The cost: the mental model is harder (local vs remote branches, push/fetch), and access control moves to the hosting layer.

```d2
direction: right
central: {
  server: "Central server\n(only copy of history)" {
    width: 280
    height: 90
    style.fill: "#ffebee"
  }
  w1: "working copy\n(svn checkout)" {
    width: 240
    height: 80
  }
  w2: "working copy" {
    width: 240
    height: 80
  }
  w1 -> server: "commit = network"
  w2 -> server: "commit = network"
}
```

**Fig. 1.** In a centralized VCS every write reaches one server; the working copies hold a single revision, not history.

```d2
direction: right
d1: "Dev clone\nfull history" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
d2: "Dev clone\nfull history" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
origin: "Shared origin\n(push/pull hub)" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
d1 -> origin: "push"
origin -> d1: "fetch/pull"
d2 -> origin: "push"
origin -> d2: "fetch/pull"
```

**Fig. 2.** In a distributed VCS each clone holds complete history; origin is a convention, not a requirement.

> [!warning] "Distributed" does not mean "no central server in practice"
> Teams still agree on one canonical remote as the integration point — otherwise pull requests and CI would have nothing to watch. The difference is that the central copy is a *policy choice*, not a *technical necessity*: if it dies, any clone can replace it.

> [!tip] Interview answer
> **Centralized systems like CVS and SVN keep history on one server; you commit over the network and branches are heavyweight. Distributed systems like Git give every developer a full copy of history, so commits and branches are local and instant, and the server is just the agreed synchronization hub. Git won because cheap branching made feature-branch workflows and code review practical.**

