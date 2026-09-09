<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# How would you explain the Maven build lifecycle

> [!abstract] Short answer
> **A lifecycle is Maven's fixed sequence of build phases; you invoke the last phase you need and everything before it runs first.** There are three built-in lifecycles — default (build and deploy), clean (remove build output), site (documentation) — and each phase is executed by plugin goals bound to it, not by Maven itself.

## Three lifecycles, one rule: phases run in order

The default lifecycle's headline phases: `validate`, `compile`, `test`, `package`, `verify`, `install`, `deploy`. Calling `mvn package` runs validate → ... → package and stops; `mvn verify` continues through integration-test checks. Clean and site are separate lifecycles, so `mvn clean install` is two lifecycles invoked in one line.

```d2
direction: down
v: "validate\nproject is sane" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
c: "compile\nsrc/main/java -> target/classes" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
t: "test\nunit tests (Surefire)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
p: "package\njar/war into target/" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
iv: "verify\nIT results checked" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
i: "install\ninto local ~/.m2" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
d: "deploy\nto remote repository" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
v -> c -> t -> p -> iv -> i -> d
```

**Fig. 1.** The default lifecycle as an ordered chain: invoking a phase runs the whole prefix up to it.

```java
mvn clean install
// --- clean:3.2.0:clean (default-clean) @ demo-app ---        (clean lifecycle)
// --- compiler:3.13.0:compile (default-compile) @ demo-app ---
// [INFO] Compiling 1 source file with javac [debug release 21] to target/classes
// --- surefire:3.2.5:test (default-test) @ demo-app ---        (bound to the test phase)
// [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
// --- jar:3.4.1:jar (default-jar) @ demo-app ---               (bound to the package phase)
// --- install:3.1.2:install (default-install) @ demo-app ---
// [INFO] BUILD SUCCESS
```

**Listing 1.** Maven 3.9.9 on JDK 21: one command walks two lifecycles; the log lines name the `plugin:goal (phase)` triple for every step.

## Phases are steps; goals are the work

A phase on its own does nothing — plugin goals are attached to it. The `compiler` plugin's `compile` goal is bound to the `compile` phase by default; Surefire's `test` goal to `test`; `jar:jar` to `package`. That is why the same `mvn test` command works for any project yet runs that project's tests: the binding is standard, the configuration lives in the POM. Custom behavior plugs in by binding extra goals to phases — see [[How would you explain the structure of a Maven pom.xml file]] for the plugin block.

> [!warning] mvn skips nothing before the phase you named
> Interview trap: "I run `mvn test`, why is my app compiling?" Because `test` sits after `compile` in the chain — Maven always executes the prefix. The same rule explains why `mvn integration-test` re-runs unit tests (Surefire is bound to `test`): phases do not skip, they accumulate. If you want only one specific action, invoke the goal directly (`mvn surefire:test`), accepting that lifecycle-side effects (resources, dependencies) may not have run. The integration-test story — why Failsafe exists and why the environment must survive failures — is in [[What is the difference between the Surefire and Failsafe plugins in Maven]]; the full journey to the local repository is [[How would you explain mvn clean install]].

> [!tip] Interview answer
> **Maven has three built-in lifecycles: default, clean, and site. The default one is the ordered chain validate, compile, test, package, verify, install, deploy — call the last phase you need and the prefix runs first. Phases themselves are empty steps; plugin goals are bound to them and do the work. Clean removes target, site builds docs, and everything is configured in the POM against that phase model.**

