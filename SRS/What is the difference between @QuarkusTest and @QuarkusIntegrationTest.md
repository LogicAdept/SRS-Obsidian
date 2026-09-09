<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is the difference between @QuarkusTest and @QuarkusIntegrationTest?

> [!abstract] Short answer
> **`@QuarkusTest` boots the application in the same JVM** as the test, through the same augmentation artifacts: CDI injection into the test works, `@InjectMock` replaces beans, the `%test` profile is active, and startup is fast. **`@QuarkusIntegrationTest` launches the artifact the build produced** — the fast-jar, the native executable, or a container image — and tests it as a **black box over the network**: no CDI injection, no mock beans, no test-profile shortcuts; callbacks only with an explicit property. Unit-ish integration (`@QuarkusTest`) versus packaged-artifact verification (`@QuarkusIntegrationTest`) — both use REST Assured against a running server.

## What actually differs at runtime

`@QuarkusTest` reuses the build's augmentation and boots the app in-process; that is why beans are injectable and why bean replacement is possible — the container is right there ([[What bean scopes does Quarkus support]]). The `%test` profile activates automatically, so Dev Services and test config apply. `@QuarkusIntegrationTest` runs after packaging (it belongs to the failsafe/IT suite: `-DskipITs=false` with Maven): it launches the produced artifact as a subprocess — `java -jar`, the native binary, or a container if the build made one — and the test class talks HTTP (or the relevant protocol) from outside. Consequently: no `@InjectMock`, no `@ConfigProperty` in tests, no per-test profile tricks — the artifact is exactly what ships ([[What is the Quarkus fast-jar packaging format]]). A subset of lifecycle callbacks can run for integration tests only when `quarkus.test.enable-callbacks-for-integration-tests=true`.

```java
// Side-by-side from the verified demo (JDK 21, Quarkus 3.39.2):
//
// @QuarkusTest
// class ExpansionTest {
//     @Inject FragileService fragile;                     // possible: same JVM, same container
//
//     @Test
//     void cacheAndFallbackAndScheduler() {
//         given().when().get("/demo/fallback").then().statusCode(200).body(is("fallback"));
//         assertEquals(4, fragile.attemptsCount() - before);   // in-process assertion
//     }
// }
// -> "Tests run: 6, Failures: 0" (JUnit, port 8081, Profile test activated)
//
// @QuarkusIntegrationTest
// class PackagedIT {
//     @Test
//     void healthEndpointUp() {
//         given().when().get("/q/health/ready").then().statusCode(200);
//     }
// }
// -> launches target/quarkus-app/quarkus-run.jar as a subprocess and polls it;
//    injection lines like @Inject would fail the build of the test - no container here.
```

**Listing 1.** The same endpoints, two vantage points: white-box in-process assertions under `@QuarkusTest`, black-box verification of the shipped artifact under `@QuarkusIntegrationTest` ([[How do you test a Quarkus application]] covers the general test story).

```d2
direction: right
qt: "@QuarkusTest\nsame JVM as app\nCDI injection, @InjectMock\n%test profile, Dev Services" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
qa: "@QuarkusIntegrationTest\nlaunches the packaged artifact\njar | native | container" {
  width: 320
  height: 90
  style.fill: "#e3f2fd"
}
http: "REST Assured over HTTP" {
  width: 240
  height: 50
}
net: "Network only\nno CDI, no mocks" {
  width: 230
  height: 55
  style.fill: "#f5c6c6"
}
qt -> http
qa -> http
qa -> net
```

**Fig. 1.** Both suites speak HTTP; only one of them can reach into the container — that is the whole difference and the reason both exist ([[What is Mutiny in Quarkus]] reactive assertions belong to the in-process side).

## How teams layer them

The productive split: fast, fine-grained behavior coverage under `@QuarkusTest` in the unit/verify phase — business rules, error paths, bean interactions, mocks — and a thin `@QuarkusIntegrationTest` suite that proves the artifact boots and serves its critical endpoints (health, one representative business call), catching packaging, config-baking and native-specific failures the in-process suite structurally cannot see. Native executables are tested through `@QuarkusIntegrationTest` exclusively — there is no in-process mode for a native binary.

> [!warning] "Integration test passed" means nothing if it ran in-process
> The naming trap: a `@QuarkusTest` is an integration test in style but not in packaging — it validates classes, not the artifact; config mistakes that bake wrong values into a native image or missing resources that only exist in the jar never surface there. The mirrored mistake: writing all tests as `@QuarkusIntegrationTest` — every feedback cycle now pays packaging, and `@InjectMock`-style isolation is gone, so failures localize slowly. Also remember the ITs must run after packaging (`-DskipITs=false`); running them in the same phase as unit tests fails because the artifact does not exist yet.

> [!tip] Interview answer
> @QuarkusTest boots the app in the test's own JVM over the augmentation artifacts — CDI injection works, @InjectMock replaces beans, %test profile and Dev Services are active — so it's fast and fine-grained. @QuarkusIntegrationTest launches the actual build output — fast-jar, native executable or container — and tests it black-box over HTTP: no injection, no mocks, run after packaging via the failsafe suite. I layer them: behavior coverage in-process, and a small IT suite proving the shipped artifact boots and serves its critical endpoints — native code has only the second option.
