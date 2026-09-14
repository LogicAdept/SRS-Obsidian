<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# Which core plugins does Maven ship with

> [!abstract] Short answer
> **The core set mirrors the default lifecycle: clean, compiler, resources, surefire, failsafe, jar (plus other packaging plugins), install, deploy, and site.** Around them the same Apache group ships tooling plugins — dependency, enforcer, verifier, archetype, release, help — and reporting plugins that run under the site lifecycle.

Maven's official catalog groups its own plugins in three buckets. **Core plugins** correspond to default build phases: `clean` removes the build output, `compiler` compiles main and test sources, `resources` copies resources into the output directory, `surefire` runs unit tests, `failsafe` runs integration tests ([[What is the difference between the Surefire and Failsafe plugins in Maven]] compares them), `install` puts the artifact into the local repository, `deploy` pushes it to a remote one, and `site` generates the project site ([[How would you explain the Maven build lifecycle]] maps these to phases).

## Packaging plugins and the tooling set

Packaging plugins produce artifacts: `jar`, `war`, `ear`, `ejb`, `rar`, `shade` (uber-JAR — [[What is the difference between the maven-shade-plugin and the maven-assembly-plugin]]), `source` (sources JAR), plus `jlink`/`jmod` for runtime images. The tooling plugins are invoked mostly by goal rather than by phase: `dependency` analyzes and manipulates the dependency tree ([[What does the maven-dependency-plugin do]]), `enforcer` enforces environment constraints (Maven version, JDK version, custom rules), `verifier` checks files' presence/contents, `archetype` scaffolds new projects from templates ([[What is a Maven archetype]]), `release` automates release branches and version bumps, `help` exposes goals like `help:effective-pom`. The super POM also pre-pins versions for a few of them (antrun, assembly, dependency, release) so a bare `mvn dependency:tree` works without declaring anything.

```d2
direction: right
core: "Core: bound to phases\nclean · compiler · resources\nsurefire · failsafe · install\ndeploy · site" {
  width: 300
  height: 150
  style.fill: "#e3f2fd"
}
pkg: "Packaging\njar · war · ear · ejb\nshade · source · jlink" {
  width: 260
  height: 150
  style.fill: "#fff3e0"
}
tools: "Tooling: invoked by goal\ndependency · enforcer · archetype\nrelease · verifier · help" {
  width: 300
  height: 150
  style.fill: "#e8f5e9"
}
rep: "Reporting: <reporting>\ncheckstyle · changelog\njavadoc · pmd" {
  width: 260
  height: 150
  style.fill: "#f3e5f5"
}
```

**Fig. 1.** The Apache catalog by role: core plugins are the ones the default lifecycle binds by default; tooling plugins are usually called directly (`mvn dependency:tree`).

> [!warning] Core does not mean "invisible"
> Interview trap: "if plugins do all the work, why don't I declare the compiler plugin?" Because the packaging (`jar` by default) already binds `compiler:compile`, `surefire:test`, `jar:jar` and friends to phases; the plugin runs even when the POM is silent. Explicitly declaring it is for overriding configuration — the version or compiler arguments — not for making it run.

> [!tip] Interview answer
> **The core plugins map onto the lifecycle: clean, compiler, resources, surefire, failsafe, install, deploy, site. Packaging plugins (jar, war, shade, source) build artifacts, tooling plugins (dependency, enforcer, archetype, release) are called by goal, and reporting plugins produce the site. They all run without being declared because the packaging binds them to phases — the POM only overrides versions and configuration.**
