<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is Git for

> [!abstract] Short answer
> Git is a **distributed version control system**: it records the history of a project as a graph of content-addressed snapshots, lets developers work in parallel on cheap local branches, and synchronizes copies of that history through any shared remote. Practically it is used for source code history, code review via pull requests, release management, and as the integration point for CI/CD.

## What problem it solves

Before version control, teams shared archives and feared refactors: nothing could be undone, nobody knew who changed what, and parallel work meant merging files by hand. Git turns the project's history into a first-class object: every commit snapshots the whole tree, is identified by a cryptographic hash of its content, and points to its parent, so any state can be reproduced exactly (see [[How does Git store data internally]] for the object model behind this).

Because a branch is just a movable pointer to a commit, creating one costs nothing — which is what makes the modern workflow possible: a branch per feature or bugfix, a pull request per branch, merge after review. [[What are Git branches for]] covers why this isolation matters, and [[What is a pull request and why is it not a push request]] how it becomes a review artifact.

## Where Git shows up in a backend job

- **Daily development**: commit local work, rebase onto the moving main line, open a pull request — the loop every team lives in.
- **Integration with CI**: every push triggers builds and tests ([[What is CI]]); a green history is what gets deployed.
- **Release management**: tags name the exact snapshots that shipped ([[What is a tag in Git and how does it differ from a branch]]).
- **Investigation**: bisect finds the commit that introduced a bug, blame attributes lines ([[What is git bisect and how do you use it]], [[What is git blame and how is it used]]).
- **Configuration and infrastructure**: Jenkinsfiles, Dockerfiles and Kubernetes manifests live in the same repo, so infrastructure changes get the same review and history as code — GitOps takes this to the point where Git *is* the deployment source of truth.

## What Git is not

> [!warning] Git is not GitHub, and not a deployment or backup tool
*[[What is the difference between Git and GitHub]]* is the classic interview trap: Git is the version control tool, GitHub/GitLab are hosting platforms around it. A repository is not a backup strategy by itself, and committing something does not deliver it anywhere — that is what CI/CD pipelines do. Secrets committed "just temporarily" stay in history forever; removing them later requires history rewriting ([[Why should you not rewrite history of shared branches]]) plus credential rotation.

```d2
direction: right
dev: "Developer\ncommits locally" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
repo: "Git history\nsnapshots graph" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
pr: "Pull request\nreview + CI" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
rel: "Tagged release\nexact reproducible state" {
  width: 280
  height: 90
  style.fill: "#f3e5f5"
}
dev -> repo: "commit / branch"
repo -> pr: "push"
pr -> repo: "merge"
repo -> rel: "tag"
```

**Fig. 1.** Git history is the hub: local work lands in it, review and CI gate it, releases pin it.

> [!tip] Interview answer
> **Git is a distributed version control system that stores project history as content-addressed snapshots. It gives every developer full local history and zero-cost branches, which enables feature-branch workflows, pull-request review, CI on every push, exact release tags, and tools like bisect and blame. It is not GitHub, not CI, and not a secrets store — it is the versioned source of truth everything else builds on.**

