<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/OOP #Java/Language/Records #Java/Versions/16 #SRS

# How would you explain default `equals` and `hashCode` inherited from `Object`?

> [!abstract] Short answer
> If you do not override them, two references are equal only when they are the **same instance**, and each instance has its own hash (distinct when the JVM can manage it). Field-by-field copies are **not** equal. That is the right default for objects with unique identity. It is the wrong default for values you intend to look up in a `HashMap` by content.

## What you get by writing nothing

```java
Point a = new Point(1, 2);
Point b = new Point(1, 2);
a == b;          // false
a.equals(b);     // false  (inherited Object.equals)
a.hashCode() == b.hashCode(); // typically false
```

**Listing 1.** Conceptual ordinary class with fields `x` and `y` and no overrides. Same numbers, different objects.

Hash-based collections then key by identity: `map.put(a, "A")` is not retrieved with `map.get(b)`. `HashSet` will hold both `a` and `b`. That is consistent, not a collection bug. [[How are hashCode and equals implemented in java.lang.Object]] is why. Arrays behave the same: `new int[]{1}.equals(new int[]{1})` is false; use `Arrays.equals`.

```d2
direction: down
keep: "Keep Object defaults" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
id: "Identity matters\n(thread, socket, listener)" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
val: "Value lookup in HashMap\n(coordinate, money, id)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
override: "Override equals and hashCode" {
  width: 280
  height: 70
  style.fill: "#ffe0b2"
}

keep -> id
keep -> val -> override
```

**Fig. 1.** Inherited identity is a choice. Value types must replace both methods. [[When should you override equals in Java]] is that decision.

## When the default is what you want

Keep it when each instance is unique in the domain: a mutable service, a thread, a GUI listener, an object you only ever look up with the **same reference** you stored. Then you must not override one method and leave the other. [[Why should equals and hashCode be overridden together]] is the half-override failure.

A `record` does **not** keep this default; it already equals and hashes by components. `IdentityHashMap` ignores your overrides and compares with `==` and identity hashes, which is the inherited `Object` pair applied even to value classes. [[What is the difference between HashMap and IdentityHashMap]] is when that is deliberate.

> [!warning] “Same fields means equals”
> Not with the inherited methods. Unit tests that only print fields will lie. `String`, `Integer`, and lists override the pair; your domain class does not unless you (or a `record`) say so. Comparing with `==` on those library types is a different mistake: [[Why should arbitrary objects not be compared with double equals in Java]].

> [!tip] Interview answer
> **Inherited `equals`/`hashCode` are identity: one object, one equivalence class, one hash. Two `new` instances with identical fields are not equal and usually not in the same `HashMap` bucket. Keep that for unique identities; override both for value types you want to look up by content.**
