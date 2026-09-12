<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is the difference between Git and GitHub

> [!abstract] Short answer
> **Git** is the open-source distributed version control system — a command-line tool and data model that records history; it works entirely offline on your machine. **GitHub** is a commercial *hosting platform* built around Git repositories: it stores a canonical remote copy and adds the collaboration layer Git deliberately lacks — pull requests with review, issues, CI/CD (Actions), permissions, code search, package and artifact hosting. GitLab and Bitbucket are competing platforms providing the same category. Git works without any of them; none of them work without Git.

## Tool vs platform

Git's scope is version control: commits, branches, merges, and the transfer protocol between repositories ([[How does Git store data internally]] for the model). Everything Git knows happens between *repositories* — push, fetch, clone ([[How do you add a remote to a local Git repository]]). GitHub's scope is *everything around the repository*: who may push to which branch (protection rules that make [[Why should you not rewrite history of shared branches]] enforceable), how changes get proposed and approved (pull requests — [[What is a pull request and why is it not a push request]]), what runs when code lands (Actions triggering [[What is CI]]), and the social surface (issues, discussions, stars, projects).

```text
$ git remote -v
origin	/home/z/dev/shared.git (fetch)
origin	/home/z/dev/shared.git (push)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): Git is perfectly functional with a *filesystem directory* as its remote — no hosting platform involved. GitHub is one possible (and dominant) replacement for that directory, adding services around it.

Practical distinctions interviewers listen for:

- **Auth and identity**: Git commits carry author/committer strings written locally, unverified unless signed ([[What does a commit object contain]]); GitHub attaches *account identity* — login, verified email, profile — and gates access per account.
- **Review model**: Git has none; the PR (or GitLab's merge request) is the platform's invention — branch comparison, line comments, approvals, status checks.
- **Automation**: Git hooks run on *one machine* ([[What are Git hooks]]); platform CI runs *per repository event* with shared runners and secrets.
- **Distribution**: your Git clone is complete; the platform copy is the agreed *canonical* one — the hub of the star topology ([[What kinds of version control systems exist]]'s distributed picture).

> [!warning] "Just push it to GitHub" is where Git ends and the platform begins — with different failure modes
> GitHub outages do not affect local commits, branching, or offline work — only collaboration; conversely, GitHub's protection rules cannot save a repo whose contributors rewrite local shared branches. Corporate GitLab *is* Git like GitHub is — the workflow transfers, the feature names differ (merge request vs pull request). And platform-specific artifacts (issues, PR discussions, Actions logs) are not in Git at all: migrating hosts moves the repository, not its conversation history.

```d2
direction: right
git: "Git\nhistory model + CLI\nworks offline" {
  width: 300
  height: 110
  style.fill: "#e3f2fd"
}
hub: "GitHub / GitLab / Bitbucket\nhosting + PR review + CI + issues" {
  width: 360
  height: 120
  style.fill: "#fff3e0"
}
dev1: "developer clone" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
dev2: "developer clone" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
dev1 -> hub: "push / PR"
hub -> dev1: "fetch"
dev2 -> hub: "push / PR"
hub -> dev2: "fetch"
git -> dev1: "runs inside"
git -> dev2: "runs inside"
```

**Fig. 1.** Git runs inside every clone and mediates repo-to-repo transfer; the platform is the social hub above it.

> [!tip] Interview answer
> **Git is the open-source version control system itself — a data model and CLI that records and synchronizes history between repositories, fully functional offline and against any remote, even a filesystem path. GitHub is a hosting platform around Git: canonical remote plus pull-request review, issues, CI, permissions and identity. GitLab and Bitbucket are the same category. Commits are Git's, unverified unless signed; accounts, approvals and automation are the platform's — and a platform outage never blocks local work.**

