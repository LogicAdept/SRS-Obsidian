<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What are Git branches for

> [!abstract] Short answer
> Branches let you take the project in **several directions at once without mixing the work**: a feature branch isolates incomplete changes from the deployable main line, a release branch stabilizes what ships while development continues, a hotfix branch patches production without carrying half-finished features. Because a branch is a free pointer ([[How would you explain what a Git branch is]]), the cost is zero and the benefit is that *every change becomes a reviewable, testable, revertible unit*.

## The jobs branches do

**Isolation.** Work-in-progress on `feature/order-validation` never breaks what CI tests on `main`. Half-implemented refactors, experimental libraries, debugging commits — all live on the branch until they are ready. Integration happens deliberately through [[How would you explain the Git merge command]], not accidentally through your working tree.

**Review units.** A short-lived branch maps to one pull request: one purpose, reviewable size, revertible as a whole. Long-lived branches lose this property — they drift from main and become integration nightmares, which is exactly why trunk-based development prefers tiny, short-lived branches ([[How does trunk based development differ from long lived feature branches]]).

**Release and hotfix lanes.** Release branches (`release/2.1`) freeze what ships and take only stabilization fixes; hotfix branches (`hotfix/2.1.1`) cut from a production tag ([[What is a tag in Git and how does it differ from a branch]]) and patch the deployed version without shipping current development. Full layout in [[What Git branching strategies do you know]].

**Experimentation and collaboration.** Spikes (`try/kafka-vs-rabbit`) are made to be deleted; per-developer branches let two people review each other's work before it touches main. Nothing here costs disk or setup — deleting the branch is the experiment's full cleanup.

```text
$ git log --oneline --graph --all
* a007554 Main: add OrderRepository      <- main (always green)
| * 8efdc49 Feature: add OrderValidator  <- feature (in progress, isolated)
|/
* dbe5cb2 Base: OrderService skeleton
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): the essential picture — main holds only complete work; the feature tip is unreachable by CI on main until merged.

> [!warning] Branches isolate *history*, not runtime resources
> Switching branches swaps tracked files in the working tree, but: uncommitted changes ride along (or block the switch by conflict); ignored files like local databases, `.env`, and logs do not change at all; Docker volumes, running services and DB schemas are untouched by Git. A "feature branch" of code that needs a new DB column can still crash locally against the old schema. Teams pair branches with migrations and feature flags precisely because a branch alone does not isolate *behavior* — and stale branches that skip migrations turn integration into archaeology.

```d2
direction: down
main: "main\nreachable, tested, deployable" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
f1: "feature/order-validation\nisolated WIP -> PR when ready" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
rel: "release/2.1\nstabilization only" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
hf: "hotfix/2.1.1\ncut from tag, patch prod" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
f1 -> main: "merge after review"
rel -> main: "branch off"
hf -> main: "merge both ways"
```

**Fig. 1.** Typical named lanes around the main line. Each has a distinct lifecycle; all are the same cheap mechanism underneath.

> [!tip] Interview answer
> **Branches exist to isolate lines of work: incomplete features stay away from the deployable main line, releases freeze on their own branch, hotfixes patch production from a tag, and every branch doubles as a reviewable, revertible pull request. The pointer mechanism makes them free, so the discipline is to keep them short-lived and single-purpose — long-lived branches drift and turn merging into the bottleneck, which is what trunk-based development optimizes away.**

