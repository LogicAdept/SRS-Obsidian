<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What are Git hooks

> [!abstract] Short answer
> **Git hooks** are executable scripts Git runs automatically at fixed lifecycle points, stored in `.git/hooks/` (sample stubs shipped there; activate by naming the file without `.sample` and making it executable). **Client-side** hooks run in your clone — `pre-commit` (sanity-check the change before the commit is created), `commit-msg` (validate the message), `pre-push` (run tests before uploading); **server-side** hooks run on the receiving repository at `pre-receive`/`update`/`post-receive` — the mechanism behind protected-branch enforcement and deploy automation on self-hosted Git. A hook's non-zero exit code cancels the operation.

## A pre-commit hook blocking a bad commit, verbatim

```text
$ cat .git/hooks/pre-commit
#!/bin/sh
if grep -q 'TODO' app.txt; then
  echo "pre-commit: TODO found, commit blocked" >&2
  exit 1
fi
$ git commit -m "Bad commit"
pre-commit: TODO found, commit blocked
$ sed -i '/TODO/d' app.txt && echo 'clean line' >> app.txt
$ git add app.txt
$ git commit -m "Clean commit"
ain 1c4dacb] Clean commit
 1 file changed, 1 insertion(+)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim, `merge` output line abridged): exit 1 aborts the commit; after the file is fixed, the same hook passes. The hook sees the *staged* content — that is why proper pre-commit scripts read `git diff --cached` or use a staged-files API, not the worktree.

Hook reference worth knowing: client side — `pre-commit` (before the editor/commit object; lint, format check), `prepare-commit-msg` (template messages), `commit-msg` (message policy: ticket id, imperative subject), `post-commit` (notifications), `pre-rebase` (protect shared commits), `pre-push` (last gate: run the test suite before it reaches CI). Server side — `pre-receive` (once per push, all refs; the natural rejection point), `update` (per-ref), `post-receive` (after acceptance: deploy, mirror, chat notifications — the classic self-hosted CD trigger).

## How teams actually use hooks

Directly editing `.git/hooks/` is a *personal* practice — that directory is not versioned. Team-scale hook usage therefore ships hooks with the repo: a `hooks/` directory plus `git config core.hooksPath hooks` ([[What are the levels of git config]] — local config pointing into versioned files), or — the industry default — a **hooks manager** (pre-commit, husky, lefthook) that installs configured hooks per developer from a committed manifest. CI remains the authoritative gate either way ([[What is CI]]); hooks give *earlier* feedback, not stronger guarantees.

> [!warning] Client hooks are advisory — and can silently degrade to nothing
> They can be bypassed (`commit --no-verify`, `--skip` on rebase) and *not installing them* skips them just as well; any rule enforced only by a client hook is a convention, not a control — the enforcement copy belongs server-side or in CI ([[Why should you not rewrite history of shared branches]] explains why platform protection is the real gate). Environment fragility is the second cost: a hook depending on your shell, node version or working directory works "only on laptops like mine" — CI-identical tooling in the hook or a manager solves it. Finally, slow pre-commit hooks train people to use `--no-verify`; keep the fast checks local, push the expensive ones to CI.

```d2
direction: right
git: "git commit / push" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
hook: "hook script\nexit 0 -> proceed\nexit 1 -> abort" {
  width: 320
  height: 120
  style.fill: "#fff3e0"
}
pass: "operation completes\n(commit created / push accepted)" {
  width: 380
  height: 100
  style.fill: "#e8f5e9"
}
fail: "operation refused\nlocally, with hook's message" {
  width: 360
  height: 100
  style.fill: "#ffebee"
}
git -> hook
hook -> pass: "0"
hook -> fail: "non-zero"
```

**Fig. 1.** A hook is a veto point, not a feature: same exit-code contract on both client and server, different blast radius.

> [!tip] Interview answer
> **Git hooks are scripts Git runs at lifecycle points — pre-commit, commit-msg and pre-push on the client; pre-receive, update and post-receive on the server — and a non-zero exit aborts the operation. I use them for fast local feedback: lint and format in pre-commit, message policy in commit-msg, full tests before push; teams distribute them by pointing core.hooksPath at a versioned directory or via a hooks manager. The critical caveat: client hooks are bypassable and optional, so anything that must be enforced lives in server hooks, protected branches or CI — hooks are earlier feedback, not security.**

