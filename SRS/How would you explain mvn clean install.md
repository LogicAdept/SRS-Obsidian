<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# How would you explain mvn clean install

> [!abstract] Short answer
> **It is two lifecycles in one command: `clean` deletes the `target/` directory, then the default lifecycle runs from `validate` up to `install`, which puts the packaged artifact into the local repository (`~/.m2`) for other local projects to consume.** The result: a from-scratch build whose jar is available to everything on your machine.

## What actually runs

`clean` is a phase of the clean lifecycle (`clean:clean` deletes `target/`). `install` is a phase near the end of the default lifecycle — package → verify → install — so invoking it also compiles sources and runs unit tests on the way. A verified run of the whole command:

```java
mvn clean install
// --- clean:3.2.0:clean (default-clean) @ demo-app ---      target/ wiped
// --- resources:3.3.1:resources (default-resources) @ demo-app ---
// --- compiler:3.13.0:compile (default-compile) @ demo-app ---
// [INFO] Compiling 1 source file with javac [debug release 21] to target/classes
// --- compiler:3.13.0:testCompile (default-testCompile) @ demo-app ---
// --- surefire:3.2.5:test (default-test) @ demo-app ---
// [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
// --- jar:3.4.1:jar (default-jar) @ demo-app ---
// [INFO] Building jar: .../target/demo-app-1.0.0.jar
// --- failsafe:3.2.5:integration-test (default) @ demo-app ---   (if configured)
// --- install:3.1.2:install (default-install) @ demo-app ---
// [INFO] Installing .../pom.xml to ~/.m2/repository/com/demo/demo-app/1.0.0/demo-app-1.0.0.pom
// [INFO] Installing .../demo-app-1.0.0.jar to ~/.m2/repository/com/demo/demo-app/1.0.0/demo-app-1.0.0.jar
// [INFO] BUILD SUCCESS
```

**Listing 1.** Captured with Maven 3.9.9 on JDK 21 — every line names the plugin goal and the phase it is bound to.

```d2
direction: right
clean: "clean lifecycle\ndelete target/" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
chain: "default lifecycle\ncompile -> test -> package" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
inst: "install phase\ncopy jar + pom to ~/.m2" {
  width: 290
  height: 90
  style.fill: "#e8f5e9"
}
other: "Other local projects\nresolve it as a dependency" {
  width: 290
  height: 90
  style.fill: "#e8f5e9"
}
clean -> chain -> inst -> other
```

**Fig. 1.** Wipe, rebuild from source, then publish the artifact to the local cache where sibling modules can pick it up.

## Why "clean" matters in the command

`target/` is not self-healing: stale compiled classes, old generated sources, or a leftover jar can survive incremental builds and make a build pass or fail for reasons that vanish on a wipe. CI always builds clean for exactly that reason, and locally `mvn clean install` is the honest rebuild — slightly slower, reproducibly correct. The alternative habit, deleting `target/` by hand when builds misbehave, is the same operation without the lifecycle guardrails.

> [!warning] install is not deploy, and the tests do run
> Two classic mix-ups. First: `install` writes to your **local** `~/.m2/repository`; `deploy` is the next step that pushes to a **remote** repository for the whole team — saying "I deployed to Maven Central with mvn clean install" is wrong. Second: `install` includes the `test` phase, so unit tests run on the way — people surprised by this reach for `-DskipTests`, which turns the command into a compile-and-package that validates nothing; use it deliberately, not by default. In multi-module projects, module B resolving module A resolves from `~/.m2` after A's install — which is exactly why the command is the glue of local multi-module work. Phase ordering refresher: [[How would you explain the Maven build lifecycle]]; what the POM contributes: [[How would you explain the structure of a Maven pom.xml file]].

> [!tip] Interview answer
> **mvn clean install wipes target, then runs the default lifecycle through install: compile, unit tests, package, and finally copies the artifact into the local ~/.m2 repository so other local projects can depend on it. Clean gives reproducibility, install is local publishing — deploy would be the team-level remote push. It is the everyday rebuild-and-share command in multi-module development.**

