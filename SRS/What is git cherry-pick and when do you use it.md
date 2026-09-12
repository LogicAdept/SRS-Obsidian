<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is git cherry-pick and when do you use it

> [!abstract] Short answer
> `git cherry-pick <commit>` takes *one* commit (or a range) and applies its change as a **new commit** on your current branch — same patch content, new id, single parent. It is the tool for copying an already-recorded change to another line of history without merging everything around it: shipping a hotfix to a release branch, back-porting a fix to an older version, lifting one reviewed commit out of a feature branch.

## Copying a commit across branches — verbatim

```text
$ git rev-parse --short side
c41210a
$ git cherry-pick side
ain b0c0778] Side: feature file
 Date: Tue Sep 1 09:04:00 2026 +0000
 1 file changed, 1 insertion(+)
 create mode 100644 side.txt
$ git log --oneline --graph --all
* b0c0778 Side: feature file      <- on main: new id, same change
* c9b3bc1 Main: parallel work
| * c41210a Side: feature file    <- original still on side
|/
* 03fd562 Base
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): the commit now exists on both branches with different ids. The author date is preserved; the committer is you ([[What does a commit object contain]] explains the two fields).

Typical backend situations:

- **Hotfix to release line**: production bug fixed on main must also ship in the maintained `release/2.1` branch — `checkout release/2.1 && cherry-pick <fix-sha>`, then tag a patch release ([[What is a tag in Git and how does it differ from a branch]]).
- **Long-term support backports**: the fix belongs to v1.x consumers; merge is impossible (v1.x diverged months ago), so fixes travel as cherry-picks.
- **Selective salvage**: a feature branch dies in review, but one commit was reviewed and approved — cherry-pick just that one onto main.
- **Reconstructing a botched flow**: after an accidental commit on the wrong branch — cherry-pick it to the right one, then remove it from the wrong one with `reset` ([[What is the difference between git reset revert and checkout]]).
- **Ranges**: `cherry-pick A..B` applies commits *after* A through B, in order; `A^..B` includes A itself.

> [!warning] Cherry-picked commits remember nothing about each other
> The new commit has a different id and no link to the original — `git log` will not warn you when the same change lands twice. Later merging the two branches makes Git's content matching usually reconcile the twins, but conflicts can result from the *same* change being applied on both sides. Discipline that avoids the pain: reference the original commit in the pick's message (`-x` flag appends "(cherry picked from commit …)"), and prefer merging when the *whole* line of work is wanted — cherry-pick is for the surgical cases. Conflicts during a pick are the ordinary resolution dance: fix, `add`, `cherry-pick --continue` (or `--abort`) — and like rebase, a pick rewrites nothing on the *source* branch, so shared history stays intact ([[Why should you not rewrite history of shared branches]]).

```d2
direction: right
src: "side branch\ncommit c41210a" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
dst: "main\nnew commit b0c0778" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
pick: "cherry-pick\ncopies the patch,\ngenerates a new id" {
  width: 260
  height: 110
  style.fill: "#e3f2fd"
}
src -> pick: "source commit untouched"
pick -> dst
```

**Fig. 1.** Cherry-pick is copy, not move: the source commit stays put; the destination receives a fresh commit carrying the same patch.

> [!tip] Interview answer
> **Cherry-pick applies a single commit's patch onto the current branch as a new commit with a new id — used for hotfixes to release branches, backports to supported versions, or lifting one approved commit out of a doomed branch. The source is untouched, so it is history-safe; the risks are duplicated change with no link between twins, so I use -x to record provenance, and I merge instead when the whole line of work is wanted. Conflicts resolve like any stopped operation: edit, add, continue.**

