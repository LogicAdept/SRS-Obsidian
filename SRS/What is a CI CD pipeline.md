<!--
reps: 0
priority: 0
-->
#DevOps/CICD #SRS

# What is a CI CD pipeline

> [!abstract] Short answer
> A **CI/CD pipeline** is the configured, automated sequence of stages that takes a commit from version control to a released artifact: checkout → build → test → package → publish to a registry → deploy to staging → approval → production. Each push, merge request, or schedule triggers a fresh run, and the pipeline's green/red status is what makes "main is releasable" an auditable fact rather than a hope.

A pipeline is the operational spine of [[What is CI]] and the delivery part of [[What is continuous delivery]]. Structurally, tools converge on the same shape. In GitLab, a `.gitlab-ci.yml` file declares **jobs** (units of work executed by runners) grouped into **stages**; stages run in sequence, jobs within a stage run in parallel, and if any job in a stage fails, the pipeline stops early. In Jenkins, the same model lives in a `Jenkinsfile` with `pipeline { agent, stages }` — [[What is a Jenkins Pipeline]] covers that tool's vocabulary. The essential economic rule is **build once, promote everywhere**: the artifact produced by the build stage (a JAR, a container image) is the *same* object that reaches production, identified by an immutable digest, not rebuilt per environment.

```d2
direction: right
push: "git push / MR\n(schedule or manual)" {
  width: 240
  height: 100
  style.fill: "#e3f2fd"
}
build: "Build\ncompile + unit tests" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
pkg: "Package + publish\nimage to registry" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
staging: "Deploy staging\nsmoke + integration" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
gate: "Approval gate" {
  width: 220
  height: 80
  style.fill: "#f3e5f5"
}
prod: "Deploy production\npromoted artifact" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
push -> build -> pkg -> staging -> gate -> prod
```

**Fig. 1.** A canonical pipeline: one artifact flows left to right; environments change, the bytes do not.

## Where it runs and what triggers it

Jobs execute on **runners** (GitLab) or **agents** (Jenkins) — machines or containers registered with the CI server. Triggers are declarative: pushes to branches, merge requests, tags, schedules (nightly regression), or manual runs with parameters. Because each run is bound to a commit id, a failed stage is diagnosable by checkout of that exact commit — this audit trail is what separates a pipeline from a build script someone runs on a laptop.

```yaml
# Conceptual GitLab pipeline
stages: [build, test, publish, deploy]
build:
  stage: build
  script: ["./gradlew assemble"]
test:
  stage: test
  script: ["./gradlew check"]
publish:
  stage: publish
  script: ["docker push registry/app:$CI_COMMIT_SHA"]
deploy-staging:
  stage: deploy
  script: ["kubectl set image ..."]
  environment: staging
```

**Listing 1.** The four canonical stages in GitLab YAML; the same SHA flows from publish to deploy.

> [!warning] Popular misconceptions
> "Pipeline" is not a synonym for the CI server — it is the *definition* of the path, executed by runners; the server is replaceable. The second expensive mistake is rebuilding the artifact for each environment: anything rebuilt can differ, so verification in staging proves nothing about production. The third is a linear pipeline with all tests at the end — feedback arrives when the developer has context-switched away; cheap checks belong at the front ([[How do you structure a CI CD pipeline]] covers the ordering discipline).

> [!tip] Interview answer
> **A CI/CD pipeline is the automated path from commit to release: checkout, build, test, package, publish, deploy to staging, approval, production. Stages run sequentially and jobs inside a stage in parallel; a failure stops the run early. The core invariants: one immutable artifact promoted through environments, every run bound to a commit, and green status gating merges and deploys. GitLab expresses it in .gitlab-ci.yml, Jenkins in a Jenkinsfile — the model is the same.**
