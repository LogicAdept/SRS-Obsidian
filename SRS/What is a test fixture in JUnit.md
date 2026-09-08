<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #SRS

# What is a test fixture in JUnit?

> [!abstract] Short answer
> A **test fixture** is the **fixed baseline state** a test runs against — the objects, data, files, connections and other context a test needs, together with the code that **sets it up** before and **tears it down** after. JUnit's own vocabulary defines the mechanism: the JUnit 4 wiki's overview describes "Test Fixtures — specify **set up and clean up methods on a per-method and per-class basis**", and Jupiter implements exactly that with four lifecycle annotations: **`@BeforeEach`** — "should be executed before each `@Test`, `@RepeatedTest`, `@ParameterizedTest`, or `@TestFactory` method in the current class" — plus `@AfterEach` (after each), and the once-per-class **`@BeforeAll`**/`@AfterAll` pair. Two properties make the fixture model work: Jupiter creates a **new test-class instance per test** (so instance fields start fresh — per-method isolation by default), and lifecycle methods "are inherited unless they are overridden" (superclass setup runs before subclass setup; teardown in reverse). The fixture is the *arrangement* half of the arrange–act–assert rhythm — not the test's assertions, and not the shared production code under test. Mechanics detail: [[What fixture annotations exist in JUnit]]; class-level specifics: [[What are the @BeforeAll and @AfterAll annotations in JUnit]].

## Set up, act, assert, tear down

The fixture answers the question every test faces: *in what state does the world need to be for this test to be meaningful?* The canonical rhythm is **arrange–act–assert**, and the fixture is the arrange part — extracted into a method that runs before the test body. Concretely, a fixture for an order-service test might: construct the service with a stubbed gateway, seed the repository with two known orders, open a temporary directory with a prepared file. After the test, teardown restores the world: close connections, delete temporary files, reset statics or singletons the test touched. In Jupiter, `@BeforeEach`/`@AfterEach` bracket *each* test (a fresh instance per test makes the fixture's instance fields automatically pristine), and `@BeforeAll`/`@AfterAll` bracket the *whole class* for expensive resources that all tests can share read-only — an embedded server started once, a Testcontainers container, a schema. The design decision per resource is always the same trade: **cheap and mutable → per-test (isolation)**; **expensive and read-mostly → class-level (speed)** — and when something is expensive *and* mutable, the senior move is to share it and reset it per-test in `@BeforeEach`.

## Isolation: the reason the fixture exists

The quiet achievement of the fixture model is **inter-test independence**. Because each test gets a fresh instance and the fixture re-establishes the baseline before every test, tests can run in any order, in parallel (JUnit Jupiter supports parallel execution on the JUnit Platform), or alone — without noticing each other. State that leaks between tests produces the classic pathology suite: a test that passes alone and fails in the suite, a test that only passes when its neighbor runs first, a suite whose result depends on JVM ordering. The fixture annotations are the framework's answer — but only when the fixture *fully describes* the state: any setup done "informally" (a static counter bumped in one test, a singleton mutated in another) escapes the model. Two disciplines keep it honest: the fixture is **explicit** (what `@BeforeEach` does is visible at the top of the class, not implied by test order), and the fixture is **complete** (a test's meaning does not depend on what the previous test happened to leave behind). Where state genuinely must be shared — a slow external resource — it belongs in a class-level fixture (or an extension/`@TempDir` for file-system cases) with per-test reset of the mutable parts.

## What belongs in a fixture — and what does not

The judgement being probed is scope. **In**: object graphs the tests read, seeded data, temporary resources, client objects wired to stubs, the request-id stamped into a thread context. **Out**: the *action* under test (arrange, don't act in `@BeforeEach` — a setup that already executes the behavior makes every test a re-verification), and assertions hidden inside setup (a fixture that "verifies" its own work turns fixture bugs into confusing test failures). Shared fixture code across classes moves to test utilities or — the Jupiter-native form — **extensions** (`@ExtendWith`), which generalize fixtures to reusable, annotated providers (Spring's test framework is the flagship example; see [[What is SpringRunner]] for the 4.x lineage). JUnit 4 named the same annotations `@Before`/`@After`/`@BeforeClass`/`@AfterClass` — same semantics, renamed in Jupiter (mapping: [[What fixture annotations exist in JUnit]]); tests that need skipping despite having fixtures use `@Disabled` ([[What is the JUnit Ignore annotation for]]), whose disabled methods skip their `@BeforeEach`/`@AfterEach` too.

```java
class OrderServiceTest {
    OrderService service;                 // fixture: fresh per test
    static OrderServer server;            // fixture: shared, expensive

    @BeforeAll
    static void bootShared() { server = OrderServer.start(); }   // once

    @BeforeEach
    void arrangeBaseline() {              // the fixture proper:
        service = new OrderService(       //   fresh objects per test,
            server.client(),              //   stubbed externals,
            twoKnownOrders()              //   seeded data
        );
        TempFiles.write("export.csv", "id;total\n1;100");
    }

    @Test void acceptsValidOrder() { /* act + assert */ }
    @Test void rejectsNegativeTotal() { /* act + assert */ }

    @AfterEach
    void resetWorld() { TempFiles.deleteAll(); }   // restore, always

    @AfterAll
    static void stopShared() { server.stop(); }    // once
}
```

**Listing 1.** The fixture at three scopes: once-per-class shared server, per-test baseline objects and seeded data, teardown that runs even when the test fails.

```d2
direction: top-down
beforeall: "@BeforeAll (once)\nexpensive shared resource" {style.fill: "#e8f5e9"}
cycle: "per test — fresh instance" {style.fill: "#e3f2fd"}
setup: "@BeforeEach\narrange: objects, seed data" {style.fill: "#fff3e0"}
test: "@Test\nact + assert" {style.fill: "#e3f2fd"}
teardown: "@AfterEach\ntear down, even on failure" {style.fill: "#fff3e0"}
afterall: "@AfterAll (once)\nrelease shared resource" {style.fill: "#ffebee"}
beforeall -> cycle
cycle -> setup -> test -> teardown -> cycle
cycle -> afterall: "last test done"
```

**Fig. 1.** The fixture timeline: a class-level pair brackets the run; each test is wrapped in per-test arrange/teardown on a fresh instance.

## Vocabulary the interview actually tests

Four items are graded. **Definition** — fixed baseline state + the setup/teardown code establishing it; "the `@BeforeEach` method" alone is the mechanism, not the concept. **The two timescales** — per-method (`@BeforeEach`/`@AfterEach` around every test) and per-class (`@BeforeAll`/`@AfterAll` around the class), and which resources belong in each. **Isolation mechanism** — fresh instance per test plus an explicit, complete fixture is *why* tests are order-independent; hand-waving "JUnit isolates tests" without the instance model is the junior tell. **JUnit 4 names** — `@Before`/`@After`/`@BeforeClass`/`@AfterClass`, same semantics. A senior bonus: teardown runs even for failed tests (the finally-semantics of after-hooks), and fixture code that mutates shared statics is exactly the leak the model cannot save you from.

> [!warning] "The fixture is whatever the tests happen to leave behind" — implicit state is the fixture killer
> The trap being probed is implicit, order-dependent state: a test that *creates* the data its neighbor expects has, in effect, a fixture written by the previous test — it passes in the suite and fails alone, and reversing the order breaks it. Two adjacent slips: doing the *action* under test inside `@BeforeEach` (the setup executes the behavior, so every test re-verifies the same side effect and per-test variations drown in setup flags), and heavy shared fixtures with mutable state — a class-level singleton database that tests mutate "just a little" until the suite is order-sensitive. The senior discipline: the fixture is explicit (`@BeforeEach` builds exactly the baseline named), mutable parts reset per test even in shared class-level fixtures, and anything crossing classes becomes an extension or utility — not copy-pasted setup.

> [!tip] Interview answer
> **A test fixture is the fixed baseline state a test runs against — the objects, seeded data and resources the test needs — plus the code that sets it up and tears it down. JUnit expresses it with four lifecycle annotations: @BeforeEach and @AfterEach around every test, @BeforeAll and @AfterAll around the whole class — JUnit 4 called them @Before, @After, @BeforeClass, @AfterClass. The isolation comes from two design choices: Jupiter creates a fresh test-class instance per test, and lifecycle methods are inherited — so tests are order-independent when the fixture is explicit and complete. Cheap mutable state goes per-test; expensive read-mostly resources go class-level; and teardown runs even when the test fails — that's why cleanup lives in the after-hooks.**
