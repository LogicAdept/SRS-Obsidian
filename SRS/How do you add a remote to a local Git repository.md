<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How do you add a remote to a local Git repository

> [!abstract] Short answer
> `git remote add origin <url>` connects an existing local repository to a remote (the conventional name `origin`); `git remote -v` lists the configured fetch/push URLs, and `git push -u origin main` publishes the branch *and* wires up tracking so future `push`/`pull` work without arguments. A local path or file URL works as a remote too — useful for testing. The reverse setup exists as well: `git clone` creates the local repo *with* `origin` already configured.

## Wiring a local repo to a remote, verbatim

```text
$ git remote add origin ../origin.git
$ git remote -v
origin	../origin.git (fetch)
origin	../origin.git (push)
$ git remote -v                 # after clone instead: pre-configured
origin	/home/z/dev/shared.git (fetch)
origin	/home/z/dev/shared.git (push)
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim, abridged): remotes are just named URL pairs in the local config — [[What are the levels of git config]] shows where they live. Cloning wired `origin` automatically; `remote add` does the equivalent for a repo born with `init`.

The full bootstrap of a local project: create the (empty) repo on the hosting, then locally `git remote add origin <url> && git push -u origin main`. The `-u` (`--set-upstream`) matters — it records `origin/main` as the branch's upstream so subsequent `git push`/`git pull` need no arguments and `git status -sb` can report ahead/behind ([[How do you download changes from a remote Git repository]] uses that). Managing remotes over time: `remote set-url origin <new-url>` (renamed or moved host — the HTTPS↔SSH switch), `remote rename` (relabel `origin` to something meaningful in multi-remote setups), `remote remove`, and `fetch --prune` to drop remote-tracking refs of deleted branches.

## Multiple remotes are normal in backend work

A fork-based workflow has `origin` (your fork) and `upstream` (the real project): fetch from upstream, push to origin, PR between them ([[What is the difference between clone fork and branch]]). Deploy pipelines add a second remote (e.g. a Heroku/ops remote). Mirrors keep a backup copy — `git remote add backup <url>` plus a push mirror config. In all cases remember: remotes are *names in local config* — nothing about them is pushed or shared; every teammate wires their own.

> [!warning] The URL protocol decides authentication — and a wrong push target is a silent foot-gun
> HTTPS remotes use tokens/passwords (CI-friendly, per-host credential helpers), SSH remotes use keys (developer-friendly, audited by key, not by token scope); switching an existing remote means `set-url`, and cached credentials for the old URL keep working — stale permissions included. Two classic traps: pushing to a remote whose branch differs from yours because you *assumed* origin (`git push` without `-u` on an untracked branch refuses with advice — read it); and `remote add` when a remote with that name exists — it errors, `set-url` is the update verb. Nothing validates the URL at add time: a typo surfaces only on the first fetch/push.

```d2
direction: right
local: "Local repo\nno remote configured" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
add: "remote add origin <url>\nname -> URL pair in config" {
  width: 340
  height: 110
  style.fill: "#fff3e0"
}
push: "push -u origin main\npublish + set upstream" {
  width: 330
  height: 110
  style.fill: "#e8f5e9"
}
rem: "origin\nshared hub" {
  width: 240
  height: 100
  style.fill: "#f3e5f5"
}
local -> add
add -> push
push -> rem
```

**Fig. 1.** Adding a remote only records a name-URL pair; the repository becomes *connected* at the first successful fetch/push, and *convenient* after `-u` sets tracking.

> [!tip] Interview answer
> **git remote add origin <url> records the remote under a name — origin by convention — remote -v shows the fetch/push URLs, and push -u origin main publishes the branch while setting up tracking so bare push and pull work afterwards. Clone wires origin automatically, set-url handles moved hosts or protocol switches, and fork workflows add a second remote named upstream. Remotes live only in local config; nothing about them is shared, and a wrong URL surfaces at first fetch, not at add.**

