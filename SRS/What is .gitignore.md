<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is .gitignore

> [!abstract] Short answer
> `.gitignore` is a file of glob patterns telling Git which *untracked* files to leave out of version control — build outputs (`target/`), dependencies (`node_modules/`), IDE folders (`.idea/`), logs, and local secrets. It prevents noise in `git status` and, more importantly, prevents accidental commits of generated or sensitive files. It only affects untracked files: an already-tracked file is never hidden by `.gitignore`.

## Pattern syntax that actually matters

- `target/` — trailing slash restricts to directories.
- `*.log`, `*.class` — glob by extension, at any depth.
- `/build` — leading slash anchors the pattern to the `.gitignore`'s directory.
- `!important.log` — negation re-includes a file that earlier patterns excluded; order matters, last match wins.
- `**/logs` or `logs/**` — `**` crosses directory levels.
- Comments start with `#`; a blank line separates groups.

```text
$ git status --short            # target/, build.log, .idea/ created
                                # (nothing shown: all matched by .gitignore)
$ echo 'real change' >> app.txt
$ git status --short            # a TRACKED file is still visible
 M app.txt
$ git rm --cached app.txt       # explicit untrack, file stays on disk
rm 'app.txt'
$ git status --short
D  app.txt
?? app.txt
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): ignored patterns vanish from status, tracked files do not — and untracking is a separate, explicit act that stages a deletion.

## Why ignore files must be committed

`.gitignore` lives in the repo itself so the whole team ignores the same things; it is part of the project contract, alongside the build configuration that defines what *is* generated. Repository-level ignores can be complemented by `.git/info/exclude` (personal, not committed) and a global ignore file configured via `core.excludesFile` (machine-wide, typically `.DS_Store`, editor swap files). Whether to commit `build.log` is never a question — but *what to do with intentional, versioned generated artifacts* (like lock files) is a team decision, not an ignore decision. The ignore list also interacts with the three-area flow: ignored files never enter [[What are the working directory the staging area and the repository in Git]]'s staging conversation, and never become objects — [[How does Git store data internally]] has content stored only once it is committed.

> [!warning] Ignoring does not hide secrets that were already committed
> Adding `application-local.properties` to `.gitignore` after it was once committed does nothing — the file stays tracked, and even a proper untrack leaves the old blob in history where anyone can read it. The safe order is: ignore first, then create. If a credential did land in history, ignore the file *and* rotate the secret *and* rewrite history ([[Why should you not rewrite history of shared branches]] explains the cost). Cache/debugging inversions have their own trap: `git check-ignore -v <path>` tells you exactly which rule matched — the first tool to reach for when Git ignores something you wanted tracked.

```d2
direction: right
file: "New file appears\nin worktree" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
ig: ".gitignore matches?" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
skip: "invisible to status,\nnever suggested for add" {
  width: 280
  height: 100
  style.fill: "#ffebee"
}
vis: "normal workflow:\nstatus / add / commit" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
tracked: "already tracked?\nignore rules do not apply" {
  width: 280
  height: 100
  style.fill: "#f3e5f5"
}
file -> ig
ig -> skip: "yes"
ig -> vis: "no"
file -> tracked: "yes"
tracked -> vis
```

**Fig. 1.** Ignore rules are a filter for *untracked* files only; tracked files flow through the normal add/commit cycle regardless of patterns.

> [!tip] Interview answer
> **.gitignore lists glob patterns for files Git should not track — build output, dependencies, IDE state, logs, local secrets. It only affects untracked files: once a file is committed, ignoring it changes nothing, and untracking requires rm --cached while the old content stays in history. The file is committed itself so the whole team shares it; check-ignore -v explains which rule hides a given path.**

