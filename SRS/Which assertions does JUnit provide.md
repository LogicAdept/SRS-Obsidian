<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #SRS

# Which assertions does JUnit provide?

> [!abstract] Short answer
> Jupiter's assertion catalogue lives in **`org.junit.jupiter.api.Assertions`** as static methods: equality and comparison — **`assertEquals`** (primitive/`Object`/arrays overloads), **`assertNotEquals`**, **`assertSame`**/`assertNotSame` (identity, `==`); booleans — **`assertTrue`**, **`assertFalse`**; nullness — **`assertNull`**, **`assertNotNull`**; exceptions — **`assertThrows(Class, Executable)`** ("returns the exception for further verification" — the guide's samples then call `exception.getMessage()`), **`assertDoesNotThrow`** (per the guide: used "when you want to verify that a particular piece of code does not throw any exceptions"); grouping — **`assertAll(heading, executables...)`** ("all assertions are executed, and all failures will be reported together"); time — **`assertTimeout`** and **`assertTimeoutPreemptively`** (a duration plus an executable); and the explicit failure — **`fail()`**. All take an optional last-argument message or `String`/`Supplier<String>` message supplier. The guide also blesses third-party assertion libraries — "third-party assertion libraries" — of which **AssertJ** is the common choice: `assertThat(frodo.getName()).startsWith("Fro").endsWith("do")` — fluent chains over the same semantics. Grouping details: [[What is the difference between hard and soft assertions]]; where assertions run: [[What is a test fixture in JUnit]].

## The value catalogue: equality, identity, booleans, nullness

The everyday core is small and worth knowing exactly. **`assertEquals(expected, actual)`** compares by `.equals()` — and the *argument order matters for the failure message*, not for pass/fail: the report renders "expected X, actual Y", so swapping the arguments turns a correct failure report into a backwards one. **`assertSame`** is the deliberate outlier: it compares *identity* (`==`), the right tool for singletons, cached instances, and tests asserting two variables reference the same object — and the wrong tool for anything relying on `equals` semantics. **`assertTrue`/`assertFalse`** take conditions; a compound condition (`a != null && a.isValid()`) hides *which* conjunct failed, so senior tests prefer specific assertions over compound booleans. **`assertNull`/`assertNotNull`** guard presence before deeper checks. Array/collection variants — `assertArrayEquals`, plus `assertIterableEquals`/`assertLinesMatch` — compare ordered contents element-wise. Every method accepts an optional message; the supplier overload (`assertEquals(e, a, () -> "context for " + id)`) defers string building until the assertion actually fails — the same lazy-formatting discipline as parameterized logging.

## The exception and time catalogues

**`assertThrows(Class<T>, executable)`** is the exception workhorse: it fails the test if nothing was thrown or the wrong type was thrown, and *returns the caught exception* so the test can inspect it further — message, cause, state mutated alongside the throw: `ArithmeticException e = assertThrows(ArithmeticException.class, () -> calc.divide(10, 0)); assertEquals("/ by zero", e.getMessage())`. Its counterpart **`assertDoesNotThrow`** asserts normal completion (and returns the executable's result). The type check follows standard exception semantics — a thrown subclass of the expected type passes. **Time assertions** wrap an executable with a deadline: **`assertTimeout`** runs the code and fails *after* it finishes if the budget was exceeded (the test always waits for completion); **`assertTimeoutPreemptively`** fails *at* the deadline by running the executable in a separate thread and abandoning it — sharper enforcement, but the abandoned thread may hold resources, which is why Jupiter documents the trade-off and seniors reserve preemptively for genuine "must not hang" cases. For grouped checks and multiple failures in one report, `assertAll` is the soft-assertion primitive ([[What is the difference between hard and soft assertions]]).

## Beyond built-ins: AssertJ and friends

The guide explicitly endorses third-party assertion libraries as the fluent complement, and AssertJ is the default in modern codebases: `assertThat(actual).isEqualTo(expected)` chains type-specific checks — `.startsWith("Fro").endsWith("do")` on strings, `.hasSize(9)` on collections — so the IDE's completion lists *all* applicable checks and failure messages describe the mismatch richly. Hamcrest serves the same goal via matcher expressions (`assertThat(value, hasProperty("name", equalTo("Frodo")))`) — historically the JUnit 4 idiom via `org.hamcrest.MatcherAssert.assertThat`. When asked "which assertions do you use", the strong answer is the *split*: Jupiter's `Assertions` for the basic vocabulary and anything framework-internal, AssertJ for domain-heavy reading (`assertThat(orders).filteredOn(o -> o.isNew()).hasSize(2)`), and the knowledge that all of them are **hard** by default — softness comes only from `assertAll`/`SoftAssertions`. The catalogue's edge cases complete the picture: `fail("reason")` aborts deliberately (unfinished tests, impossible branches), and the whole family lives in `Assertions` — statically imported in real tests.

```java
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class CalculatorTest {
    Calculator calc = new Calculator();

    @Test void values() {
        assertEquals(2, calc.add(1, 1));                    // equals()
        assertNotSame(new Calculator(), calc);              // identity ==
        Calculator c = Calculator.shared();                 // singleton check
        assertSame(Calculator.shared(), c);
        assertTrue(calc.isRunning(), () -> "state: " + calc.state()); // lazy msg
        assertNotNull(calc.history());
    }

    @Test void exceptions() {
        // returns the exception -> inspect it further
        ArithmeticException e =
            assertThrows(ArithmeticException.class, () -> calc.divide(10, 0));
        assertEquals("/ by zero", e.getMessage());
        assertDoesNotThrow(() -> calc.divide(10, 2));
    }

    @Test void groupedAndTimed() {
        assertAll("calculator state",                       // all failures reported
            () -> assertEquals(2, calc.add(1, 1)),
            () -> assertTrue(calc.isRunning()));
        assertTimeout(java.time.Duration.ofMillis(100),
                      () -> calc.heavyComputation());       // fails after completion
    }
}
```

**Listing 1.** The catalogue in use: value assertions with lazy messages, `assertThrows` returning the exception for inspection, `assertAll` grouping, and a timeout budget.

```d2
direction: right
a: "Assertions\n(static, org.junit.jupiter.api)" {style.fill: "#e3f2fd"}
val: "values\nequalsEquals / assertSame /\nassertTrue / assertNull" {style.fill: "#e8f5e9"}
exc: "exceptions\nassertThrows -> returns ex /\nassertDoesNotThrow" {style.fill: "#fff8e1"}
soft: "grouping\nassertAll -> all failures\nreported together" {style.fill: "#f3e5f5"}
time: "time\nassertTimeout (wait) /\nassertTimeoutPreemptively (abort)" {style.fill: "#ffebee"}
fluent: "third-party fluent\nAssertJ assertThat(x).isEqualTo(y)\nHamcrest assertThat(x, is(y))" {style.fill: "#eceff1"}
a -> val
a -> exc
a -> soft
a -> time
a -> fluent
```

**Fig. 1.** The catalogue at a glance: value, exception, grouping and time families — plus the fluent third-party layer on the same semantics.

## Vocabulary the interview actually tests

Four items are graded. **The families** — value (equals/identity/boolean/nullness), exception (`assertThrows` returning the exception), grouping (`assertAll`), time (`assertTimeout` vs *preemptively*); reciting only `assertEquals/assertTrue` is the floor, not the answer. **`assertEquals(expected, actual)` order** — irrelevant to pass/fail, decisive for the failure report. **`assertSame` vs `assertEquals`** — identity vs `equals()`; the singleton and cache tests depend on it. **Fluent layer** — AssertJ (or Hamcrest) chains on top; knowing *when* to prefer which reads as production experience. A senior bonus: the message-supplier overload for lazy strings, `fail()` for impossible branches, and that everything here is hard — the first failure stops the method unless wrapped in `assertAll`.

> [!warning] "assertEquals(a, b) — the order is just style" — it is the failure report's contract
> The slips this question catches: **swapped arguments** (`assertEquals(calc.add(1,1), 2)`) — the test still passes/fails identically, but every failure message now reports "expected 2, actual 3" backwards, misleading whoever debugs it. **`assertSame` used where `equals` was meant** — a `String` or DTO comparison "works" until two equal-but-distinct instances appear, then fails mysteriously (and `String` literals interning can make the mistake pass *in tests* and fail in production data). **`assertTimeoutPreemptively` on code holding resources** — the deadline kills the *wait*, not the work; the abandoned thread may still own a lock or a connection. And the AssertJ variant: fluent chains that were never checked because the enclosing `SoftAssertions` missed its `assertAll()` — a green test that verified nothing (see [[What is the difference between hard and soft assertions]]).

> [!tip] Interview answer
> **Jupiter's Assertions class gives five families, all static. Values: assertEquals by equals — expected first, the order shapes the failure message — assertSame for identity, assertTrue/assertFalse, assertNull/assertNotNull, plus array and iterable variants. Exceptions: assertThrows with the expected type and a lambda — it returns the caught exception so you can assert its message or cause — and assertDoesNotThrow. Grouping: assertAll runs every check and reports all failures together. Time: assertTimeout and assertTimeoutPreemptively, which aborts at the deadline in a separate thread. And on top of the built-ins, AssertJ's assertThat chains give type-specific checks and richer messages — that's the usual pairing in real codebases.**
