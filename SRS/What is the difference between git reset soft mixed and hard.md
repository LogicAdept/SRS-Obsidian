<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is the difference between git reset soft mixed and hard

> [!abstract] Short answer
> All three `reset` modes move the current branch pointer to the given commit; they differ in **how much of your work they leave in place**. `--soft` touches only the pointer — the undone changes stay **staged** in the index. `--mixed` (the default) also resets the index — changes remain as **unstaged** edits in the worktree. `--hard` resets pointer, index *and* worktree — the changes are **gone** as uncommitted content (committed-but-abandoned commits remain reflog-recoverable). Choose by what you want to keep: `soft` to recommit differently, `mixed` to restage selectively, `hard` to trust the target state completely.

## One scenario, three escalations

```text
$ git log --oneline                       # v3 <- v2 <- v1
$ git reset --soft HEAD~1                 # drop v3
$ git status --short                      # v3's change: staged
M  app.txt
$ git reset --mixed HEAD~1                # drop v2 too
$ git status --short                      # changes: only in worktree
 M app.txt
$ git reset --hard 'HEAD@{2}'             # recover v3 via reflog
HEAD is now at 1170dae v3
$ git reset --hard HEAD~1                 # abandon v3 entirely
HEAD is now at dc4cbae v2
$ git status --short                      # clean — no trace
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): soft leaves the change in the index (`M ` — first column), mixed demotes it to the worktree (` M` — second column), hard clears everything down to the target snapshot. The three-area model behind the columns: [[What are the working directory the staging area and the repository in Git]].

The mental picture: reset is "move the branch pointer, then *optionally* drag the index and worktree along to the target". A second use of the same command has no mode at all: `git reset <paths>` (no commit argument) copies entries from HEAD into the index for just those paths — the old-style "unstage". Modern spelling of that case is `git restore --staged` ([[What is the difference between git reset revert and checkout]] maps the family).

## Choosing in practice

- **`--soft`** — remake the last commit(s): `reset --soft HEAD~1`, adjust, commit again; also the standard "squash my last N unpushed commits into one" recipe (`reset --soft HEAD~N && git commit`) without interactive rebase ([[How does interactive rebase work and how do you squash commits]]).
- **`--mixed`** — "unstage everything, I'll re-decide": after `git add .` panic, or to restage in coherent chunks.
- **`--hard`** — make the worktree exactly match a commit: abandoning local experiments, cleaning a botched state before `pull`, recovering by pointing at a reflog entry ([[What is git reflog and how do you recover lost commits]] is the undo of this undo).

> [!warning] --hard is the only mode that destroys content — and it destroys exactly the uncommitted part
> Worktree edits and staged-but-uncommitted changes have no commit, no object, no reflog entry: `reset --hard` deletes them *permanently*. What reset --hard *does* leave recoverable are the abandoned commits themselves — through the reflog until garbage collection prunes them. Two production habits follow: run `git stash` ([[How would you explain git stash]]) or `git status` before any `--hard`, and never `reset --hard` a *shared* branch — the push that follows needs force ([[Why should you not rewrite history of shared branches]]). Also note `reset` never touches other branches and never touches the remote — divergence afterwards (`git status -sb` showing ahead/behind) is your signal.

```d2
direction: right
soft: "--soft\nbranch pointer moves\nindex: keeps changes\nworktree: keeps changes" {
  width: 300
  height: 130
  style.fill: "#e8f5e9"
}
mixed: "--mixed (default)\nbranch pointer moves\nindex: reset to target\nworktree: keeps changes" {
  width: 300
  height: 130
  style.fill: "#fff3e0"
}
hard: "--hard\nbranch pointer moves\nindex: reset to target\nworktree: reset to target" {
  width: 300
  height: 130
  style.fill: "#ffebee"
}
soft -> mixed: "also reset index"
mixed -> hard: "also reset worktree"
```

**Fig. 1.** The modes are cumulative: each adds one more area dragged to the target commit; soft changes only history.

> [!tip] Interview answer
> **All three move the branch pointer; they differ in what survives. Soft keeps the undone changes staged — remake a commit. Mixed, the default, also resets the index so changes become unstaged — re-decide what to stage. Hard additionally resets the worktree to the target — full local reset, and the only one that permanently destroys uncommitted work. Abandoned commits stay reflog-recoverable, but uncommitted content does not, and hard-resetting a shared branch turns into a forced push, which is a history-rewriting incident.**

