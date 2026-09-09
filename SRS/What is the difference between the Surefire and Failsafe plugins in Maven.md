<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #Java/Testing #SRS

# What is the difference between the Surefire and Failsafe plugins in Maven

> [!abstract] Short answer
> **Surefire runs unit tests, bound to the `test` phase; Failsafe runs integration tests across the `pre-integration-test` → `integration-test` → `post-integration-test` → `verify` stretch.** The point of the split: a failing unit test stops the build immediately, but a failing integration test must not skip the environment teardown — Failsafe defers the failure to `verify`, so cleanup still happens.

## Different phases, different failure semantics

Both are JUnit runners under the hood (Surefire auto-detects the JUnit Platform provider). They differ in when they run and what a failure does. Surefire reports go to `target/surefire-reports/`, Failsafe's to `target/failsafe-reports/`.

```d2
direction: down
test: "test phase\nSurefire: unit tests" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
fail: "Unit test fails?\nbuild stops here" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
pre: "pre-integration-test\nset up environment" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
it: "integration-test\nFailsafe: run ITs\nfailure is NOTED, not raised" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
post: "post-integration-test\ntear down environment" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
verify: "verify phase\nFailsafe: check results now" {
  width: 290
  height: 80
  style.fill: "#e8f5e9"
}
test -> fail
fail -> pre: "all green"
pre -> it -> post -> verify
```

**Fig. 1.** Surefire is bound to one phase; Failsafe spans four so the environment is torn down before the failure is raised.

Naming conventions decide who picks up what: Surefire's default includes are `*Test`, `Test*`, `*Tests`, `*TestCase`; Failsafe's are `*IT`, `IT*`, `*ITCase`. One verified run shows both in a single `mvn clean install`:

```java
mvn -B clean install
// --- surefire:3.2.5:test (default-test) @ demo-app ---
// [INFO] Running com.demo.AppTest
// [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.064 s -- in com.demo.AppTest
// --- jar:3.4.1:jar (default-jar) @ demo-app ---
// --- failsafe:3.2.5:integration-test (default) @ demo-app ---
// [INFO] Running com.demo.AppIT
// [INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.055 s -- in com.demo.AppIT
// --- failsafe:3.2.5:verify (default) @ demo-app ---
// --- install:3.1.2:install (default-install) @ demo-app ---
// [INFO] BUILD SUCCESS
```

**Listing 1.** Maven 3.9.9 on JDK 21: `AppTest` ran at the `test` phase, `AppIT` only after packaging at `integration-test` — each plugin caught its own naming pattern.

Failsafe needs two goals bound in the POM (`integration-test` and `verify`) because without `verify` a failing IT would never fail the build:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-failsafe-plugin</artifactId>
    <version>3.2.5</version>
    <executions>
        <execution>
            <goals>
                <goal>integration-test</goal>
                <goal>verify</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**Listing 2.** The standard Failsafe wiring from the demo POM that produced Listing 1.

> [!warning] Running ITs with Surefire skips your teardown
> The named trap: if Surefire also matches `*IT` classes (or you bind it to `integration-test`), a failed test aborts the build inside `integration-test` — before `post-integration-test` tears the environment down. Containers and databases leak into the next run or hang CI. That is the exact scenario the Failsafe design exists for: "failsafe" as the antonym pun of "surefire" — it fails safely, deferring the verdict to `verify`. Second trap: Failsafe runs ITs against the packaged artifact, so it only sees the real thing after `package`; running "integration tests" before packaging tests classes, not the deployable. Where the IT classpath comes from (test scope): [[What are the dependency scopes in a Maven pom]]; the phase chain: [[How would you explain the Maven build lifecycle]]; the command that triggers both runners: [[How would you explain mvn clean install]].

> [!tip] Interview answer
> **Surefire runs unit tests in the test phase — a failure stops the build immediately. Failsafe runs integration tests around packaging: pre-integration-test sets up, integration-test runs but swallows the failure, post-integration-test tears the environment down, and verify raises the failure afterwards. Name unit tests *Test and ITs *IT, and give Failsafe the integration-test and verify goals so teardown always happens.**

