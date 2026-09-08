<!--
reps: 0
priority: 0
-->
#Java/Testing/JUnit #Java/Annotations #SRS

# What is the JUnit Ignore annotation for?

> [!abstract] Short answer
> **JUnit 4’s `@Ignore`** (`org.junit.Ignore`) **skips** a `@Test` method or an entire test **class**. Those tests are **not executed**; a 4.x runner **reports them as ignored**, not as failures. Optional `value` records **why**. In **JUnit Jupiter** the replacement is **`@Disabled`**, not `@Ignore`.

## Skip without failing the build

`@Ignore` is `@Target({METHOD, TYPE})`, `@Retention(RUNTIME)`, with optional `String value()` (default `""`). A method with `@Test` **and** `@Ignore` is not run. On the class, **none** of its tests run. Use a reason: `@Ignore("not ready yet")`.

Jupiter’s analogue is `@Disabled` — same idea (class or method), **not inherited**. A disabled **method** skips `@BeforeEach` / `@AfterEach` for that method; the class may still be constructed and `@BeforeAll` / `@AfterAll` still run. A disabled **class** disables every test in it. The JUnit team wants a **reason** on `@Disabled` too.

`@Ignore` on a Jupiter test is the **wrong type**; Vintage runs JUnit 4, Jupiter looks for `@Disabled`. The fixture annotation mapping and the test fixture concept: [[What fixture annotations exist in JUnit]].

```java
@Ignore("flaky until #42")
@Test
public void something() { /* not run */ }

@Ignore
public class IgnoreMe {
    @Test public void test1() { }
    @Test public void test2() { }
}
```

**Listing 1.** JUnit 4 — method or class. Jupiter: `@Disabled("…")` on `org.junit.jupiter.api`.

```d2
direction: right
j4: "@Ignore\norg.junit" {
  width: 150
  height: 55
  style.fill: "#fff3e0"
}
j5: "@Disabled\norg.junit.jupiter.api" {
  width: 190
  height: 55
  style.fill: "#e8f5e9"
}
j4 -> j5: "Jupiter"
```

**Fig. 1.** Same job, different annotation and package.

> [!warning] `@Ignore` is not Jupiter
> Importing `org.junit.Ignore` in a `@Test` from `org.junit.jupiter.api` does **nothing** useful: Jupiter will **run** the test (or not see Ignore at all). `@Disabled` is **not** `@Inherited` — a subclass of a `@Disabled` class is **not** automatically disabled. Skipping is not a substitute for deleting a dead test; ignored counts hide rot.

> [!tip] Interview answer
> Ignore is JUnit 4’s way to leave a test or class in the suite without executing it; the runner counts it as ignored. Give a reason in the optional value. On JUnit 5/6 Jupiter you use Disabled instead; mixing Ignore onto Jupiter tests is a common migration miss.
