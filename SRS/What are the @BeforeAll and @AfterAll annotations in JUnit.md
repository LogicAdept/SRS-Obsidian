<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #SRS

# What are the @BeforeAll and @AfterAll annotations in JUnit?

> [!abstract] Short answer
> **`@BeforeAll`** and **`@AfterAll`** mark the **class-level fixture hooks** of JUnit Jupiter: the annotated method runs **once** before (respectively after) **all** tests in the class. The guide's definition: `@BeforeAll` "denotes that the annotated method should be executed before all `@Test`, `@RepeatedTest`, `@ParameterizedTest`, and `@TestFactory` methods in the current class; **analogous to JUnit 4's `@BeforeClass`**", with `@AfterAll` the symmetric closer — "analogous to JUnit 4's `@AfterClass`". The signature rule is the interview's favorite: such methods "**must be `static` unless the 'per-class' test instance lifecycle is used**" — because Jupiter's default lifecycle creates a **new test-class instance per test**, so when `@BeforeAll` runs there is *no instance yet* to call a method on; it can only be a `static` (or `@TestInstance(Lifecycle.PER_CLASS)` non-static, or a Java `interface` `default` method) method. They are **inherited** unless overridden, and their per-class counterparts — running around *each* test — are `@BeforeEach`/`@AfterEach`. Mapping and siblings: [[What fixture annotations exist in JUnit]]; concept: [[What is a test fixture in JUnit]].

## Why "static": the per-method instance model

The rule is not bureaucracy — it follows from Jupiter's lifecycle design. By default each test method executes on a **fresh instance** of the test class; instance fields therefore do not carry state between tests, which is what makes tests order-independent by construction. Now place `@BeforeAll` in time: it runs *before the first test of the class* — before any of those instances exists. A non-static method needs a receiver, and there is none; hence `static`. The same logic explains what the hook *may* touch: `static` fields, static helpers, external resources — never instance state. The escape hatch exists for the cases where a shared instance is genuinely useful: annotating the class with `@TestInstance(Lifecycle.PER_CLASS)` switches to one instance for the whole class, `@BeforeAll` may then be non-static and may initialize instance fields — with the cost that state now persists *across* tests and the author is responsible for restoring isolation. A practical Jupiter footnote: `@Nested` inner test classes could not declare static methods before Java 16 (`static` in an inner class was illegal), so per-class lifecycle was the documented way to give them `@BeforeAll` hooks — one more reason the annotation's lifecycle semantics, not its name, is what is being tested.

## What "before all" and "after all" actually bracket

The pair executes around the *entire* class run: `@BeforeAll` before the first `@Test`/`@RepeatedTest`/`@ParameterizedTest`/`@TestFactory` method, `@AfterAll` after the last one — once per class, not once per test. Typical uses: starting and stopping something expensive whose lifetime spans all tests (an embedded database or server, a Docker container via Testcontainers, a shared `ApplicationContext` in Spring's test integration — see [[What is SpringRunner]] for how the 4.x era wired that), and the symmetric teardown (closing the server, verifying no leaked connections). Execution order within a class: `@BeforeAll` → for each test: `@BeforeEach` → test → `@AfterEach` → … → `@AfterAll`. Inheritance adds the outer-in wrinkle the guide spells out for lifecycle methods generally — they "are inherited unless they are overridden": a superclass `@BeforeAll` runs before the subclass's, and after-hooks run in reverse, so teardown restores what setup did. One nuance beginners trip on: if a *test fails*, `@AfterEach` still runs, and `@AfterAll` still runs — the after-hooks are the "finally" of the fixture world, which is exactly why cleanup logic belongs there and not in the tests.

## Choosing between class-level and per-test hooks

The design decision behind the annotations is **scope of shared state**. Class-level hooks (`@BeforeAll`/`@AfterAll`) fit expensive, read-mostly resources that tolerate sharing across tests: boot a container once, run hundreds of tests against it, stop it once. Per-test hooks (`@BeforeEach`/`@AfterEach`) fit per-test state that must be pristine: seed rows, create fixtures, roll back. The classic senior heuristic: *expensive and immutable → class-level; cheap and mutable → per-test*. Mutable state shared through `@BeforeAll` (a mutable singleton database modified by each test) is the anti-pattern that produces order-dependent, "passes alone, fails in suite" tests — the isolation cost is precisely what the static rule nudges you away from. With `@TestInstance(PER_CLASS)` the temptation is strongest (instance fields persist), so the discipline is explicit reset in `@BeforeEach`. The full hook table with the JUnit 4 names: [[What fixture annotations exist in JUnit]]; disabling tests that need the hooks: [[What is the JUnit Ignore annotation for]].

```java
class OrderApiTest {
    static OrderServer server;                 // shared, expensive, read-mostly

    @BeforeAll
    static void startServer() {                // runs ONCE, before any test;
        server = OrderServer.start();          // static: no instance exists yet
    }

    @BeforeEach
    void seedOneOrder() {                      // fresh state per test
        repository.seed("order-1");
    }

    @Test void listsOrders() { /* ... */ }
    @Test void rejectsEmpty() { /* ... */ }

    @AfterEach
    void clearSeed() { repository.clear(); }   // finally of the per-test world

    @AfterAll
    static void stopServer() { server.stop(); } // runs ONCE, after all tests
}

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class LegacyStyleTest {
    OrderServer server = OrderServer.start();  // instance field shared across tests

    @BeforeAll
    void startOnce() { /* non-static now legal: one instance for the class */ }
}
```

**Listing 1.** The standard static pair around per-test hooks, and the `PER_CLASS` opt-in that makes non-static `@BeforeAll` legal — at the price of cross-test state.

```d2
direction: top-down
beforeall: "@BeforeAll\nONCE (static by default)" {style.fill: "#e8f5e9"}
t1: "test 1: @BeforeEach -> test -> @AfterEach\n(new instance per test)" {style.fill: "#e3f2fd"}
t2: "test 2: @BeforeEach -> test -> @AfterEach\n(new instance per test)" {style.fill: "#e3f2fd"}
afterall: "@AfterAll\nONCE (static by default)" {style.fill: "#ffebee"}
beforeall -> t1 -> t2 -> afterall
per: "@TestInstance(PER_CLASS):\none instance for the class,\nnon-static hooks allowed" {style.fill: "#fff8e1"}
beforeall - per: "opt-in relaxes\nthe static rule" {style.stroke-dash: 4}
```

**Fig. 1.** The class timeline: one `@BeforeAll`/`@AfterAll` pair brackets per-test cycles, each of which gets a fresh instance; `PER_CLASS` relaxes the static rule at the cost of isolation.

## Vocabulary the interview actually tests

Four items are graded. **The static rule and its reason** — "must be static" quoted without "because per-method lifecycle creates no instance before all tests" is half credit; the `PER_CLASS` escape and its cost complete it. **The bracket** — once per class around all tests, not around each; per-test is the other pair's job. **The JUnit 4 names** — `@BeforeClass`/`@AfterClass` (also static; JUnit 4 was per-class-instance-all-along, so the static requirement there predates Jupiter's per-method default). **Inheritance order** — hooks are inherited unless overridden; outer `@BeforeAll` runs first, after-hooks unwind in reverse. A senior bonus: `@AfterAll` runs even when tests fail — cleanup belongs there and in `@AfterEach`, not in the tests themselves.

> [!warning] "Make it static or just annotate the class PER_CLASS" — the escape hatch changes test semantics
> The trap most candidates miss is the cost of `@TestInstance(Lifecycle.PER_CLASS)`: it does not merely "allow non-static `@BeforeAll`" — it makes **instance fields persist across tests**, silently replacing Jupiter's per-test isolation with shared mutable state, and the first order-dependent suite failure appears weeks later. Related slips: trying to read instance fields from a static `@BeforeAll` (compile error — no instance exists; this is the *point*), expecting `@BeforeAll` to re-run for each test (that is `@BeforeEach`), and forgetting that a *disabled* class still constructs nothing useful — hooks are skipped along with the tests (see [[What is the JUnit Ignore annotation for]]). And in `@Nested` classes before Java 16, remember static methods were illegal — `PER_CLASS` was the documented workaround.

> [!tip] Interview answer
> **@BeforeAll and @AfterAll are the class-level fixture hooks — they run once around all tests in the class, Jupiter's analogues of JUnit 4's @BeforeClass and @AfterClass. The key rule: by default they must be static, because Jupiter creates a fresh test-class instance per test, so at @BeforeAll time no instance exists to call a method on. If you annotate the class with @TestInstance(PER_CLASS) — one instance for the whole class — the hooks can be non-static, but instance state then persists across tests and you own the isolation. Typical use: start and stop an expensive shared resource once — a server, an embedded database, a container — while per-test state stays in @BeforeEach/@AfterEach.**
