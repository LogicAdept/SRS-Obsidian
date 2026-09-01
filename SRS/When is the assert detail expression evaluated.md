<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# When is the assert detail expression evaluated?

> [!abstract] Short answer
> **Only when assertions are enabled and the condition is already `false`.** If assertions are off, or the condition is `true`, `detail` in `assert cond : detail;` is not evaluated. That is why a mutating `detail` (such as `++x`) must not be required program logic.

## Enabled failure only

The second form is `assert cond : detail;` ([[What are the two forms of the Java assert statement]]). Execution:

1. **Disabled** — neither `cond` nor `detail` runs; the statement is a no-op ([[How do you enable Java assertions at runtime]], [[Why are Java assertions disabled by default]]).
2. **Enabled** — evaluate `cond` (`boolean` or `Boolean`). If it is `true`, stop; `detail` is skipped.
3. If `cond` is `false`, evaluate `detail`. Its value becomes the `AssertionError` message (string conversion). A `void` `detail` is a compile-time error ([[Can the assert detail expression be a void method]], [[What happens when a Java assert statement fails]]).

If evaluating `detail` throws, that exception (or error) completes the `assert` — no `AssertionError` is created from a value that never existed. If `cond` is a `null` `Boolean`, unboxing throws `NullPointerException` before `detail` runs.

```d2
direction: down
stmt: "assert cond : detail" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
off: "assertions off\ndetail skipped" {
  width: 260
  height: 70
  style.fill: "#eceff1"
}
ok: "cond true\ndetail skipped" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
eval: "cond false\nevaluate detail" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
stmt -> off
stmt -> ok
stmt -> eval
```

**Fig. 1.** `detail` runs on one path only: enabled and `cond` already false.

```java
class Demo {
    static int x = 10;

    static void demo() {
        assert x == 10 : ++x; // teaching only — do not mutate in detail
    }
}
```

**Listing 1.** With `-ea` and `x == 10`, `++x` does not run; `x` stays `10`. With assertions off, `++x` does not run either. If you wrote `assert x != 10 : ++x` and enabled asserts, `++x` would run, then `AssertionError` would carry message `11`.

> [!warning] Dumps that say “iff the boolean is false” omit the enablement half
> False is not enough. Without `-ea`, a false condition still does not evaluate `detail`. Never put required mutation or I/O there ([[Why must Java assert expressions be free of side effects]]).

> [!warning] `++x` in `detail` is a classroom trick
> It demonstrates skip-vs-eval. It is not a style to copy: assertion expressions should not change state that the rest of the program can see.

> [!tip] Interview answer
> **The expression after `:` runs only if assertions are on and the condition has already come out false.** If the condition is true, or asserts are off, it is not evaluated at all. That is why you must not put needed side effects in the detail.
