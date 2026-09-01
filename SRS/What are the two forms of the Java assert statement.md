<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# What are the two forms of the Java `assert` statement?

> [!abstract] Short answer
> **`assert cond;` and `assert cond : detail;`.** `cond` must be `boolean` or `Boolean`. The second form’s `detail` may be any type except `void`; on an enabled failure it becomes the `AssertionError` message. If assertions are off, both forms are no-ops.

## Simple vs detail

The statement has existed since Java 1.4 ([[In which Java version was the assert keyword introduced]]). Parentheses around `cond` (`assert (x > 10);`) are ordinary grouping, not part of the syntax.

**Simple form** — `assert cond;`

- Enabled and `cond` is `true`: the statement completes normally.
- Enabled and `cond` is `false`: throw `AssertionError` with no detail message.
- Disabled: nothing runs ([[How do you enable Java assertions at runtime]], [[What happens when a Java assert statement fails]]).

**Detail form** — `assert cond : detail;`

Same control flow, except a failed enabled assert evaluates `detail` and uses its value (string conversion) as the error message. `detail` is **not** evaluated when `cond` is `true`, or when assertions are off ([[When is the assert detail expression evaluated]]). A `void` method call is illegal here ([[Can the assert detail expression be a void method]]).

If `cond` has type `Boolean` and is `null`, unboxing throws `NullPointerException` before any `AssertionError`.

```d2
direction: down
forms: "assert statement" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
simple: "assert cond;\nno message" {
  width: 240
  height: 70
  style.fill: "#eceff1"
}
detail: "assert cond : detail;\nmessage from detail" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
forms -> simple
forms -> detail
```

**Fig. 1.** Two syntactic forms. The colon supplies an `AssertionError` message; it does not change when the check runs.

```java
class Demo {
    static void simple(int age) {
        assert age >= 18;
    }

    static void detailed(int index) {
        assert index >= 0 : "index must be non-negative, got " + index;
    }
}
```

**Listing 1.** Simple form vs detail form. With `-ea`, `simple(10)` throws `AssertionError` with no message; `detailed(-1)` throws one whose message includes the index. Without `-ea`, both return normally.

> [!warning] `detail` is not a second boolean
> The value after `:` is the error message, not another condition. It must not be `void`. Putting required work there (or in `cond`) is wrong: those expressions run only on an enabled failure (or, for `cond`, only when assertions are on).

> [!warning] `assert(x > 10)` is not a method
> Dumps wrap the condition in parentheses. That is still the statement. You cannot declare `void assert(boolean b)` to intercept it at a 1.4+ source level.

> [!tip] Interview answer
> **Two forms: `assert cond;` and `assert cond : detail;`.** The first throws a bare `AssertionError` on an enabled failure; the second uses `detail` as the message. `detail` is skipped when the condition is true or assertions are off, and it cannot be `void`.
