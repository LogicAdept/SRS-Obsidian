<!--
reps: 0
priority: 0
-->
#DevOps/VCS #SystemDesign/Tradeoffs #SRS

# What is the difference between a monorepo and a multirepo

> [!abstract] Short answer
> A monorepo holds all projects in one version-control repository; a multirepo gives each project (or service, or team) its own repository. The tradeoff is global visibility and atomic cross-project change (monorepo) versus per-project autonomy, access isolation and small tooling footprint (multirepo). Google's codebase — the canonical monorepo — justifies it as a common source of truth for tens of thousands of developers, enabled by custom-built tooling; most organizations choose one style per stage of scale, and hybrids are common.

## What each model buys

Monorepo advantages: atomic changes across projects (a protocol change and all its consumers land in one commit — no cross-repo synchronization dance); one source of truth with universal visibility (anyone can read, reuse, and review any code; no "lost" forks); unified tooling, CI configuration and dependency versions (one build system sees the whole dependency graph); and large-scale refactoring becomes mechanical — rename an API, fix every caller in the same change. The costs are tooling and scale: VCS and CI must handle huge histories and wide checkouts (Google literally built its own VCS and tooling for this — the research writeup describes the custom-built monolithic repository and the systems that make it feasible); access control is coarser (everything readable unless tooling adds per-path ACLs); builds need aggressive caching and change detection or every commit builds everything; and the repo becomes an organizational choke point without investment. Multirepo advantages: per-team autonomy (own workflow, releases, access), small fast clones and CI scopes, natural access boundaries, and clean version boundaries (libraries version explicitly). Its costs mirror: cross-repo changes are choreographed commits; dependency drift and version skew accumulate; code sharing decays into copy-paste or versioned-package overhead; and "who has the current truth?" becomes a real question across dozens of repos.

```text
monorepo:  atomic cross-project change, one truth, unified CI
           costs: tooling at scale, coarse ACLs, build choreography
multirepo: autonomy, access isolation, small CI scopes
           costs: version skew, choreographed cross-repo changes,
                  slower reuse, drift between repos
decision driver: org scale + how often projects change together
```

**Listing 1.** The tradeoff ledger and the deciding question.

## Choosing and the hybrid reality

The decision follows organizational scale and coupling: many small teams owning loosely-coupled services with stable interfaces fit multirepo; tightly-coupled projects changing together, a strong platform-engineering function, and a reuse-heavy codebase fit monorepo. Company scale pushes monorepo only with tooling investment (build caching, affected-target computation, code owners, path ACLs) — adopting a monorepo without that investment yields the costs without the atomicity. Both models ride on the same VCS mechanics ([[What are version control systems for]]), and per-repo access boundaries — the multirepo's isolation argument — can also be expressed inside one platform by fork layouts ([[What is the difference between clone fork and branch]]), which is why large organizations often debate tooling, not Git. The hybrids cover most real enterprises: a monorepo per domain plus multirepo for shared libraries published as versioned packages; vendor/opensource code kept separate; and the CI discipline ([[What is the difference between a monorepo and a multirepo]]-adjacent [[What is the difference between a stateful service and a stateless service]]-style independence of deployables) keeping either model honest — the repo layout is a coordination choice, and the deployment units remain independently shippable either way. [[How do you design a system against vendor lock-in]]'s portability lens applies to tooling choice as well: monorepo tooling is often bespoke and itself a dependency.

> [!warning] A monorepo without build intelligence is a slowdown machine
> If every commit triggers full builds of every project because the tooling cannot compute affected targets, the monorepo tax is paid on every change and the atomicity benefit never materializes. The model requires the tooling investment upfront, not after the pain.

> [!tip] Interview answer
> Monorepo = all projects in one repo: atomic cross-project changes, universal visibility, unified tooling — paid in build/CMS scale engineering and coarse access control. Multirepo = per-project repos: autonomy and isolation, paid in version skew and choreographed cross-repo changes. I choose by scale and coupling, and hybrid layouts are the enterprise norm.
