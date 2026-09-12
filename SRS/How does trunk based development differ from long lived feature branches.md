<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How does trunk based development differ from long lived feature branches

> [!abstract] Short answer
> **Trunk-based development**: all developers integrate into one shared trunk (main) at least daily; work-in-progress lives in tiny branches (hours, not weeks) or directly behind **feature flags**; releases are cut by tags from a green trunk. **Long-lived feature branches**: each feature grows in isolation for days-to-months, then integrates in one big, conflict-prone merge — and the longer the branch, the worse the integration scales. The tradeoff is *continuous integration of code* (trunk) versus *isolation before readiness* (branches), with flags buying trunk-based teams the isolation back at the feature level.

## What actually differs day to day

```text
$ git log --oneline --graph --all      # long-lived branch model
* a007554 Main: add OrderRepository
| * 8efdc49 Feature: 3 weeks of work
|/
* dbe5cb2 Base
# merge day: three weeks of drift reconcile at once

$ git log --oneline --graph --all      # trunk-based
* f2c1b9a Add flag-guarded validator skeleton   <- merged today
* 86123b1 Main: add OrderRepository
* 1df7631 Base
# same feature: 4 tiny merges this week, flag off until ready
```

**Listing 1.** git 2.47.3 sandbox (abridged illustration): same feature, two integration rhythms — one large reconciliation versus many trivial merges. Under trunk-based flow, incomplete code ships *dark*: merged but disabled by a flag.

Consequences to articulate at interview:

- **Merge cost profile** — trunk-based makes every merge trivial (minutes of drift); feature-branching concentrates the pain on merge day, and conflicts between *semantic* changes survive clean textual merges ([[How do you merge two divergent Git branches]]' invisible-divergence warning).
- **CI and release coupling** — trunk is continuously green and every commit is a release candidate ([[What is CI]]); long-lived branches produce untestable intermediate states: CI validates the branch *and* the eventual merge, neither of which is the product.
- **Readiness mechanisms** — trunk-based teams need the alternatives branches provided: **feature flags** (toggle at runtime, kill-switch included), **branch by abstraction** (merge through an internal interface while implementations differ), release **tags** not release branches ([[What is a tag in Git and how does it differ from a branch]]). Without this machinery, trunk-based development is just broken main.
- **Review cadence** — feature-branch PRs review a big batch late; trunk reviews many small PRs early — better signal, more interruptions; pair programming and very small PRs replace "review the month".

## Where each model wins

Trunk-based fits continuous deployment, strong automated testing, flags infrastructure, and teams sharing ownership of one product (the model behind modern CI/CD lore — Google, Facebook scale stories). Long-lived branches fit regulated or versioned deliveries, low deployment frequency, code you cannot flag (config/data migrations, licensed third parties), or teams without shared ownership — where *isolation is the risk control*, not an accident. Most real organizations are hybrids: trunk for the product, versioned branches for maintained releases ([[What Git branching strategies do you know]]'s GitLab Flow lane).

> [!warning] Trunk-based without discipline is broken main; feature-branching without discipline is merge hell — and half-done features are visible either way
> If flags leak (never removed), the trunk accretes dead toggles; if "integrate daily" slips, you quietly become feature-branching with extra steps. The reverse failure: long-lived branches that *never* merge are lost work, and three-week branches make reverts and code archaeology costly — the branch's squashed PR becomes the only history ([[What kinds of Git branch merges exist]]'s squash caveat). A measurable health metric for either model: **time from commit to production** and **branch age** — long branches with fast deploys is the contradiction to call out in interview answers.

```d2
direction: right
tb: {
  trunk: "trunk (main)\nalways releasable" {
    width: 300
    height: 90
    style.fill: "#e8f5e9"
  }
  tiny: "tiny branches\nhours, flag-guarded merges" {
    width: 320
    height: 90
    style.fill: "#e3f2fd"
  }
  tiny -> trunk: "daily"
}
lb: {
  lb1: "main" {
    width: 160
    height: 80
    style.fill: "#e8f5e9"
  }
  lb2: "feature branch\nweeks of isolation" {
    width: 320
    height: 90
    style.fill: "#ffebee"
  }
  lb2 -> lb1: "one big merge, late"
}
```

**Fig. 1.** Two rhythms of integration: many small crossings (top) versus one cliff (bottom) — the drift under the cliff grows with branch age.

> [!tip] Interview answer
> **Trunk-based development integrates everyone into one main at least daily — tiny branches or direct commits, incomplete features behind flags, releases cut by tag from green trunk. Long-lived feature branches isolate each feature for weeks and integrate once, late and painfully, with semantic conflicts that survived clean textual merges. Trunk-based trades that risk for machinery: flags, branch-by-abstraction, strong CI — and wins time-to-production; long-lived branches still fit versioned, low-frequency releases where isolation is the risk control. The honest metric is branch age and commit-to-production time.**

