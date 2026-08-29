<!--
reps: 0
priority: 0
-->
#Java/Exceptions #SRS

# Which keyword throws an exception in Java?

> [!abstract] Short answer
> **`throw`.** It is a statement that actually throws a `Throwable`. **`throws` does not throw** — it only declares checked exceptions a method or constructor may propagate. `throw` is not an operator.

## `throw` throws; `throws` declares

`throw expr;` evaluates `expr` and completes abruptly with that exception. The value must be a `Throwable`. `throw null;` becomes `NullPointerException` ([[Can you throw an object that is not a Throwable]], [[Which operator allows throw exception]]). Control then searches for a matching `catch` or continues to the caller.

`throws` is part of a method or constructor declaration. For a **checked** exception, the compiler requires `catch` or `throws` on that path. Unchecked exceptions (`RuntimeException`, `Error`) need no `throws` ([[How would you explain the throws clause for checked exceptions]], [[Must you declare RuntimeException in a throws clause]], [[What does keyword word throws]]).

A method can list types in `throws` and still never execute `throw` itself — a called method may throw. Conversely, `throw new IllegalStateException("x")` needs no `throws` clause.

```d2
direction: down
kw: "keyword" {
  width: 240
  height: 50
}
th: "throw expr;" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
decl: "throws Type" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
kw -> th: "does the throw"
kw -> decl: "only declares"
```

**Fig. 1.** `throw` is the action. `throws` is the signature.

```java
class Demo {
    static void fail() throws java.io.IOException {
        throw new java.io.IOException("disk");
    }
}
```

**Listing 1.** `throw` throws. `throws IOException` only tells callers the checked type may leave `fail`.

> [!warning] `throw` vs `throws` is a standard mix-up
> `throws` on the method line does not throw anything by itself. Without a `throw` (here or in a callee), nothing is thrown.

> [!warning] `throw` is a statement
> It is not a binary or unary operator. The operand is an expression that yields a `Throwable`.

> [!tip] Interview answer
> **The keyword that throws is `throw`.** `throws` only declares checked exceptions on a method or constructor. You write `throw new SomeException(...)`; you write `throws` next to the method name.
