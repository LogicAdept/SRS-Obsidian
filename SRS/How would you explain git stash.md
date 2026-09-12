<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How would you explain git stash

> [!abstract] Short answer
> `git stash` shelves uncommitted changes (worktree *and* index) into a stack of commits attached to no branch and returns your working copy to a clean HEAD — letting you switch branches, pull, or branch off without committing half-done work. `git stash pop` restores the top entry and drops it; `git stash apply` restores but *keeps* it; entries are listed by `git stash list` (`stash@{0}` newest) and removed by `git stash drop`. Stashes are local-only, LIFO, and untouched by branch switching.

## The cycle, verbatim

```text
$ git status --short                 # dirty: unfinished feature
 M app.txt
$ git stash push -m "wip feature"
Saved working directory and index state On main: wip feature
$ git status --short                 # clean — safe to switch/pull
$ git stash list
stash@{0}: On main: wip feature
$ git stash pop                      # restore AND drop
...modified: app.txt...
Dropped refs/stash@{0} (b904c915c4a1f9f4cf179f47ba1a377cfcd84e44)
$ git status --short
 M app.txt
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): the full shelf-return-restore cycle. The dropped sha is the stash commit — recoverable from the reflog if you drop too early ([[What is git reflog and how do you recover lost commits]]).

`pop` vs `apply` is the interview detail: **pop** = apply + remove from the stack (the default flow when the stash was a temporary detour); **apply** = apply but keep the entry (use when you may want the same change again — e.g. apply on another branch, or re-apply after an interrupted review). Other flags that come up: `stash -m` names the entry (do it — `stash@{2}` alone means nothing tomorrow); `stash -u`/`-a` include untracked (default) and ignored files — critical, because by default **new untracked files are not stashed** and will still block switches; `stash -p` stages interactively; `git stash show -p stash@{0}` inspects before applying.

## When stash is the right tool — and when it is not

Right: *brief* detours — "pull while I have dirty files", "hotfix branch in the next five minutes", "let me look at main without losing this". Also the safety move before any risky bulk operation (`reset --hard`, [[What is the difference between git reset soft mixed and hard]]). Not right: anything longer than a day — a stash commit has no branch, no PR, no CI, and stacks silently rot; commit to a `wip/...` branch instead ([[What are Git branches for]]). And it does not play with *state outside the worktree*: local databases, env files, Docker volumes stay as they were ([[What are Git branches for]]'s isolation warning applies verbatim).

> [!warning] Pop is not guaranteed to apply — conflicts leave the stash entry alive
> If the branch moved since the stash was taken (the usual case after a pull), `pop` can conflict; on conflict Git *keeps* the entry ("The stash entry is kept in case you need it again") and marks files unmerged — resolve as in any conflict ([[What is a merge conflict and how do you resolve it]]), then `stash drop` manually. The other trap: `git stash` without `-u` silently leaves new files behind, so after a "clean" stash your switch still fails — or worse, you carry untracked files into the next branch unknowingly. Long-lived stacks (`stash@{7}`) are a smell: name entries, and drop aggressively.

```d2
direction: right
dirty: "worktree + index dirty" {
  width: 270
  height: 80
  style.fill: "#fff3e0"
}
push: "stash push\ncommits to refs/stash, resets worktree" {
  width: 340
  height: 110
  style.fill: "#e3f2fd"
}
clean: "clean HEAD\nbranch ops allowed" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
pop: "pop = apply + drop\napply = apply only" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
dirty -> push
push -> clean
clean -> pop
pop -> dirty: "restore"
```

**Fig. 1.** Stash is a parking loop around the clean state: shelf the diff, do the detour, come back — with pop and apply differing only in whether the parking ticket is discarded.

> [!tip] Interview answer
> **git stash shelves uncommitted worktree and index changes as a stack of unnamed commits and resets the worktree to clean HEAD — for short detours like pulling or switching branches. pop applies and drops the top entry, apply keeps it; list, drop, and -m names manage the stack; -u is essential to include untracked files. Conflicts on pop keep the entry alive for manual resolution, and anything older than a day belongs on a real wip branch, not in a stash stack.**

