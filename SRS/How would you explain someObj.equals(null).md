<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #SRS

# How would you explain `someObj.equals(null)`?

> [!abstract] Short answer
> **`false`**, when `someObj` is a non-null reference. The `Object.equals` contract requires that for any non-null `x`, `x.equals(null)` returns `false`. A correct override must do the same and must not throw on a null argument.

This is one clause of the full equivalence rules in [[How would you explain the Object equals method contract]]. It is not the same as calling a method on a null *receiver*.

## What the contract requires

`Object.equals` defines an equivalence relation on **non-null** references. The last rule is explicit: for any non-null reference value `x`, `x.equals(null)` should return `false`.

```d2
direction: down
recv: "someObj\n(non-null)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
call: "someObj.equals(null)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
ok: "false\n(contract)" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
badRecv: "someObj == null\n.then .equals(...)" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
npe: "NullPointerException\nbefore equals runs" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}

recv -> call -> ok
badRecv -> npe
```

**Fig. 1.** A null **argument** must yield `false`. A null **receiver** never reaches a correct `equals` body.

Default `Object.equals` is identity: it returns `true` only when the argument is the same object. A null argument is never the same object, so the default already returns `false`.

```java
Object someObj = new Object();
boolean result = someObj.equals(null); // false
```

**Listing 1.** Non-null receiver, null argument: contract answer is `false`.

## Overrides must keep the null rule

Any value-equality override still has to reject `null` up front. A common shape is an identity check, then a null / type check, then field comparisons:

```java
@Override
public boolean equals(Object o) {
    if (this == o) {
        return true;
    }
    if (o == null || getClass() != o.getClass()) {
        return false;
    }
    Point other = (Point) o;
    return x == other.x && y == other.y;
}
```

**Listing 2.** Conceptual value `equals`: `o == null` returns `false` before any field access. See [[How do you override equals correctly in Java]].

Throwing `NullPointerException` because the argument is null **violates** the contract. Returning `true` for null also violates it.

## Null-safe comparison of two possibly-null references

When either side may be null, do not write `a.equals(b)`. Use `Objects.equals(a, b)` (Java 7+): both null → `true`; exactly one null → `false`; otherwise `a.equals(b)`.

```java
Objects.equals(someObj, null); // false if someObj != null
Objects.equals(null, null);    // true
```

**Listing 3.** `Objects.equals` tolerates a null on either side; instance `equals` does not tolerate a null receiver.

[[How do you compare objects for equality in Java]] and [[Why should arbitrary objects not be compared with double equals in Java]] cover `==` versus `equals` more broadly.

> [!warning] Null receiver is a different bug
> Interview prompts often write `someObj.equals(null)` and assume `someObj` is live. If `someObj` itself is `null`, the expression throws **before** any `equals` logic. That NPE is ordinary method dispatch, not the equals-null contract.

> [!warning] “equals never NPEs” is too strong
> The contract forbids NPE for a **null argument** on a **non-null** receiver. A broken override can still throw. Field access on a null nested reference inside your own `equals` can also throw. Prefer an early `o == null` (or pattern matching) before touching the argument’s state.

> [!tip] Interview answer
> **`someObj.equals(null)` returns `false` if `someObj` is non-null.** That is part of the `Object.equals` contract, and overrides must keep it. If `someObj` is null, you get `NullPointerException` on the call itself — use `Objects.equals` when either reference may be null.
