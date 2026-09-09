<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# How would you explain Maven

> [!abstract] Short answer
> **Maven is a build automation and dependency-management tool: you describe the project in one declarative `pom.xml` (coordinates, dependencies, plugins), and Maven runs the build through a fixed lifecycle of phases, doing the real work through plugins.** Same commands build any Maven project, dependencies are downloaded by coordinates from repositories, and the directory layout is standardized.

## What Maven actually provides

Maven's stated objectives are a simple, uniform build process and quality project information. The mechanics behind that: a conventional project layout (`src/main/java`, `src/test/java`, `target/` for output), a centrally defined build lifecycle, and a dependency mechanism that resolves artifacts by `groupId:artifactId:version` coordinates from remote repositories into your local cache (`~/.m2/repository`).

```d2
direction: right
pom: "pom.xml\ncoordinates + deps + plugins" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
lifecycle: "Fixed lifecycle\nvalidate -> ... -> deploy" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
plugins: "Plugins do the work\ncompiler, surefire, jar..." {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
repo: "Repositories\n~/.m2 local, Central remote" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
pom -> lifecycle
lifecycle -> plugins
plugins -> repo
```

**Fig. 1.** The POM declares; the lifecycle sequences; plugins execute; repositories supply dependencies and artifacts.

You write what the project is, not how to build it — the opposite tradeoff from script-based builds. Maven is also the reference for coordinates everywhere: a module's identity (`com.demo:demo-app:1.0.0`) is Maven-shaped even in Gradle builds, and dependency resolution rules ([[What are the dependency scopes in a Maven pom]]) define what lands on which classpath.

## The build in practice

A real minimal run shows the pieces working together — phases execute in order, and each active step is a plugin goal:

```java
mvn clean install
// --- clean:3.2.0:clean (default-clean) @ demo-app ---
// --- compiler:3.13.0:compile (default-compile) @ demo-app ---
// [INFO] Compiling 1 source file with javac [debug release 21] to target/classes
// --- surefire:3.2.5:test (default-test) @ demo-app ---
// [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
// --- jar:3.4.1:jar (default-jar) @ demo-app ---
// --- install:3.1.2:install (default-install) @ demo-app ---
// [INFO] Installing .../demo-app-1.0.0.jar to ~/.m2/repository/com/demo/demo-app/1.0.0/
// [INFO] BUILD SUCCESS
```

**Listing 1.** Verified with Maven 3.9.9 on JDK 21: one command cleaned, compiled, tested, packaged, and installed the artifact into the local repository.

> [!warning] Maven is declarative — fighting it costs more than the XML is worth
> The common misread is that Maven is "outdated XML" and the workaround is hacking behavior in. The model inverts responsibility: the lifecycle and layout are fixed, so unusual steps (generated sources, custom packaging) go through plugins bound to phases, not free-form script. Two traps follow. First, Maven runs phases, not plugin goals directly — calling `mvn compiler:compile` skips the test and packaging steps a phase would have run. Second, without version management the build is unpinned: dependency coordinates without `dependencyManagement` drift across modules, and transitive conflicts resolve silently. For the phase model itself see [[How would you explain the Maven build lifecycle]], for one full command walk-through [[How would you explain mvn clean install]], and for Gradle's counter-model see [[Do you use Maven or Gradle for Java project builds]].

## Where it sits in interviews

"Explain Maven" wants the division: declarative POM + standard lifecycle + plugin execution + repository-based dependency management. The POM shape is in [[How would you explain the structure of a Maven pom.xml file]]; the test tooling that plugs into its phases is covered by [[What is the difference between the Surefire and Failsafe plugins in Maven]].

> [!tip] Interview answer
> **Maven is a declarative build and dependency management tool. You describe the project once in pom.xml — coordinates, dependencies, plugins — and Maven builds it through a standard lifecycle: validate, compile, test, package, install, deploy. The work is done by plugins, dependencies are resolved by coordinates from repositories into a local ~/.m2 cache, and the layout is conventional, so the same commands build any Maven project.**

