<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is git blame and how is it used

> [!abstract] Short answer
> `git blame <file>` annotates **every line** of a file with the commit that last touched it: short hash, author, date, line number, and content — the fastest answer to "who wrote this and when". The mature use is *investigation*, not accusation: pair it with the commit it names (`git show <sha>`) to learn *why* the line exists, and use its modifiers — `-L` for ranges, `-w` to ignore whitespace, `-M`/`-C` to follow moved or copied code, `--follow` to track renames — so refactors don't forge the trail.

## Reading blame output

```text
$ git blame app.txt
^934a47e (SRS Demo 2026-09-01 09:06:00 +0000 1) rev 1
cbb80bec (SRS Demo 2026-09-01 09:07:00 +0000 2) rev 2
bb71f3e9 (SRS Demo 2026-09-01 09:08:00 +0000 3) rev 3
0933e89c (SRS Demo 2026-09-01 09:09:00 +0000 4) rev 4
b8cd78b0 (SRS Demo 2026-09-01 09:10:00 +0000 5) rev 5
b8cd78b0 (SRS Demo 2026-09-01 09:10:00 +0000 6) buggy-line
6b84a0ed (SRS Demo 2026-09-01 09:11:00 +0000 7) rev 6
024e0a68 (SRS Demo 2026-09-01 09:12:00 +0000 8) rev 7
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): line 6 (`buggy-line`) carries the same hash as line 5 — one commit added both; the `^` prefix on line 1 marks the *boundary commit* (oldest reachable — the initial commit here). In a real team, names differ per line, which is what makes the output a lead: `git show 0933e89c` shows the change and its review context.

Flags that matter in production codebases:

- `-L 100,130` / `-L /fun:/return` — blame only a range (by lines or by regex-anchored region); the default whole-file dump is noise for big files.
- `-w` — ignore whitespace-only changes: reformatters stop hiding the real author.
- `-M` / `-C` — detect moved *within* the file / moved or copied *from other files*: after a big refactor, the original author follows the code instead of the refactor commit.
- `--follow <file>` — on `git log`, follows renames; blame tracks content regardless, but rename awareness matters for history depth.
- `git log -S"string"` / `-G<regex>` (pickaxe) — find commits where a *string entered or left* the codebase; when blame points at a mechanical reformat, pickaxe finds the *introducing* commit — the pairing interviewers like next to [[What is git bisect and how do you use it]].

## Blame in a review/debug workflow

The productive loop: `blame` the suspicious line → `show` the commit → read the PR/ticket it references → decide: intended behavior or regression? IDE blame plugins (GitHub/GitLab annotations) render the same data with commit links — same model, faster access. For "when did this API become deprecated" style questions across versions, blame a line *in a tagged revision* (`git blame v2.0 -- file`) — [[What is a tag in Git and how does it differ from a branch]] for pinning the revision.

> [!warning] Last-toucher is not origin-author — refactors forge blame without -M/-C, and squash merges flatten it
> A commit that moved a function across files becomes the "author" of every moved line unless `-C` digs deeper; a reformat with `-w` unread hides months of history. Squash-merge policies ([[What kinds of Git branch merges exist]]) collapse a PR into one commit: blame shows the squashed sha and the *merging* author — the real trail lives in the PR reference in its message, so follow the link instead of trusting the hash. Finally: blame output names colleagues; reading it as "who to blame" poisons teams — it is "which change introduced this", and the follow-up question is always *why* ([[How can you refer to a commit in Git]] for turning any hash in the output into a full id).

```d2
direction: down
line: "suspicious line in review" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
blame: "git blame -L <range>\nwhich commit last touched it" {
  width: 340
  height: 100
  style.fill: "#fff3e0"
}
show: "git show <sha>\nwhat and why changed" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
pick: "mechanical commit?\nlog -S / -G finds introducer" {
  width: 360
  height: 100
  style.fill: "#e8f5e9"
}
line -> blame
blame -> show
show -> pick: "refactor noise"
```

**Fig. 1.** Blame is the first hop of investigation, not the verdict: commit → show → (if the trail is forged) pickaxe.

> [!tip] Interview answer
> **git blame prints the last-touching commit for every line — hash, author, date — so I use it to locate the change behind a line, then git show that commit for context. Production modifiers matter: -L for ranges, -w to skip whitespace churn, -M and -C to follow moved or copied code through refactors, and log -S or -G when blame points at a mechanical commit and I need the true introducer. In squash-merge repos blame gives the squashed commit and I follow its PR link — and I read blame as which change introduced this, never as who to blame.**

