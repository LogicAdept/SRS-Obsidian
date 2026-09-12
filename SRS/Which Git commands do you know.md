<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# Which Git commands do you know

> [!abstract] Short answer
> The daily core is small: `clone / pull / push` to move history to and from a remote, `add / commit` to record it, `status / log / diff` to inspect it, `branch / checkout / switch / merge / rebase` to shape it. Around that core sit the rescue tools — `stash`, `reset`, `revert`, `reflog`, `cherry-pick` — and the investigation tools `blame` and `bisect`. Knowing *what each command moves* (worktree, index, local history, remote) matters more than knowing many of them.

## The working set, grouped by what it touches

**Moving work in.** `git add` stages file changes into the index; `git commit` records the staged snapshot as a new node in history; `git status` shows the boundary between worktree, index and HEAD at any moment. The full walk-through of that boundary is [[What are the working directory the staging area and the repository in Git]].

**Moving history around.** `git clone` copies a whole repository; `git fetch` downloads new commits from a remote without touching your branches; `git pull` is fetch plus integrate (merge or rebase); `git push` uploads your commits. Details and the fetch-vs-pull trap: [[How do you download changes from a remote Git repository]].

**Shaping branches.** `git branch` lists and creates branches, `git switch` (or the older `checkout`) moves between them, `git merge` joins two lines of history, `git rebase` replays one line on top of another. When to prefer which: [[How does Git rebase differ from merge]] and [[How would you explain the Git merge command]].

**Inspecting.** `git log --oneline --graph` shows history as a graph, `git diff` compares worktree/index/commits, `git show` prints any object, `git blame` attributes lines. For a single look back: [[How do you inspect the previous Git commit]].

```text
$ git checkout -b feature/order-flow
Switched to a new branch 'feature/order-flow'
$ git add OrderService.java
$ git commit -m "Add order flow service"
[feature/order-flow 6ac3c2f] Add order flow service
 1 file changed, 12 insertions(+)
$ git checkout main
Switched to branch 'main'
$ git merge feature/order-flow
Updating 1df7631..6ac3c2f
Fast-forward
 OrderService.java | 12 ++++++++++++
 1 file changed, 12 insertions(+)
```

**Listing 1.** git 2.47.3 — the loop a backend engineer runs dozens of times a day: branch, stage, commit, integrate (verbatim output from the empirics sandbox).

**Rescue tools.** `git stash` shelves uncommitted work ([[How would you explain git stash]]); `git restore` discards file changes; `git reset` / `git revert` undo commits at different risk levels ([[What is the difference between git reset revert and checkout]]); `git reflog` recovers "lost" commits ([[What is git reflog and how do you recover lost commits]]); `git cherry-pick` copies one commit onto another branch ([[What is git cherry-pick and when do you use it]]). Investigation under pressure: `git bisect` hunts the regression commit ([[What is git bisect and how do you use it]]).

> [!warning] The dangerous set is small but sharp
> `push --force` (prefer `--force-with-lease`), `reset --hard` on uncommitted work, history rewriting on shared branches, and `clean -fd` without `-n` dry-run first. These are the commands that destroy work that was not pushed anywhere — everything else is recoverable through the reflog. See [[Why should you not rewrite history of shared branches]] for the shared-history rules.

```d2
direction: right
wt: "worktree\n(files on disk)" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
idx: "index\n(add / restore --staged)" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
hist: "local history\n(commit / reset / revert)" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
rem: "remote\n(fetch / pull / push)" {
  width: 230
  height: 90
  style.fill: "#f3e5f5"
}
wt -> idx: "add"
idx -> hist: "commit"
hist -> rem: "push"
rem -> hist: "fetch"
```

**Fig. 1.** Every everyday command moves information one step along worktree → index → local history → remote.

> [!tip] Interview answer
> **My daily set is add/commit/status to record work, fetch/pull/push to sync, branch/switch/merge/rebase to shape history, and log/diff/show/blame to inspect it. For recovery: stash, restore, reset, revert, reflog, cherry-pick; for investigations, bisect. The mental model is that each command moves changes between worktree, index, local history and remote — and the few genuinely dangerous ones are force-push, hard reset and history rewriting on shared branches.**

