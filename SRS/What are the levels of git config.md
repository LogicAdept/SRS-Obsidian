<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What are the levels of git config

> [!abstract] Short answer
> Git configuration lives in three scopes, each overriding the previous one: **system** (`/etc/gitconfig`) for all users of the machine, **global** (`~/.gitconfig`) for you across all repositories, and **local** (`.git/config` inside a repository) for that one repository only. `git config --list --show-origin` shows the effective merged view and which file every value came from. Local wins, so per-repo exceptions (work email, custom hooks path) override global defaults.

## What belongs at each level

**System** — rarely touched by developers: shared editor defaults, credential helper policy, proxies enforced by an admin. On shared CI machines this layer often carries the mirror rewrite rules.

**Global** — your personal defaults: `user.name`/`user.email`, preferred editor, `init.defaultBranch main`, aliases (`git config --global alias.lg "log --oneline --graph --all"`), colors, and credential helpers. If you set your identity only here, every repo you create inherits it — which is exactly what [[How do you make your first Git commit and add all files]] relies on.

**Local** — repository-specific truth: the project's remote URLs, branch tracking setup, per-repo identity, and behavioral switches like `core.hooksPath` or `merge.ff false`. Because local wins over global, the standard trick for separating company and personal work is to override `user.email` locally in each company repo.

```text
$ git config --local --list
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
user.name=SRS Demo
user.email=srs-demo@example.com
commit.gpgsign=false
tag.gpgsign=false
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): the local scope of a scratch repo — identity and signing switches were written here with `git config user.name ...` (no scope flag defaults to local when inside a repo).

```text
$ git config --list --show-origin --show-scope
system  file:/etc/gitconfig	...
global  file:/home/dev/.gitconfig	user.name=Jane Dev
global  file:/home/dev/.gitconfig	init.defaultbranch=main
local   file:.git/config	user.email=jane@company.com
```

**Listing 2.** Shape of the merged view (typical values): scope and origin file are printed before every key. For the *same* key in several files, the last effective line — local — wins.

## Beyond the three classic files

There is a fourth, optional layer: `include.path` / `includeIf.gitdir:...` directives let one global file pull in conditionals — the common pattern is `includeIf "gitdir:~/work/"` pointing at a work identity file, which removes the need for per-repo local overrides. Also note `git config -f <file>` edits an arbitrary config file, which is how tooling writes `.gitmodules` for [[What are Git submodules and when do you use them]].

> [!warning] Environment variables and command-line flags beat config files
> `GIT_AUTHOR_NAME`, `GIT_COMMITTER_DATE` and friends override anything written in any config file, and `-c key=value` on a single command line overrides everything for that one invocation. When debugging "why does Git think my name is X", check the effective view (`git config --list --show-origin --show-scope`) rather than eyeballing files — and remember that an inherited `EMAIL` environment variable can silently supply your identity. Corporate security tools sometimes set `safe.directory` at the system level, which changes *whether* a repo can be touched at all.

```d2
direction: right
sys: "system\n/etc/gitconfig" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
glob: "global\n~/.gitconfig" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
loc: "local\n.git/config" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
env: "env vars / -c flags\n(for one command)" {
  width: 270
  height: 80
  style.fill: "#f3e5f5"
}
sys -> glob: "overridden by"
glob -> loc: "overridden by"
loc -> env: "overridden by"
```

**Fig. 1.** Precedence chain: every layer to the right overrides the layers to its left for the same key.

> [!tip] Interview answer
> **Three file scopes — system, global (~/.gitconfig), and local (.git/config) — with local taking precedence, plus conditionally included configs for work/personal separation. Identity and aliases usually live in global; remotes, tracking and per-repo identity in local. `git config --list --show-origin --show-scope` prints the effective merge, and env vars or `-c` flags temporarily override everything — which is also why a wrong-looking identity should be debugged through that list, not by guessing files.**

