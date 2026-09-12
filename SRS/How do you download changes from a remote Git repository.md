<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How do you download changes from a remote Git repository

> [!abstract] Short answer
> `git fetch origin` **downloads** new commits and updates the remote-tracking refs (`origin/main`) but touches *none* of your branches — you inspect and integrate deliberately. `git pull` is **fetch + integrate**: it downloads and immediately merges (or rebases, with `pull --rebase`) into the current branch. The professional habit is fetch-then-look-then-integrate; the interview trap is knowing that after `fetch` your working branch has *not changed at all*.

## Fetch vs pull, verbatim

```text
$ git fetch origin
From …/remoteteam/origin
   598fdba..85983c4  main       -> origin/main
$ git status -sb
## main...origin/main [behind 1]
$ git log --oneline main..origin/main     # what fetch brought
85983c4 Dev1: more work
$ git merge --ff-only origin/main         # integrate deliberately
Fast-forward
 app.txt | 1 +
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): fetch moved *only* `origin/main`; `status -sb` reports the local branch behind; the range `main..origin/main` shows the incoming commits ([[How can you refer to a commit in Git]]), and only the explicit merge changes your branch.

After `fetch`, the interesting questions are all ref-vs-ref: `git diff main origin/main` (content), `git log main..origin/main` (what's incoming), `git log origin/main..main` (what we'd push), `git log --graph --all` (the whole picture). Integration is then a decision: fast-forward when your branch has nothing new (`merge --ff-only` enforces it), a real merge when diverged ([[How do you merge two divergent Git branches]]), or rebase your unpushed work on top ([[How does Git rebase differ from merge]]).

`pull` = the same thing compressed: `pull --no-rebase` merges FETCH_HEAD into your branch (writing a merge commit when diverged — [[How would you explain the Git merge command]]'s three outcomes), `pull --rebase` replays your local commits on origin's tip (cleaner history while they are unpushed). Modern Git can make the default explicit and safe: `git config pull.rebase true` (or `pull.ff only` to forbid surprise merge commits) — the config exists because default `pull` behavior surprised too many people ([[What are the levels of git config]] shows where such settings live).

## Related fetch knowledge interviewers probe

- **`fetch --prune`** deletes remote-tracking refs for branches deleted on the server — without it, `origin/*` fills with ghosts; `--prune-tags` does the same for tags.
- **`fetch` never touches your worktree** — that is why it is safe on a dirty tree and in CI scripts; *pull* can refuse when uncommitted changes collide with incoming ones.
- **`clone --depth 1`** (shallow clone) downloads only the latest commit — huge time saver in CI; `rev-parse --is-shallow-repository` detects it, and history-dependent tools (bisect, blame beyond depth) need `fetch --unshallow` ([[What is git bisect and how do you use it]]'s prerequisite).
- **Tracking branches**: `branch -vv` shows each local branch's upstream and ahead/behind; `branch --set-upstream-to=origin/main main` fixes a missing pairing.

> [!warning] A plain `git pull` on a diverged branch writes a merge commit you may not want — and pull with dirty files can fail
> The "pull surprise" merges remote work into yours under a default message, burying integration decisions; teams avoid it by fetching first or pinning `pull.rebase`/`pull.ff`. And pulling with uncommitted local changes is refused when the merge would touch the same files — the stash ([[How would you explain git stash]]) exists exactly for that detour. Note also that fetch *does* move remote-tracking refs and can run server-side hooks for hosted flows ([[What are Git hooks]]' server-side cousins), but it neither modifies your commits nor starts any integration.

```d2
direction: down
rem: "origin/main\n(remote truth)" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
f: "git fetch\nupdates origin/main only" {
  width: 340
  height: 100
  style.fill: "#e3f2fd"
}
om: "local origin/main\nupdated; branches untouched" {
  width: 340
  height: 100
  style.fill: "#fff3e0"
}
dec: "inspect: log main..origin/main" {
  width: 360
  height: 90
  style.fill: "#fff3e0"
}
int: "integrate: merge --ff-only /\nmerge / pull --rebase" {
  width: 360
  height: 100
  style.fill: "#e8f5e9"
}
rem -> f
f -> om
om -> dec
dec -> int
```

**Fig. 1.** Fetch stops at updating the tracking refs; integration is a separate, chosen step — that separation is the whole professional habit.

> [!tip] Interview answer
> **git fetch downloads new commits and moves the remote-tracking refs like origin/main without touching my branches, so I can review incoming work with log main..origin/main and integrate deliberately — ff-only when possible, merge or rebase when diverged. git pull is fetch plus immediate integration: merge by default, --rebase for clean history on unpushed work — and since that default surprises people, modern repos pin pull.rebase or pull.ff. I also keep fetch --prune in the routine so deleted remote branches stop haunting origin/*.**

