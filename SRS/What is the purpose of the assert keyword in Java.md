<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# What is the purpose of the assert keyword in Java?

> [!abstract] Short answer
> **`assert` is a statement that checks a boolean you believe is always true.** Enabled, a `false` condition throws **`AssertionError`**. Disabled, it is a **no-op** — neither the condition nor the optional detail is evaluated. It is for **internal invariants**, not a public contract.

## A check that can be switched off

JLS **§14.10**: an assertion is enabled or disabled. Enabled: evaluate the boolean and report an error if it is `false`. Disabled: **no effect whatsoever**. Typical use is **on in development and testing, off in deployment**.

Two forms ([[What are the two forms of the Java assert statement]]): `assert cond;` and `assert cond : detail;`. `detail` must not be `void`. On an enabled failure the JVM throws `java.lang.AssertionError`; the detail value is string-converted and becomes the error message ([[What happens when a Java assert statement fails]]). Enable at launch with **`-ea`** ([[How do you enable Java assertions at runtime]]).

Because a disabled `assert` does not run, the boolean (and `detail`) **must not be required work**. Side effects are not illegal, but they make behavior depend on `-ea` ([[Why must Java assert expressions be free of side effects]]). Public-argument checking belongs on `IllegalArgumentException` / `NullPointerException`, not `AssertionError` ([[Why should you not use assert to validate public method arguments]], [[When is it appropriate to use Java assertions]]).

```java
void afterPut(int size, int expected) {
    assert size == expected : size;
}
```

**Listing 1.** Internal postcondition. With `-ea`, a mismatch throws `AssertionError` whose message is the actual size. Without `-ea`, the method returns even if `size` is wrong.

```d2
direction: down
stmt: "assert cond\n[: detail]" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
on: "enabled\nevaluate cond" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
off: "disabled\nno-op" {
  width: 180
  height: 50
  style.fill: "#eceff1"
}
err: "false → AssertionError" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}

stmt -> on
stmt -> off
on -> err
```

**Fig. 1.** The keyword’s job is a **switchable** invariant check, not a substitute for `if` + throw on a published API.

> [!warning] Not compile-time stripping by default
> Disabling is a **runtime** assertion status (JLS). Optional class-file stripping is a separate toolchain choice. Do not write `assert` as if the compiler always deletes it.

> [!warning] `assert` is a statement, not an operator
> There is no `assert` expression. Parentheses around the condition are ordinary grouping.

> [!tip] Interview answer
> **assert checks an internal boolean; failure is AssertionError.** Turn it on with -ea while you develop; off, the statement does nothing, so do not put required mutations or public-argument checks there. Two forms: with and without a detail message.
