<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# What Git branching strategies do you know

> [!abstract] Short answer
> Four models cover every real team. **Git Flow** — long-lived `main` + `develop`, plus `feature/*`, `release/*`, `hotfix/*` branches: heavyweight, suits versioned releases shipped on a cadence. **GitHub Flow** — one long-lived `main`, everything else is a short feature branch merged via PR after CI: the web-deployment default. **GitLab Flow** — GitHub Flow plus *environment* branches (`staging`, `production`) or release branches that cherry-pick fixes. **Trunk-based development** — everyone commits to one trunk constantly behind flags, branches live minutes-to-hours: the CI/CD and continuous-deployment optimum. The pick follows release cadence and deployment risk, not fashion.

## The models in one view

```d2
direction: right
gf: "Git Flow\nmain + develop + feature/release/hotfix" {
  width: 380
  height: 110
  style.fill: "#ffebee"
}
gh: "GitHub Flow\nmain + short-lived PR branches" {
  width: 360
  height: 110
  style.fill: "#e8f5e9"
}
gl: "GitLab Flow\nGitHub Flow + environment branches" {
  width: 380
  height: 110
  style.fill: "#fff3e0"
}
tb: "Trunk-based\none trunk, tiny branches, flags" {
  width: 380
  height: 110
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Complexity decreases left to right; deployment frequency usually increases the same way. [[What are Git branches for]] explains the mechanism each model merely names.

- **Git Flow** — two protected lines (`main` holds only tagged releases — [[What is a tag in Git and how does it differ from a branch]]; `develop` is the integration line), features branch from `develop`, `release/*` freezes a version, `hotfix/*` cuts from `main` and merges back to *both*. Powerful for shrink-wrapped/cadence-released products with multiple maintained versions; the cost is ceremony — merges everywhere, `develop` drift, and a model that fights continuous deployment by design.
- **GitHub Flow** — branch off `main`, commit, open a PR, CI green + review, merge, deploy. One rule: `main` is always deployable. Perfect when deployment is continuous and per-commit; weak when you need *staged* releases (what is deployed ≠ what is in main).
- **GitLab Flow** — keeps GitHub Flow's simplicity and adds the missing piece: **environment branches** (`production` moves only by merging from main — deployment = branch merge, visible in Git) or **release branches** for maintained versions where fixes travel by cherry-pick ([[What is git cherry-pick and when do you use it]]).
- **Trunk-based** — no long-lived branches at all: trunk (`main`/trunk) integrated constantly, incomplete features hidden behind **feature flags**, releases cut by tags. Requires CI discipline and flag hygiene; eliminates merge hell structurally. [[How does trunk based development differ from long lived feature branches]] is the dedicated comparison card.

## The decision dimensions

Ask (and answer at interview): **release cadence** — continuous (GitHub/trunk) vs versioned on schedule (GitLab/Git Flow); **supported versions** — how many old releases carry fixes (more versions → release branches → cherry-pick flow); **team size and coupling** — trunk-based scales with CI investment, Git Flow survives weak integration discipline; **deployment automation** — if deploys are manual and risky, long-lived environment branches map reality; if deploys are automated, they only add ceremony.

> [!warning] The strategy is a *policy*, not a Git feature — and mixed models rot
> Git works identically under all of them; the strategy lives in protection rules, PR templates and CI gates ([[Why should you not rewrite history of shared branches]] — policy enforced at the platform). The failure modes are all hybrids: a "GitHub Flow" where `release/*` branches linger for months, a trunk-based team without flag discipline (dark launches become live launches), Git Flow whose `develop` quietly stops tracking `main`'s hotfixes. Whatever the model, *long-lived branches are the common failure point* — the answer to "which strategy" is credible only together with "how long do branches live here".

> [!tip] Interview answer
> **The four to name: Git Flow — main plus develop with feature, release and hotfix branches, for versioned, cadence-released products; GitHub Flow — one deployable main, short PR branches, for continuous deployment; GitLab Flow — GitHub Flow plus environment or release branches so deployments and maintained versions are visible in Git; trunk-based — everyone integrates to one trunk behind feature flags, branches living hours, for mature CI/CD. I pick by release cadence, number of maintained versions and CI maturity — and I keep any model honest by measuring branch age, since long-lived branches are where every strategy fails.**

