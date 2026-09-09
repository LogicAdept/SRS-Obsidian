<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What are the dependency scopes in a Maven pom

> [!abstract] Short answer
> **A scope decides two things: which classpaths (compile, runtime, test) contain the dependency, and whether it propagates transitively.** The six scopes: `compile` (default, everywhere, transitive), `provided` (compile+test only — the JDK or container supplies it at runtime), `runtime` (runtime+test, not compile), `test` (test compilation and execution only, not transitive), `system` (a local file path, effectively deprecated), `import` (only in `dependencyManagement` for BOMs).

## One dependency, three classpaths

The build has distinct classpaths: compiling `src/main/java`, running the app, compiling and running `src/test/java`. The scope table decides where each dependency appears:

```d2
direction: right
s1: "compile\ndefault; all classpaths;\ntransitive to consumers" {
  width: 270
  height: 100
  style.fill: "#e8f5e9"
}
s2: "provided\ncompile + test;\ncontainer/JDK at runtime;\nnot transitive" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
s3: "runtime\nruntime + test;\nhidden at compile time" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
s4: "test\ntest compile + run;\nnot transitive" {
  width: 240
  height: 100
  style.fill: "#ffebee"
}
s5: "system / import\nlocal jar path /\nBOM import in\ndependencyManagement" {
  width: 280
  height: 110
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Six scopes; the everyday four are compile, provided, runtime, test.

Classic placements: JDBC drivers are `runtime` (you compile against `java.sql`, not the driver), the Servlet API is `provided` (the web container supplies it), JUnit is `test`:

```java
mvn -B dependency:tree
// [INFO] com.demo:demo-app:jar:1.0.0
// [INFO] \- org.junit.jupiter:junit-jupiter:jar:5.10.2:test
// [INFO]    +- org.junit.jupiter:junit-jupiter-api:jar:5.10.2:test
// [INFO]    |  +- org.opentest4j:opentest4j:jar:1.3.0:test
// [INFO]    |  +- org.junit.platform:junit-platform-commons:jar:1.10.2:test
// [INFO]    |  \- org.apiguardian:apiguardian-api:jar:1.1.2:test
// [INFO]    +- org.junit.jupiter:junit-jupiter-params:jar:5.10.2:test
// [INFO]    \- org.junit.jupiter:junit-jupiter-engine:jar:5.10.2:test
// [INFO]       \- org.junit.platform:junit-platform-engine:jar:1.10.2:test
```

**Listing 1.** Real output (Maven 3.9.9, JDK 21): the whole JUnit subtree rides at `test` scope.

## Proof that test scope stays out of src/main

The scope is enforced at compile time, not just conventionally:

```java
// src/main/java/com/demo/IllegalUse.java
import org.junit.jupiter.api.Test;

public class IllegalUse {
    @Test
    public void oops() {
    }
}

mvn compile
// [ERROR] COMPILATION ERROR :
// [ERROR] .../IllegalUse.java:[3,29] package org.junit.jupiter.api does not exist
// [ERROR]   symbol:   class Test
```

**Listing 2.** The test-scoped JUnit jar is invisible to the main compile classpath — the build fails with "package does not exist" (verified run).

> [!warning] Wrong scope fails late and far from the cause
> The traps live in the edges. `provided` compiles fine and then dies with `ClassNotFoundException` in the container or in fat-jar deployment — because runtime classpaths exclude it. Marking a library `compile` "just in case" bloats every consumer through transitivity and causes dependency conflicts, since compile-scope deps propagate while test/provided do not. `system` scope bypasses repositories with a hardcoded path and is not recommended. And `import` is not a classpath scope at all — it only splices a BOM's managed versions inside `dependencyManagement`. Use `mvn dependency:tree` before arguing about any of this. The POM blocks that carry these declarations: [[How would you explain the structure of a Maven pom.xml file]]; the phases where test-scope code runs: [[How would you explain the Maven build lifecycle]]; the test runners consuming the test classpath: [[What is the difference between the Surefire and Failsafe plugins in Maven]].

> [!tip] Interview answer
> **Six scopes, and each answers where the jar lands and whether it spreads transitively. compile is the default — every classpath, transitive. provided — compiles now, container or JDK supplies at runtime, not transitive. runtime — not visible when compiling, needed to run, like JDBC drivers. test — only the test classpath, like JUnit. system points at a local jar and is discouraged, and import is the BOM mechanism inside dependencyManagement. The classic failure: wrong provided/test scope surfaces as ClassNotFoundException or package-does-not-exist far from the change.**

