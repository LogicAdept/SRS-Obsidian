<!--
reps: 0
priority: 0
-->
#DevOps/CICD #SRS

# How do you structure a CI CD pipeline

> [!abstract] Short answer
> Order stages by **cost against feedback value**: lint and unit tests first (fail in minutes), then build and package, then integration tests against containers, then deploy to staging with smoke checks, and only then a production gate. Combine three invariants — **build once and promote the same artifact**, **parallelize independent jobs**, **gate merges on green** — and the pipeline stays fast, auditable, and boring.

The anatomy of a pipeline is [[What is a CI CD pipeline]]; this card is about the design decisions on top of it. The first decision is ordering: a stage that takes seconds must run before a stage that takes half an hour, so a typo fails before expensive work starts. The second is fan-out: independent jobs inside a stage run in parallel — GitLab runs stage jobs concurrently, and its `needs` keyword lets a job start as soon as its actual dependencies finished rather than when the whole previous stage drained. The third is artifact discipline: the build stage produces one artifact (a JAR or a container image pinned by digest), and every later environment promotes that same object — anything rebuilt per environment voids the verification that staging performed.

```d2
direction: down
lint: "Lint + compile\nseconds" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
unit: "Unit tests\nparallel, minutes" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
pkg: "Build + publish artifact\nonce, digest-pinned" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
int: "Integration tests\ncontainers" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
stage1: "Deploy staging\nsmoke suite" {
  width: 280
  height: 80
  style.fill: "#f3e5f5"
}
gate: "Manual gate\nthen production" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
lint -> unit -> pkg -> int -> stage1 -> gate
```

**Fig. 1.** Fast, cheap gates at the top; expensive environment-adjacent checks at the bottom, each stage depending on the verified artifact of the previous one.

## Hygiene that keeps it maintainable

Dependency caching keeps runners from re-downloading the world on every run; secrets live in CI variables or a vault, never in the repository and never echoed into logs; and environments are declared explicitly so a job "knows" what it deploys to. For merge-based flows, merge-request pipelines validate what main would look like — GitLab's merged-results pipelines and merge trains queue MRs as if already merged, which is how the tool enforces green main for [[What Git branching strategies do you know]] based on trunk. A rollback story belongs in the design, not in an incident: every deployable stage needs a documented way back (previous image tag, blue-green flip), or the production gate is theater.

```yaml
# Conceptual: fail-fast ordering + parallel fan-out
stages: [verify, package, deploy]
lint:   { stage: verify, script: ["./gradlew lintKotlin"] }
unit:   { stage: verify, script: ["./gradlew test"] }
license:{ stage: verify, script: ["./gradlew checkLicense"] }  # runs in parallel with unit
package:{ stage: package, script: ["./gradlew build publish"] }
deploy-staging:
  stage: deploy
  needs: ["package"]
  script: ["promote staging"]
  environment: staging
```

**Listing 1.** Three cheap jobs run concurrently in one stage; the deploy job depends only on `package`, not on the whole stage list.

> [!warning] Structure smells
> The mega-job — one giant script doing lint, build, test, deploy — is the most common anti-structure: nothing runs in parallel, logs are unreadable, and a lint typo costs a full re-run including deployment. The silent rebuild is worse: packaging per environment means staging verified a *different* artifact than production receives. And pipelines that leak secrets (echoed variables, debug dumps) turn the CI log archive into a credentials store.

> [!tip] Interview answer
> **I order stages fail-fast: lint and unit tests first, then build once and publish a digest-pinned artifact, integration tests against containers, deploy to staging with a smoke suite, and a production gate last. Independent jobs run in parallel, dependencies are explicit, secrets live in CI variables, and every stage has a rollback. Merge-request or merge-train pipelines keep main provably green. The invariant that matters most: the same artifact is promoted end to end — nothing is rebuilt per environment.**
