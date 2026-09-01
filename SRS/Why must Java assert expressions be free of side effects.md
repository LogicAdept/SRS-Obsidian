<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# Why must Java assert expressions be free of side effects?

> [!abstract] Short answer
> **Because the expressions may never run.** Assertions are off by default, and even when they are on, `detail` in `assert cond : detail;` runs only if `cond` is already `false`. Required mutation or I/O inside `assert` would change behavior depending on `-ea`. It is not a compile-time error — it is just wrong for anything the program still needs.

## The statement is optional at run time

A disabled `assert` evaluates neither `cond` nor `detail` ([[Why are Java assertions disabled by default]], [[How do you enable Java assertions at runtime]]). Programs must not assume those expressions execute. So they should not change state that is visible after the statement: no `list.remove(...)`, no `++n`, no logging the program relies on.

That still matters when assertions **are** enabled. `cond` is skipped if the JVM never hits the line; `detail` is skipped if `cond` is `true` ([[When is the assert detail expression evaluated]], [[What are the two forms of the Java assert statement]]). An assignment “hidden” after `:` is not a reliable increment.

Side effects are **legal**. They are generally **inappropriate**. The usual replacement when the check must always run is `if (...) throw ...` — especially for public arguments ([[When is it appropriate to use Java assertions]], [[Why should you not use assert to validate public method arguments]]).

They are not stripped by `javac` in the normal compilation. Disablement is a runtime default. (A `static final boolean` guard around `assert` can let the compiler fold them out; that is an extra idiom, not the default.)

```d2
direction: down
a: "assert expr with a mutation" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
off: "-ea absent\nmutation never happens" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
on: "-ea present\nmutation may happen" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
a -> off
a -> on
```

**Fig. 1.** Same source, two behaviors. Required work cannot live in `assert`.

```java
class Demo {
    static void broken(java.util.List<String> names) {
        // Wrong: removal disappears when asserts are off
        assert names.remove(null);
    }

    static void fixed(java.util.List<String> names) {
        boolean removed = names.remove(null);
        assert removed;
    }
}
```

**Listing 1.** `broken` only removes `null` under `-ea`. `fixed` always removes, then asserts that it did. Do not “fix” this by putting the assignment in the detail expression — that runs only on an enabled failure.

> [!warning] “Never any side effects” has one narrow exception
> State that is **only** read by other assertions (for example a copy taken under `assert` to check a postcondition later) is an accepted exception, because when asserts are off that state is unused. Visible program state is not that exception.

> [!warning] The compiler will not save you
> `assert n++ > 0;` compiles. With asserts off, `n` does not increment. With asserts on and `n` already `> 0`, the detail form `assert n > 0 : n++;` still would not increment. Use `if`/`throw` for a check that must always run.

> [!tip] Interview answer
> **Assert expressions must not matter when they are skipped, and they are skipped whenever asserts are off — which is the default.** The detail expression is also skipped when the condition is true. So do not mutate state or do required work there; use `if (...) throw ...` if the check has to run in production.
