<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How can you refer to a commit in Git

> [!abstract] Short answer
> A commit can be named many ways, and they compose: the **full or abbreviated SHA-1** (`2b5a507b…`, `2b5a507`), any **ref name** (`main`, `v2.0` — see [[What is a tag in Git and how does it differ from a branch]]), **HEAD** and its ancestry walk (`HEAD~3`, `HEAD^`, `main^2`), **`:/text`** search of commit messages, and **ranges** for log/diff — `A..B` (in B, not in A) and `A...B` (symmetric difference). Commands like `reset`, `revert`, `checkout`, `blame`, `bisect` all accept these; the safe habit for anything destructive is `git rev-parse <expr>` first to see what it resolves to.

## Ancestry syntax without tears

- `HEAD` — current commit; `@` is a synonym.
- `<ref>~N` — N *first-parent* steps back: `HEAD~2` = grandparent. On a merge-heavy history this walks the "straight line" of the branch you are on.
- `<ref>^` — one step back (`^` == `~1`); `<ref>^N` — the **N-th parent** of a merge commit: `HEAD^2` is the second parent of a merge, *not* the grandparent. This distinction is how you read merge commits ([[What does a commit object contain]] lists the parent fields).
- `HEAD@{N}` — where HEAD was N moves ago, from the reflog — the recovery syntax [[What is git reflog and how do you recover lost commits]] is built on.
- `main@{yesterday}` — the ref as of a time; useful, but depends on reflog availability.
- `:/keyword` — most recent commit whose message matches, e.g. `git checkout :/hotfix`.

```text
$ git rev-parse HEAD
2b5a507b57746f43e7e95340d983b9b182b76fb2
$ git rev-parse main^{commit}      # peel a ref/tag down to a commit
2b5a507b57746f43e7e95340d983b9b182b76fb2
$ git rev-parse HEAD~1..HEAD       # commits reachable from HEAD, not from HEAD~1
2b5a507b57746f43e7e95340d983b9b182b76fb2
^9c610c1c3e9be0f44396c7b931117daacdfadc17
$ git log --oneline -1 'HEAD@{1}'  # reflog-reachable commit (orphaned, detached demo)
54cc51a Commit made while detached
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): the same commit reached by ref, by ancestry, and through a two-dot range; the caret output is the internal form of "exclude this parent".

## Ranges: `A..B` vs `A...B`

`A..B` = commits in B but not in A — the review question "what will this merge bring?" (`git log origin/main..feature`). `A...B` = commits on either side but not both — with `git log --left-right` it shows what each branch has that the other lacks, the "how far did we diverge?" question ([[How do you merge two divergent Git branches]] lives in this territory). `git diff` accepts both with a subtly different meaning for `...` (diff from merge-base), which is the classic confusion: for *diffs* `git diff main...feature` means "what feature changed since the common ancestor", not the symmetric difference.

> [!warning] `~` and `^` look interchangeable — until a merge is involved
> `HEAD~2` and `HEAD^2` are completely different: the first is two first-parent steps, the second is the second parent of HEAD *if HEAD is a merge* (an error otherwise on non-merge commits in older Git; modern Git resolves `^2` on a non-merge to nothing sensible). Another trap: abbreviated SHAs are unambiguous only at the current object count — scripts should pass full hashes (and `--no-abbrev`) or use refs. And revision syntax is interpreted *before* filenames, hence the `--` separator convention in commands like `git log main -- file.txt` when a file and a branch share a name.

> [!tip] Interview answer
> **By full or short SHA, by ref name — branch or tag — by HEAD with ancestry suffixes: tilde-N for N first-parent steps, caret-N for the N-th parent of a merge, at-brace-N for reflog positions — by message search with colon-slash, and by ranges A-dot-dot-B and A-dot-dot-dot-B for what one side has that the other lacks. For anything destructive I confirm with rev-parse first; and I keep tilde and caret-N straight by remembering they diverge exactly on merge commits.**

