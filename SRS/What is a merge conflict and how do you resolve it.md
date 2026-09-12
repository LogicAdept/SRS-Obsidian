<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is a merge conflict and how do you resolve it

> [!abstract] Short answer
> A merge conflict happens when two lines of history changed the **same region of the same file** (or one deleted what the other modified), and Git cannot choose for you. Git stops the merge, marks the file **unmerged** (`UU` in status), and writes both versions into the file between `<<<<<<< HEAD`, `=======`, and `>>>>>>> <other>` markers. Resolution = edit the file to the intended result, `git add` it (marks resolved), finish with `git merge --continue` (or `git commit`). `git merge --abort` backs out entirely.

## A real conflict, start to finish

```text
$ git merge conflictor
Auto-merging app.properties
CONFLICT (add/add): Merge conflict in app.properties
Automatic merge failed; fix conflicts and then commit the result.
$ git status --short
AA app.properties
$ git diff
++<<<<<<< HEAD
 +port=9090
++=======
+ port=8080
++>>>>>>> conflictor
$ merge --abort                # bail out; try again when ready
$ git merge conflictor         # resolve this time
printf 'port=9090\n# reviewed: main wins\n' > app.properties
$ git add app.properties
$ git status --short
M  app.properties
$ GIT_EDITOR=true git merge --continue
ain e5947c0] Merge branch 'conflictor'
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): conflict → markers in `diff` → abort → re-merge → edit → `add` → `--continue`. The `AA` short code means both sides added the file; `UU` is the modify/modify case.

What Git *can* merge automatically: changes in different files, or different regions of one file. What it cannot: overlapping edits to the same lines, delete-vs-modify, and any binary file (there are no lines to align — you pick one side with `git checkout --ours/--theirs <file>` or replace it wholesale).

## The resolution discipline that scales

1. **Read the graph first**: `git status` and `git log --merge -p <file>` show which commits contributed each side — blind marker-fixing is how teammate code gets silently dropped.
2. **Resolve to the *intended* state**, not to "ours" or "theirs" mechanically — the result often needs a third version (both changes, or a design decision). Tests after resolving, before continuing.
3. **`git add` is the "resolved" declaration** — it stages your chosen content; all conflict markers must be gone (`grep -n '<<<<<<<'` as a cheap check).
4. **Finish or bail**: `git merge --continue` (opens editor for the merge message) or `git commit` during a merge; `--abort` any time before committing. During a *rebase*, the same dance repeats per replayed commit with `git rebase --continue` ([[How does Git rebase differ from merge]]).

> [!warning] Marker syntax is plain text — commits containing it are silent landmines
> If someone resolves by committing *with* `<<<<<<<` left inside, the code compiles in some languages (Java strings, YAML text) and explodes much later. CI grep checks for markers are common for a reason. The other production trap: resolving a conflict by taking "ours" while the teammate's change was the *fix* — review every resolved hunk in the final diff before pushing. And remember a pull that stops mid-conflict is an ordinary merge in progress: finish it or `--abort`; do not stack new work on top ([[How do you merge two divergent Git branches]] shows the pull-then-conflict situation).

```d2
direction: down
m: "git merge" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
auto: "same file, same region?" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
ok: "auto-merged\nmerge commit written" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
stop: "STOP: UU file,\nmarkers inside" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
edit: "edit to intended state\ngit add" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
fin: "merge --continue\nor --abort" {
  width: 290
  height: 90
  style.fill: "#e8f5e9"
}
m -> auto
auto -> ok: "no overlap"
auto -> stop: "overlap"
stop -> edit
edit -> fin
```

**Fig. 1.** Conflict is not an error — it is a stopped merge asking for one decision: the intended content of the overlapping region.

> [!tip] Interview answer
> **A conflict is Git declining to guess: both sides changed the same region of a file. Git stops, writes both versions between marker lines, and marks the file unmerged. I resolve by reading what each side intended, writing the correct combined content, running the tests, staging with git add to mark resolution, and finishing with merge --continue — or aborting if the resolution needs a decision first. Binaries and delete-vs-modify need an explicit ours/theirs choice, and I check the final diff so no marker or teammate fix is lost.**

