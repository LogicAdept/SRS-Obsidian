<!--
reps: 0
priority: 0
-->
#Java/Tooling #SRS

# Which build tools for Java do you know

> [!abstract] Short answer
> Three generations: **Ant** (2000s — XML task scripts, no dependency management, full explicitness), **Maven** (2004 — convention over configuration, POM model, central dependency management, standardized lifecycle: `compile → test → package`), **Gradle** (2012 — Groovy/Kotlin DSL, incremental builds, build cache, daemon; the modern Android and Spring Boot default). Historical bits worth knowing: `bat`/shell scripts were the pre-tool reality, and Ant's concepts still leak through Maven plugin names. Today's de-facto choice is Maven for structured enterprises and Gradle where build performance or multi-module flexibility pays.

## What each generation solved

**Shell scripts** — the origin: every project hand-rolled `compile.bat`/`build.sh`; no portability, no dependency handling, no shared conventions. **Ant** made scripts portable XML (`build.xml` with targets depending on targets) but remained *procedural*: you describe every step, dependencies on jars are hand-managed in `lib/`, and two projects share nothing but habits. **Maven** flipped to *declarative conventions*: standard directory layout, a **POM** declaring coordinates (groupId/artifactId/version) and dependencies, a fixed lifecycle where plugins hook standard phases, and — the killer feature — **transitive dependency resolution** from central repositories ([[What are Git submodules and when do you use them]]'s vendored-code era ended here). **Gradle** kept Maven's dependency model but replaced XML with a programmable DSL, added the **build daemon, incremental execution, and build cache** — watch-services make it skip work Maven redoes; Kotlin DSL gives type-safe build scripts for big multi-module builds.

```d2
direction: right
src: "src/main/java\ntest/main/resources\n(convention)" {
  width: 300
  height: 110
  style.fill: "#e3f2fd"
}
pom: "pom.xml / build.gradle\ndependencies + plugins" {
  width: 320
  height: 110
  style.fill: "#fff3e0"
}
life: "Lifecycle\ncompile -> test -> package" {
  width: 320
  height: 110
  style.fill: "#e8f5e9"
}
repo: "Repositories\nMaven Central, Nexus/Artifactory" {
  width: 330
  height: 110
  style.fill: "#f3e5f5"
}
pom -> life: "binds plugins to phases"
life -> repo: "resolves + publishes"
src -> life
```

**Fig. 1.** The Maven/Gradle shared model: conventions + declarative build + managed lifecycle + repository resolution — Ant had none of these four boxes.

Practical Java-backend notes: **dependency scopes** (`compile`, `test`, `provided`) and **BOMs** for version alignment are interview staples; **Spring Boot** ships both Maven and Gradle starters, with Gradle commonly chosen for monorepos and faster rebuilds; **reproducibility** comes from lock-style pinning (Gradle lockfiles, Maven `enforcer` + flattened POMs) and artifacts published to **Nexus/Artifactory** — which is also where CI picks them up ([[Which CI CD tools do you know]]). Multi-module builds: Maven's `parent/aggregator` POMs vs Gradle's composite builds — both solve the "one command for ten modules" problem.

> [!warning] The build tool is also the supply-chain surface — and "version ranges" are a reproducibility bug
> Dependencies resolve from repositories at build time: an unscoped `LATEST`, a version range, or a hijacked plugin (classics: the Apache Struts/Maven-plugin incidents; typosquatting on Central) executes code *on your build box* — pin versions, use BOMs/lockfiles, and gate on dependency-analysis plugins (OWASP dependency-check, Gradle versions plugin). Local builds differing from CI ("works on my machine" at build level) come from daemon/cache state, toolchain drift, or profile activation — CI must run the same toolchain, ideally via wrapper: **always commit the `mvnw`/`gradlew` wrapper**, never require a globally installed tool. And the slow-build trap: Gradle daemon + cache misconfiguration can be *slower* than Maven for small projects — benchmarks before dogma.

> [!tip] Interview answer
> **Ant was procedural XML with no dependency management; Maven introduced convention-over-configuration — standard layout, POM coordinates, a fixed lifecycle with plugin bindings, and transitive dependency resolution from Central; Gradle kept Maven's dependency model but replaced XML with a Groovy/Kotlin DSL and added daemon, incrementality and build cache, which is why it dominates Android and modern Spring Boot. Before tools there were shell scripts. Today I pick Maven for enterprise convention and Gradle where build speed and multi-module flexibility pay — and either way I pin versions, use BOMs, commit the wrapper, and publish artifacts to Nexus or Artifactory.**

