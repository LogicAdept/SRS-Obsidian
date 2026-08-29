<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Exceptions/Error #SRS

# What happens when a Java `assert` statement fails?

> [!abstract] Short answer
> **If assertions are enabled and the condition is `false`, the statement throws `AssertionError`.** The simple form `assert cond;` has no detail message. The form `assert cond : detail;` uses the string conversion of `detail` as the error message. If assertions are **disabled**, the statement is a no-op: neither expression runs, and nothing is thrown even when `cond` would be false.

## Enabled failure vs disabled skip

An `assert` is either enabled or disabled for its top-level class. Disabled: execution has no effect — `cond` and `detail` are not evaluated ([[Why are Java assertions disabled by default]], [[How do you enable Java assertions at runtime]], [[Why must Java assert expressions be free of side effects]]).

Enabled: evaluate `cond` (`boolean` or `Boolean`). If it is `true`, the statement completes normally. If it is `false`, the statement completes abruptly by throwing a newly created `AssertionError` ([[What is the purpose of the assert keyword in Java]], [[What are the two forms of the Java assert statement]]).

`AssertionError` extends `Error`, so it is **unchecked**: you do not declare `throws AssertionError`. It is not a subclass of `Exception`. `catch (Exception e)` does not catch it. It is legal to catch, but it is intended not to ([[Is AssertionError a subclass of Exception]], [[Should you catch AssertionError]], [[Are Error subclasses checked or unchecked]]).

The detail expression is evaluated **only** when the enabled condition is already `false`. Its value becomes the `AssertionError` message (string conversion). It must not be `void` ([[When is the assert detail expression evaluated]]).

Do not use `assert` to validate public arguments; a failed check should be `IllegalArgumentException` / `NullPointerException`, and those checks must run when asserts are off ([[Why should you not use assert to validate public method arguments]]).

```d2
direction: down
assert: "assert cond : detail" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
off: "assertions disabled\nnothing happens" {
  width: 280
  height: 70
  style.fill: "#eceff1"
}
ae: "cond is false\nAssertionError" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ok: "cond is true\ncontinue" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
assert -> off
assert -> ae
assert -> ok
```

**Fig. 1.** Failure is an `Error`, and only when assertions are on.

```java
class Demo {
    static void simple(int x) {
        assert x > 10;
    }

    static void detailed(int x) {
        assert x > 10 : "x should be >10 but is " + x;
    }
}
```

**Listing 1.** With `-ea`, `simple(3)` throws `AssertionError` with no message; `detailed(3)` throws `AssertionError` whose message includes the detail string. Without `-ea`, both calls return normally.

> [!warning] Dumps say “exception”; the type is `Error`
> Casual speech calls any throw an exception. `AssertionError` is an `Error`. It is not a checked exception you must declare, and `catch (Exception)` will miss it.

> [!warning] A `Boolean` condition can NPE instead
> If `cond` has type `Boolean` and is `null`, unboxing throws `NullPointerException` before any `AssertionError`. That is not an assertion failure.

> [!tip] Interview answer
> **Enabled `assert` with a false condition throws `AssertionError` — an unchecked `Error`, not something you declare.** The `: detail` form supplies the message. If assertions are off, the statement is skipped entirely.
