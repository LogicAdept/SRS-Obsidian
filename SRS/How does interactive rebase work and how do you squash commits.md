<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How does interactive rebase work and how do you squash commits

> [!abstract] Short answer
> `git rebase -i <base>` opens an editor listing the commits between `<base>` and HEAD, one per line, oldest first: `pick <sha> <message>`. You rewrite that *plan* — reordering lines, changing the verb (`squash`/`fixup` to fold a commit into the previous one, `reword` to edit a message, `edit` to pause, `drop` to discard) — and Git replays the plan, creating new commits as instructed. To squash the last N commits: `git rebase -i HEAD~N` and mark all but the first as `fixup`/`squash`.

## Folding messy commits — verbatim

```text
$ git log --oneline feature
77f74bb wip: more scratch
00a85bf wip: scratch notes
8a26b4f Add order flow: validator
1df7631 Base commit
$ GIT_SEQUENCE_EDITOR="sed -i '2,3s/^pick/fixup/'" git rebase -i HEAD~3
$ git log --oneline feature
6a86b73 Add order flow: validator     <- one commit now carries all three changes
86123b1 Main moves on independently
1df7631 Base commit
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): the todo list had `pick` on lines 1–3; replacing lines 2–3 with `fixup` folds both wip commits — content *and* no new message — into the validator commit. All three SHAs changed: replayed commits are new objects ([[How does Git rebase differ from merge]]).

Verb reference for the todo list: `pick` keep as is; `fixup` fold into the previous commit, discard its message (no editor round-trip); `squash` fold but *combine messages* (opens an editor — use when the summary should merge several intents); `reword` change the message only; `edit` stop after this commit (amend files, then `rebase --continue`); `drop`/deleting the line discards the commit. Non-interactive equivalents worth knowing: `git commit --amend` is rebase -i with one reword; `git reset --soft HEAD~N && git commit` is the poor-man's squash of trailing commits ([[What is the difference between git reset revert and checkout]]).

## What interactive rebase is actually for

Before opening a PR: turn "wip", "fix typo", "actually fix" into a small number of reviewable commits — the reviewer sees intent, not your typing rhythm. During a PR: incorporate review fixes as fixups and fold them (`git commit --fixup=<sha>` + `rebase -i --autosquash` automates the todo list). Also: dropping a commit that was a failed experiment, reordering to untangle independent changes, and splitting a commit with `edit`. All of this is *history rewriting* — legal on branches you own, forbidden on shared lines ([[Why should you not rewrite history of shared branches]]).

> [!warning] Rebase -i rewrites every id *after* the base — and stops mid-flight need your attention
> A conflict in the middle of the replay leaves you "interactive rebase in progress" with a partially applied plan: fix, `git add`, `git rebase --continue` (or `--skip` to drop that commit, or `--abort` to restore the pre-rebase state exactly). The old commits remain reachable via the reflog, so "I botched my rebase" is recoverable — [[What is git reflog and how do you recover lost commits]]. Two classic foot-guns: squashing commits that others reviewed makes the PR diff unreadable mid-review (fold only after the review round), and rebasing *merge commits* on your branch needs `--rebase-merges` to preserve them — otherwise they dissolve into their content.

```d2
direction: down
todo: "todo list (editor)\npick A\npick B\npick C" {
  width: 260
  height: 110
  style.fill: "#e3f2fd"
}
plan: "edited plan\npick A\nfixup B\nfixup C" {
  width: 250
  height: 110
  style.fill: "#fff3e0"
}
replay: "git replays A, folds B, C\nnew commit A'" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
res: "history: A' on <base>\nlinear, one meaningful commit" {
  width: 360
  height: 90
  style.fill: "#e8f5e9"
}
todo -> plan: "you edit"
plan -> replay: "save & close"
replay -> res
```

**Fig. 1.** Interactive rebase = edit a plan, Git executes it. Every executed step produces a *new* commit object; only the base stays identical.

> [!tip] Interview answer
> **Interactive rebase shows the commits since a base as an editable todo list — pick, fixup, squash, reword, edit, drop — and replays it, creating new commits per the plan. To squash the last three I run rebase -i HEAD~3 and mark the last two as fixup; commit --fixup plus --autosquash automates that during review rounds. It rewrites ids after the base, so it is for branches I own; mid-rebase conflicts are resolved with add plus rebase --continue, and abort or the reflog always gets me back.**

