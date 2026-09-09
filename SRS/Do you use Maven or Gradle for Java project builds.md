<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #Java/Tooling/Gradle #SRS

# Do you use Maven or Gradle for Java project builds

> [!abstract] Short answer
> **Both are production-grade; the honest answer is "the team's existing build wins, and I know both."** Maven gives a fixed lifecycle, conventional layout, and XML POM — predictable and instantly familiar. Gradle gives a programmable Kotlin/Groovy DSL, incremental builds, and the daemon — faster and more flexible, at the cost of build logic that can become code you must maintain.

## The real comparison axes

The tools agree on the fundamentals: dependency resolution by Maven coordinates, `src/main/java` + `src/test/java` convention, multi-module builds, repositories. They differ in how the build is expressed and executed.

```d2
direction: right
m: "Maven\nXML POM, fixed lifecycle\npredictable, uniform" {
  width: 290
  height: 100
  style.fill: "#e3f2fd"
}
g: "Gradle\nKotlin/Groovy DSL\nincremental, daemon, cacheable" {
  width: 290
  height: 100
  style.fill: "#fff3e0"
}
mp: "Extra behavior = plugins\nbound to phases" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
gp: "Extra behavior = build logic\nlifecycle is up to you" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
m -> mp
g -> gp
```

**Fig. 1.** Maven trades flexibility for uniformity; Gradle trades uniformity for flexibility.

Where Gradle measurably wins: incremental and cacheable tasks (unchanged inputs skip work), the long-lived daemon, and build-script expressiveness (type-safe Kotlin DSL, `configuration cache`). Where Maven wins: near-zero surprise — any Java developer can read a POM, plugin documentation maps one-to-one to lifecycle phases ([[How would you explain the Maven build lifecycle]]), and the build behaves the same on every machine because there is little build logic to diverge.

> [!warning] Gradle's flexibility is a maintenance cost, not a free lunch
> The trap is answering "Gradle, it's modern" without the cost side. Gradle build scripts are programs: custom tasks and `doLast` blocks can hide behavior that IDEs, CI, and new hires must rediscover, and version mismatches between the wrapper and cache can produce builds that differ per machine. Maven's rigidity bites differently — unusual steps need plugin configuration or a custom plugin, and XML grows verbose. Neither choice is wrong; switching mid-project is the wrong move, since the migration cost dwarfs either tool's deltas. Dependency scoping rules ([[What are the dependency scopes in a Maven pom]]) transfer conceptually between them, and test running is phase/task wiring either way — see [[What is the difference between the Surefire and Failsafe plugins in Maven]].

## How to answer the question

Name the criterion, not the religion: "Greenfield Android or a performance-sensitive multi-module monorepo — Gradle. A team of mixed experience with mostly standard Java modules — Maven is easier to keep consistent. What matters more than the pick: pinned plugin/dependency versions (managed centrally — see [[How would you explain the structure of a Maven pom.xml file]] or Gradle version catalogs), the wrapper in VCS, and reproducible CI." Then actually answer: name what your current project uses and one concrete thing you did in it.

> [!tip] Interview answer
> **I pick by team and project shape. Maven: fixed lifecycle, conventions, verbose but uniform — great for standard Java services and mixed teams. Gradle: programmable DSL, incremental builds and the daemon — faster for large or unconventional builds, but build logic becomes code you maintain. I know both; consistency, pinned versions and a committed wrapper matter more than the tool itself.**

