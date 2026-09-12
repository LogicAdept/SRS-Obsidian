<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How do you make your first Git commit and add all files

> [!abstract] Short answer
> `git init` turns a directory into a repository, you set your identity once (`user.name`, `user.email`), then `git add .` stages everything that is not ignored and `git commit -m "..."` records the first snapshot. `git status` and `git log` confirm the result. The clone path is different: `git clone` creates the repo *with* history, so you commit on top of it instead of initializing.

## The sequence, with real output

```text
$ git init -b main
$ git config user.name "SRS Demo"
$ git config user.email "srs-demo@example.com"
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	report.md

nothing added to commit but untracked files present (use "git add" to track)
$ git add report.md
$ git status --short
A  report.md
$ git commit -m "Add weekly report stub"
$ git log -1 --stat
commit 96826df4eb2d18fe7a4a7d5f26cec18d89a24edb
Author: SRS Demo <srs-demo@example.com>
Date:   Tue Sep 1 09:01:00 2026 +0000

    Add weekly report stub

 report.md | 1 +
 1 file changed, 1 insertion(+)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): init, identity, stage, commit, verify. The short status `A ` means the file is in the index but not yet committed.

Step notes that interviewers probe:

- **`git init -b main`** creates `.git` and names the initial branch; on older Git the default was `master`, configurable through `init.defaultBranch`. `init` never touches existing files — it only adds the `.git` database.
- **Identity comes from the config hierarchy** — [[What are the levels of git config]] explains `--local` vs `--global`; without it Git refuses to commit and asks you to set `user.email`/`user.name` first.
- **`git add .` vs `git add -A` vs `git add <file>`**: in modern Git all three stage everything from the current directory; the explicit path is still the safest habit for a first commit of a *cleaned* project.
- **Before the first `add`**: create [[What is .gitignore]] — `target/`, `node_modules/`, IDE folders, logs, local secrets. After the first commit, untracking mistakes means history surgery ([[Why should you not rewrite history of shared branches]] shows why that is expensive).
- **`git commit` without `-m`** opens an editor; commits with empty messages are refused.

> [!warning] A first commit is not a push, and `init` is not a remote
> The new repository is strictly local. Publishing it takes `git remote add origin <url>` plus `git push -u origin main` — [[How do you add a remote to a local Git repository]] walks through exactly that. Also verify nothing sensitive made it into the commit: the history is permanent, and `git rm --cached` after the fact does not remove the blob from earlier commits.

```d2
direction: down
init: "git init -b main\ncreates .git" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
add: "git add .\nworktree -> index" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
commit: "git commit -m\nindex -> first snapshot" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
push: "remote add + push -u\npublish to origin" {
  width: 280
  height: 90
  style.fill: "#f3e5f5"
}
init -> add: "status shows ?? files"
add -> commit: "A  staged"
commit -> push: "log shows root commit"
```

**Fig. 1.** The first commit pipeline: initialize, stage, snapshot, publish. Each step is verified with `status`, then with `log`.

> [!tip] Interview answer
> **`git init -b main` creates the repository, I configure user.name and user.email, write a .gitignore before staging anything, then `git add .` and `git commit -m` to record the root snapshot — verified with `status` and `log`. If the project comes from an existing remote I use `git clone` instead of `init`, and publishing afterwards means `git remote add origin` plus `git push -u origin main`.**

