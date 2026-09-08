<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #SRS

# What is the difference between hard and soft assertions?

> [!abstract] Short answer
> **Hard** assertions are the default behavior of every JUnit assertion: each `assertEquals`/`assertTrue` **throws `AssertionError` on failure immediately**, so the test method stops at the *first* failed check and later checks never run. **Soft** assertions run *all* the checks anyway and report every failure together. JUnit Jupiter's built-in soft mechanism is **`assertAll`** — grouped assertions — with the guide's own wording: "In a grouped assertion all assertions are executed, and all failures will be reported together" (a failed heading produces a `MultipleFailuresError` carrying all of them). AssertJ ships the same idea as **`SoftAssertions`**, collected and checked via `assertAll()` at the end — with convenience wrappers (the JUnit 4 rule, the JUnit 5 extension that injects a `SoftAssertions` parameter, `AutoCloseableSoftAssertions`, and `assertSoftly`). The engineering reason soft assertions exist: when validating a multi-field response, hard assertions show you *one* bug per test run; soft assertions show you *all* of them in one run — which is the difference between one CI cycle and several. Related: [[Which assertions does JUnit provide]] for the assertion catalogue, [[What fixture annotations exist in JUnit]] for where checks execute.

## Hard: fail fast, and what the shortcut costs

Hard semantics are simply Java semantics: an assertion is a method call that throws `AssertionError` when its condition fails; an uncaught error fails the test, and the test method's remaining lines never execute. Fail-fast is usually *right*: the next check often *depends* on the previous one — asserting a field of an object that the previous assert already proved to be null would only add a confusing secondary `NullPointerException`, and the guide itself teaches the pattern: "within a code block, if an assertion fails the subsequent code in the same block will be skipped" — inside `assertAll` blocks, dependent assertions are grouped *sequentially* so a failed guard skips the checks that depend on it. The cost appears with *independent* checks: verify a REST response's status, three headers, five body fields and the schema — with hard assertions a typo in field #2 hides whether fields #3–#8 are also broken. The test turns red, the fix goes in, CI reruns, field #6 is now red, rerun again. Each cycle costs minutes to hours; multiply by the number of latent bugs and the case for softness writes itself.

## Soft: assertAll in Jupiter, SoftAssertions in AssertJ

Jupiter's `assertAll(heading, executables...)` collects `Executable` lambdas, **executes every one of them, and reports all failures together**; within a single executable the hard-rule still applies (the dependent-assertion pattern above), but independent executables never hide each other. AssertJ's `SoftAssertions` is the fluent equivalent: instead of `assertThat(x).isEqualTo(y)` throwing, `SoftAssertions.assertSoftly(softly -> softly.assertThat(x)...` *records* assertion errors and `assertAll()` (called for you by `assertSoftly`, by the auto-closeable variant, by the JUnit 4 rule, or by the JUnit 5 extension that injects a `SoftAssertions` parameter) re-throws everything collected — the BDD flavor swaps `assertThat` for `then`. The idiomatic split: **Jupiter's `assertAll` for plain JUnit assertions**, **AssertJ soft assertions when the fluent API is already in use** — and the two nest: an `assertAll` block whose executables themselves contain soft-assertion checks still reports everything. What soft assertions do *not* change: the test still fails if anything failed — softness is about *completeness of the report*, not leniency.

## When which — the practical contract

The working rule: **hard by default; soft for a batch of independent validations of one artifact** — a response object, a DTO, a rendered page, a row in a table. The moment two checks have a *dependency* (check B reads what check A established), they belong in the same sequential block or in separate hard phases — softness across a dependency produces misleading secondary errors. AssertJ's own documentation frames the wrappers around exactly the pain point: forgetting the final `assertAll()` means **the soft assertions were recorded but never checked** — the test passes green while every soft check inside failed; that is why the auto-calling forms (JUnit 4 rule, JUnit 5 extension, `assertSoftly`, `AutoCloseableSoftAssertions`) exist and should be preferred to hand-managing a `SoftAssertions` instance. The interview-grade summary: hard assertions maximize *precision* (the first failure is the root cause), soft assertions maximize *throughput of information* (all independent failures in one run) — seniority is choosing deliberately per check, not picking a side. Catalogue: [[Which assertions does JUnit provide]]; hooks around them: [[What is a test fixture in JUnit]].

```java
// HARD: stops at the first failure - one bug per CI run
@Test
void hardOrderResponse() {
    Response r = api.getOrder(42);
    assertEquals(200, r.status());          // if this fails, nothing below runs
    assertEquals("Alice", r.body().customer());
    assertEquals(2,    r.body().items().size());
    assertEquals(NEW,  r.body().state());
    assertEquals(7550, r.body().total());
}

// SOFT (Jupiter): all failures reported together (MultipleFailuresError)
@Test
void softOrderResponse() {
    Response r = api.getOrder(42);
    assertAll("order response",
        () -> assertEquals(200, r.status()),
        () -> assertAll("body",              // independent checks - all reported
            () -> assertEquals("Alice", r.body().customer()),
            () -> assertEquals(2,    r.body().items().size()),
            () -> assertEquals(NEW,  r.body().state())),
        () -> assertAll("derived",           // dependent: guarded sequentially
            () -> assertNotNull(r.body().items()),
            () -> assertEquals(7550, r.body().total())));
}

// SOFT (AssertJ): assertSoftly auto-calls assertAll() at the end
@Test
void assertJSoft() {
    Response r = api.getOrder(42);
    SoftAssertions.assertSoftly(softly -> {
        softly.assertThat(r.status()).isEqualTo(200);
        softly.assertThat(r.body().customer()).isEqualTo("Alice");
        softly.assertThat(r.body().total()).isEqualTo(7550);
    });
}
```

**Listing 1.** Hard stops at the first failure; Jupiter's `assertAll` and AssertJ's `assertSoftly` report every independent failure in one run — with dependent checks still guarded.

```d2
direction: right
run: "one test run" {style.fill: "#e3f2fd"}
h1: "assert #1 FAILS" {style.fill: "#ffebee"}
h2: "asserts #2..n\nnever executed" {style.fill: "#eceff1"}
s1: "assertAll / SoftAssertions" {style.fill: "#fff8e1"}
s2: "assert #1 FAIL -> recorded" {style.fill: "#ffebee"}
s3: "asserts #2..n executed,\nfailures recorded" {style.fill: "#fff8e1"}
rep: "MultipleFailuresError:\nALL failures in one report" {style.fill: "#e8f5e9"}
run -> h1 -> h2
run -> s1
s1 -> s2 -> s3
s3 -> rep
```

**Fig. 1.** Hard assertions abort at the first failure; soft assertions execute every check and collapse all failures into a single report.

## Vocabulary the interview actually tests

Three items are graded. **Mechanism** — hard = throw immediately; soft = collect and report together; the exact Jupiter quote ("all failures will be reported together") and the `MultipleFailuresError` carrier show the docs were read. **The two soft APIs** — Jupiter's `assertAll` (lambdas) vs AssertJ's `SoftAssertions` (fluent, with the auto-`assertAll` wrappers: `assertSoftly`, the JUnit 5 extension, the JUnit 4 rule, auto-closeable). **Dependency awareness** — softness is for *independent* checks; dependent checks stay sequential (the guide's dependent-assertions pattern), and mixing them is how soft assertions produce noise. A senior bonus: soft assertions do not weaken the test — any recorded failure still fails it; and the classic AssertJ bug is hand-managing a `SoftAssertions` without the final `assertAll()`, which yields a green test that checked nothing — the reason the wrapper forms exist.

> [!warning] "Soft assertions are just lenient assertions" — they are batched reporting, not tolerance
> The misread that costs points: soft assertions never pass a test that has failures — every recorded error is re-thrown at `assertAll()`; softness only changes *when the run stops*, not *whether it passes*. The second trap is the forgotten final check: a `new SoftAssertions()` used by hand without `assertAll()` at the end records everything and verifies nothing — the test goes green with every soft check failed inside; use `assertSoftly`, the JUnit 5 extension, the JUnit 4 rule, or `AutoCloseableSoftAssertions` so the final check is structural. The third is softness across *dependencies*: after a null fails, the follow-up `.get()` assertions produce a shower of `NullPointerException`s that buries the one real cause — dependent checks belong in a sequential block, exactly as the guide's dependent-assertions example shows.

> [!tip] Interview answer
> **Hard assertions are the default: an assertEquals or assertTrue throws AssertionError on failure, so the test stops at the first failed check and later checks never run. Soft assertions run every check and report all failures together: in Jupiter that's assertAll — grouped assertions, all failures reported together in a MultipleFailuresError — and in AssertJ it's SoftAssertions, where assertSoftly or the JUnit 5 extension calls assertAll for you. Use hard for dependent checks where the next check only makes sense if the previous passed, and soft for a batch of independent validations of one artifact — verifying ten fields of an API response shows all the bugs in one CI run instead of one per run. And soft never means lenient: any recorded failure still fails the test.**
