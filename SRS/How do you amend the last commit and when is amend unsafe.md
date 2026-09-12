<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How do you amend the last commit and when is amend unsafe

> [!abstract] Short answer
> `git commit --amend` replaces HEAD with a new commit: same parent, same snapshot plus whatever you staged — used to fix a typo in the message (`--amend -m "..."` or `--amend --no-edit` to keep it), add forgotten files, or adjust authorship. It is **safe only when the commit is unpushed or on a branch nobody else builds on**: amend does not extend history, it *replaces* the commit id, so a pushed-and-pulled amend is a shared-history rewrite with all of its consequences.

## The mechanics, verbatim

```text
$ echo 'fixup' >> app.txt && git add app.txt
$ GIT_AUTHOR_DATE=... git commit -q --amend --no-edit
$ git log --oneline -3
549676f Revert "v3"          <- same message, new id, extra change inside
1170dae v3
dc4cbae v2
$ git show HEAD --stat
    Revert "v3"

    This reverts commit 1170daeb6f0d4f50b4c59d9504da1a15b8e29870.

 app.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim, abridged): the amended commit folds the staged `fixup` change into the previous commit's snapshot. The id changed — [[What does a commit object contain]] explains why (the id hashes tree + parents + message + dates).

Variants worth knowing: `--amend` with no staged changes and `--no-edit` only re-creates the commit (useful to fix author/committer identity or re-sign); `--reset-author` stamps the current identity as author (after cherry-picking); amending an *empty* commit into a real one is the clean way to "un-mark" a release placeholder; and `--no-edit` + staged changes is exactly "add one file to the last commit without a new history entry". Amend is the single-commit special case of [[How does interactive rebase work and how do you squash commits]] (`reword`/`fixup` on the top commit).

## The safety rule and its boundary

**Unpushed → amend freely. Pushed → ask who has the commits.** If you are the sole author on a feature branch and CI only builds it, amending plus `push --force-with-lease` is routine ([[Why should you not rewrite history of shared branches]] details the guard). The moment others may have pulled, amend manufactures divergence: their old id hangs around while the remote holds the replacement, and reconciling is manual archaeology. On *protected* branches amend is not even a question — hosting rules reject the forced push.

> [!warning] Amend after a push is rewrite-in-place — the sharpest form of history rewriting
> The old commit id disappears from the branch, so every clone still holding it looks "behind" while actually holding a *different* commit — worse than an ordinary behind, because a naive pull merges the ghost and resurrects the pre-amend content ([[What is the difference between git reset revert and checkout]] contrasts revert's append-only safety). Two more traps: amending the wrong commit because HEAD moved (check `git log -1` *before* amending), and assuming amend keeps timestamps — committer date becomes *now*, author date is preserved; reproducible-build pipelines that embed dates notice.

```d2
direction: right
c1: "commit A (HEAD)\nparent: P" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
amend: "commit --amend\nstaged changes folded in" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
c2: "commit A'\nparent: P, new id" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
old: "A (orphaned)\nreachable via reflog only" {
  width: 290
  height: 90
  style.fill: "#ffebee"
}
c1 -> amend
amend -> c2
c1 -> old: "replaced, not deleted"
```

**Fig. 1.** Amend swaps A for A′ under the same parent P; A itself is orphaned, recoverable but no longer referenced by the branch.

> [!tip] Interview answer
> **Amend replaces the last commit with a new one — same parent, new id — folding staged changes and optionally a corrected message or authorship. It is the right tool for polishing my own unpushed work, and the wrong tool the moment the commit is pulled by others: their references then point at a dead id and the required forced push is a shared-history rewrite. I check log before amending, use force-with-lease when repushing my own branch, and reach for revert instead whenever anything is truly shared.**

