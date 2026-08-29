<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Can a try block exist without catch and finally?

> [!abstract] Short answer
> **Not as a plain `try`.** A `try` statement is either `try` + `catch`(es), `try` + `finally` (optional `catch`es), or try-with-resources. `try { ... }` by itself does not parse. Try-with-resources may omit both `catch` and `finally`; that form has been in the language since Java 7 with `AutoCloseable`.

## The grammar has no bare `try`

A non-resource `try` must attach at least one handler: one or more `catch` clauses, a `finally` block, or both. `try`/`finally` without `catch` is legal — that is a different question ([[Can you try-finally without catch]]).

```d2
direction: down
tryKw: "try { ... }" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
plain: "catch and/or finally\nrequired" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
twr: "try (resources) { ... }\ncatch and finally optional" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
tryKw -> plain: "no resource spec"
tryKw -> twr: "resource spec"
```

**Fig. 1.** Only a resource specification makes both `catch` and `finally` optional. See [[What forms of try catch and try with resources exist in Java]].

```java
class Demo {
    static void work() {}
    static void cleanup() {}

    static void tryCatch() {
        try {
            work();
        } catch (RuntimeException e) {
            throw e;
        }
    }

    static void tryFinally() {
        try {
            work();
        } finally {
            cleanup();
        }
    }
}
```

**Listing 1.** Two legal non-resource forms. `try { work(); }` with nothing after the block is a compile-time error.

## Try-with-resources may omit both

A try-with-resources statement is `try` ResourceSpecification Block, then optional `catch`es and an optional `finally`. With no `catch` and no `finally` it is a *basic* try-with-resources statement. `catch`/`finally` are often unnecessary because each resource is closed automatically after the `try` block, in reverse initialization order. See [[What is try-with-resources]].

Every resource's type must be a subtype of `AutoCloseable`, or the statement does not compile. The resource specification is `(` ResourceList [`;`] `)` with a **non-empty** resource list (one or more resources).

```java
class Handle implements AutoCloseable {
    @Override
    public void close() {}
}

class Demo {
    static void use() {
        try (Handle h = new Handle()) {
            // no catch, no finally
        }
    }
}
```

**Listing 2.** Legal basic try-with-resources. `Handle.close()` declares no checked exceptions, so `use` needs no `throws`.

> [!warning] Empty parentheses are not a bare `try`
> `try () { work(); }` is not a resource specification. The list must contain at least one resource. That is still a compile-time error, not a loophole around the no-bare-`try` rule.

> [!warning] Omitting `catch` does not cancel `close()`'s checked exceptions
> `AutoCloseable.close()` is declared `throws Exception`. If the actual resource's `close` can throw a checked type, a basic try-with-resources *statement* is still legal, but the enclosing method or constructor must catch or declare that type. No `catch` on the `try` does not mean "no checked exceptions from this statement."

> [!tip] Interview answer
> **A plain `try` must be followed by `catch`, `finally`, or both — `try { }` alone does not compile. Try-with-resources may omit both, because the compiler closes `AutoCloseable` resources after the block. `try`/`finally` without `catch` is valid, but that is still a `finally`, not a try with neither clause.**
