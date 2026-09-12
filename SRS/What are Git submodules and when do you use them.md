<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What are Git submodules and when do you use them

> [!abstract] Short answer
> A **submodule** embeds one Git repository inside another as a pinned reference: the parent stores the child's *exact commit id* as a special `gitlink` entry (mode 160000) plus the child's URL in `.gitmodules`. The parent does **not** contain the child's code — it contains "repo X at commit Y". Use them to vendor third-party or shared libraries at auditable versions, to share code between products while keeping separate histories, or to split a monolith's *build* before splitting its *code*. The tradeoff is real operational friction: submodules are a state you must actively sync, not files you just edit.

## The mechanics, verbatim

```text
$ git submodule add ../libx libx
Cloning into '…/subm/libx'...
$ git ls-tree HEAD libx              # what the PARENT stores
160000 commit 43f6b1be6d990ee5548f06f3aa1126200fe7d629	libx
$ git submodule status
 43f6b1be6d990ee5548f06f3aa1126200fe7d629 libx (heads/main)
$ git config -f .gitmodules --list
submodule.libx.path=libx
submodule.libx.url=../libx
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): the parent commits a `gitlink` — mode 160000, the pinned SHA — and `.gitmodules` (url + path). The child's history lives entirely in its own repository.

Operational model worth memorizing:

- **Clone a parent**: `git clone … && git submodule update --init --recursive` — without the second command the submodule directories are empty (the classic CI failure). `git clone --recurse-submodules` does it in one step.
- **Bump a submodule**: `cd libx && git fetch && git checkout <new-sha> && cd .. && git add libx && git commit` — the parent records the new pin; *nothing else changes*.
- **Consume updates**: teammates run `git submodule update --recursive` after pulling; the check for "did I forget" is `git submodule status` (a `+` prefix means checked-out commit ≠ recorded pin).
- **Editing inside a submodule** happens on its own HEAD — typically detached ([[What is HEAD and what is a detached HEAD]]), by design: the parent pins *commits*, not branches.

## When they earn their friction — and the alternatives

Legitimate: vendoring a dependency you must **audit and patch in place** (security-critical forks); sharing a spec/proto library across independent services where *build reproducibility at a pinned commit* beats convenience; breaking a giant repo into nested builds *before* deciding ownership boundaries. In most other cases modern tooling wins: **Maven/Gradle dependencies** for Java libraries ([[Which build tools for Java do you know]]) — versioned, cached, transitive; **package managers + lock files** for the same guarantee with better ergonomics; **monorepo tooling** when the real problem is atomic cross-project change ([[What is the difference between a monorepo and a multirepo]] covers that tradeoff directly).

> [!warning] The classic submodule incidents are all "state forgotten"
> Committing the parent *without* committing the submodule's own change first records a stale pin; CI builds break because `update --init` was skipped; everyone "fixes" it by committing a bump — three branches, three pins, confusion. `submodule update` silently *detaches and can discard* local work in the submodule (it checks out the recorded pin — commit or branch inside first). Security note: `.gitmodules` URLs are attacker-controllable input in cloned repos (CVE-2024-32002 class issues led to stricter defaults, e.g. file-transport restrictions — hence `-c protocol.file.allow=always` for local demos); treat submodule URLs like dependencies, not configuration.

```d2
direction: right
parent: "Parent repo\nlibx -> gitlink 43f6b1b\n.gitmodules -> url" {
  width: 320
  height: 110
  style.fill: "#e3f2fd"
}
child: "libx repo\nfull history, own HEAD" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
sync: "update --init --recursive\n(checkout recorded pin)" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
bump: "checkout new sha + commit\nin parent = new pin" {
  width: 330
  height: 100
  style.fill: "#f3e5f5"
}
parent -> child: "points at one commit"
child -> sync: "clone into place"
sync -> bump: "lifecycle"
```

**Fig. 1.** The parent stores a pointer, the child owns its history; two sync commands (init-on-clone, update-on-pull) and one bump flow are the whole operational surface.

> [!tip] Interview answer
> **A submodule embeds another repository by reference: the parent records the child's exact commit as a gitlink plus its URL in .gitmodules — it never contains the child's code. They fit vendoring and auditing third-party code, sharing a pinned library across products, and staged repo splits; otherwise dependency managers with lock files are usually saner. The operational costs are the forgotten ones — update --init on clone, update after pull, committing the bump explicitly — and detached HEADs inside submodules are normal, since the parent pins commits, not branches.**

