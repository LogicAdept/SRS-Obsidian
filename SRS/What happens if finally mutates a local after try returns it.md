<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# What happens if `finally` mutates a local after `try` returns it?

> [!abstract] Short answer
> **The caller still gets the value that `return` already computed.** `return x` evaluates `x` first (that value `V` is the reason for abrupt completion). Then `finally` runs. Assigning a new value to the local does **not** change `V`. If `x` is a reference to a **mutable** object, `finally` can still mutate that object, so the caller sees field/content changes even though the returned reference is the one saved before `finally`.

## The return expression is evaluated before `finally`

A `return` with an expression evaluates that expression to a value `V`, then completes abruptly for “return with value `V`.” Any enclosing `finally` runs next. If `finally` completes **normally**, the method still returns that same `V`. Rebinding the local (`x = 2`, `x = other`) happens after `V` was taken, so it is invisible to the caller ([[How would you explain the finally block in Java]], [[How would you explain try-catch-finally]], [[Is a finally block always executed in Java]]).

If `finally` itself completes abruptly (`return`, `throw`), that new reason **replaces** the saved return ([[What happens if finally returns after try throws an exception]], [[What happens if try and finally both throw an exception]]). That is a different rule from mutating a local.

When `V` is a reference, it still points at the same object. `finally` may call methods or assign fields on that object. The caller’s variable is that reference, so those mutations are visible. Replacing the local with a different object is not.

```d2
direction: down
eval: "return x\nV = current value of x" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
fin: "finally runs" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
assign: "x = newValue\nV unchanged" {
  width: 280
  height: 70
  style.fill: "#eceff1"
}
mut: "x.append(...) / x.f = ...\nobject behind V mutates" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
out: "caller receives V" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
eval -> fin
fin -> assign
fin -> mut
assign -> out
mut -> out
```

**Fig. 1.** Saved `V` vs mutating the object `V` refers to.

```java
class Demo {
    static int primitive() {
        int x = 1;
        try {
            return x;
        } finally {
            x = 2;
        }
    }

    static StringBuilder mutate() {
        StringBuilder x = new StringBuilder("a");
        try {
            return x;
        } finally {
            x.append("b");
        }
    }

    static StringBuilder rebind() {
        StringBuilder x = new StringBuilder("a");
        try {
            return x;
        } finally {
            x = new StringBuilder("z");
        }
    }
}
```

**Listing 1.** `primitive()` returns `1`. `mutate()` returns a builder whose content is `"ab"`. `rebind()` still returns the original `"a"` builder. A `return` **inside** `finally` would discard `V` entirely.

Control does not re-enter the `try` block after `finally` ([[Does control return to the try block after a catch handles an exception]]). There are no statements between `try`/`catch`/`finally` ([[Can you place statements between try catch and finally]]).

> [!warning] Interview questions mix two different `finally` tricks
> Mutating the **local** after `return x` does not change the saved value. `return` **from** `finally` replaces that value (and can swallow a throw from `try`). Read the snippet: assignment vs `return` in `finally`.

> [!warning] Reference mutation looks like “`finally` changed the return”
> For `StringBuilder` / arrays / beans, the **reference** was saved, not a snapshot of the contents. `finally` can still edit the object. A primitive or an immutable `String` does not show that effect.

> [!tip] Interview answer
> **`return x` snapshots the value of `x`, then `finally` runs, then that snapshot is returned.** Assigning the local in `finally` does not change it. If `x` is a mutable object, mutating that object is visible. A `return` in `finally` is a different rule: it replaces the saved return.
