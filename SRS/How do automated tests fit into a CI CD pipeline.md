<!--
reps: 0
priority: 0
-->
#DevOps/CICD #Testing #SRS

# How do automated tests fit into a CI CD pipeline

> [!abstract] Short answer
> Tests are layered along the pipeline by cost and speed: **unit tests on every push** as the first gate, **integration tests** after packaging (often against containerized dependencies), **smoke tests after every deployment** to an environment, and the **full regression suite nightly or on merge requests**. Each layer answers a different question, and putting a layer in the wrong place either blocks feedback or lets bugs through.

The placement logic is "fail fast where it is cheap". Unit tests run in the earliest stage — they take seconds, so a red build reports within minutes of the push ([[What is CI]] describes why this feedback loop is the practice's whole point). After the artifact is packaged, integration tests run against real dependencies spun up in containers. After each deployment — staging and production alike — a small **smoke suite** (typically five to ten critical-path cases) verifies the deployment actually works, complementing container-level probes ([[How do Docker health checks work]] covers the runtime version of the same idea). The heavy **regression suite** runs on merge requests and on a nightly schedule, producing a report — Jenkins publishes JUnit XML, and aggregate HTML reports such as Allure turn raw failures into diagnosable pages.

```yaml
# Conceptual: test layers as pipeline stages
stages: [unit, package, itest, deploy, smoke]
unit:
  stage: unit
  script: ["./gradlew test"]          # every push, seconds
itest:
  stage: itest
  script: ["./gradlew integrationTest"]  # containers via Testcontainers
smoke:
  stage: smoke
  script: ["./gradlew smokeTest -Denv=staging"]  # after each deploy
nightly-regression:
  script: ["./gradlew regression alluredPublish"]
  rules: [{ if: "$CI_PIPELINE_SOURCE == 'schedule'" }]
```

**Listing 1.** The same suite taxonomy expressed as GitLab stages: cheap gates first, full regression on schedule.

## When a test fails in CI but passes locally

The classic follow-up. The divergence lives in the environment: differences in database state or version, externalized configuration, timezone or locale, parallel execution exposing a **race condition**, or timeouts tuned too tightly for shared runners. The debugging order is: read the CI logs (not the local re-run), diff the environment (versions, env variables, data), then reproduce with the CI's own command line. A test that fails only in CI is *information*, not noise — it found a real portability or concurrency defect more often than not.

> [!warning] Flaky red trains the team to ignore red
> A pipeline with habitual flaky failures loses its function within weeks: people merge on red, and the gate is gone. The professional responses are quarantine (move the test out of the blocking path, file a ticket, fix or delete), retrying *only* at the infrastructure level with explicit reporting, and keeping unit suites fast and deterministic. Equally damaging is the opposite lie — "tests run in CI, so we do not need them locally": the local pre-commit loop is where most defects should die, and CI is the audit layer, not the first line of defense.

> [!tip] Interview answer
> **Tests are distributed by cost: unit tests gate every push, integration tests run against containerized dependencies after packaging, smoke tests verify every deployment, and the full regression suite runs on merge requests or nightly with published reports. A CI-only failure is diagnosed through logs and environment diffs — versions, data, timing, race conditions. The main hazard is flakiness: habitual red normalizes merging unverified code, so flaky tests are quarantined and fixed rather than retried blindly.**
