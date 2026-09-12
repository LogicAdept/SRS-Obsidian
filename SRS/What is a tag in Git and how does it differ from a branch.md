<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What is a tag in Git and how does it differ from a branch

> [!abstract] Short answer
> Both a tag and a branch are just a **name pointing to a commit** — the difference is intent and mutability. A **branch** is a moving pointer that advances with every commit; it is how you organize ongoing work. A **tag** is a name for a *fixed point* you promise not to move — releases, milestones. Git enforces neither promise technically (a tag *can* be deleted or moved), but two tag types exist: **lightweight** (a bare ref to a commit) and **annotated** (its own object with tagger, date, and message, and signable).

## Types and the real objects behind them

```text
$ git tag v1.0                       # lightweight
$ git tag -a v2.0 -m "Release 2.0 with API freeze"
$ git cat-file -t v1.0
commit
$ git cat-file -t v2.0
tag
$ git cat-file -p v2.0
object 2b5a507b57746f43e7e95340d983b9b182b76fb2
type commit
tag v2.0
tagger SRS Demo <srs-demo@example.com> 1788254400 +0000

Release 2.0 with API freeze
$ git show v2.0 --stat --no-patch
tag v2.0
Tagger: SRS Demo <srs-demo@example.com>
Date:   Tue Sep 1 09:20:00 2026 +0000

    Release 2.0 with API freeze
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): a lightweight tag *is* the commit it names; an annotated tag is a separate object that points at one — with its own author and message, so the release record survives independent of who asks.

Practical rules of thumb:

- **Releases → annotated tags.** They carry the release metadata, are what `git describe` uses to build version strings, and can be GPG-signed so a build can *prove* which commit shipped.
- **Temporary/local markers → lightweight.** A quick "this worked here" pointer costs nothing.
- **Branches are never tags.** If a name is expected to move with development, it is a branch ([[What are Git branches for]]); if the name must stay put, tag it. Semantic versioning on releases maps naturally: `v2.0.0`, `v2.0.1`, …
- **Tags are not pushed by default**: `git push --follow-tags` (annotated only) or `git push origin v2.0` explicitly. Teams that release from CI pass the tag into the pipeline trigger.

## What tags are used for in a Java backend world

Release engineering is the core: CI builds an artifact *from a tag*, so "what is running in prod" has a Git answer. Docker image labels, Maven release versions and Helm chart versions are commonly derived from `git describe --tags` output. Hotfix workflows branch *from a tag* (`git checkout -b hotfix v2.0.1`) — [[What Git branching strategies do you know]] shows where that fits in release branching models. Tags also anchor bisect ranges: you can bisect from `v2.0.0` (good) to `main` (bad) ([[What is git bisect and how do you use it]]).

> [!warning] Tags are only as immutable as your team's discipline — and deletion propagates badly
> Nothing stops `git tag -f v2.0` or `git push --delete origin v2.0`; moving a published tag silently makes one version string mean two different commits — worse than rewriting a feature branch, because *every consumer* trusted it. Some protected hosting setups lock tags (`tagger` verification, branch protection on tag patterns); where they do not, the rule is: a moved tag is an incident. Also remember that fetching tags is not automatic in all flows — a plain `git fetch` can miss new tags, while `git fetch --tags` pulls them all; stale local tags after remote deletion need `git fetch --prune-tags`.

```d2
direction: right
c1: "C1" {
  width: 120
  height: 70
}
c2: "C2" {
  width: 120
  height: 70
}
c3: "C3 (HEAD)" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
b: "branch 'main'\nmoves with every commit" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
t: "tag 'v2.0'\nfixed: release point" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
c1 -> c2 -> c3
b -> c3
t -> c2
```

**Fig. 1.** Same commit graph, two kinds of names: the branch ref rides C3 as history grows; the tag stays pinned to C2 forever.

> [!tip] Interview answer
> **A tag is a named pointer to a fixed commit — a release marker — while a branch is a moving pointer for ongoing work. Lightweight tags are bare refs; annotated tags are separate objects with tagger, date and message, and can be signed, which is why releases use them. Tags are not pushed by default, are only mutable by discipline rather than by Git, and moving a published tag is treated as an incident because builds and provenance keyed on it become meaningless.**

