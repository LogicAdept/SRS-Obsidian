<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/Language #SRS

# How does Java decide whether two objects are equivalent?

> [!abstract] Short answer
> It calls **`equals` on the receiver**. The method is virtual: `Object.equals` is identity (`x == y`); a class that overrides it defines its own logical value. There is no separate language-level “structural equality” for ordinary objects. Hash tables and lists consult that same `equals` (after a hash, or element-wise). `==` and `Comparator.compare` answer different questions.

## The decision is a method call

```java
a.equals(b);           // a's runtime class decides
Objects.equals(a, b);  // both null → true; else a.equals(b) if a != null
```

**Listing 1.** Equivalence of two references is `equals`, not a compiler comparison of fields. `Objects.equals` only adds a null-safe dispatch.

`Object.equals` implements the most discriminating equivalence relation: each non-null instance is its own class. An override may coarsen that partition so distinct instances are substitutable “at least for some purposes.” That wording is in the `equals` specification. [[How would you explain the Object equals method contract]] lists the five rules the override must still obey.

```d2
direction: down
q: "Are a and b equivalent?" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
id: "==  (same object or both null)" {
  width: 280
  height: 70
  style.fill: "#eceff1"
}
eq: "a.equals(b)\n(runtime override)" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
ord: "compare(a,b) == 0\n(order, not Map equality)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}

q -> id
q -> eq
q -> ord
```

**Fig. 1.** Three relations. Collections that document equality (`HashMap`, `List.equals`, `Set`) use `equals`. Sorted maps use compare and misbehave if that order is inconsistent with `equals`.

## What collections actually ask

`HashMap` locates a bin from `hashCode`, then treats keys as the same mapping when identity or `equals` holds. `List.equals` is true when both are lists of the same size and corresponding elements satisfy `Objects.equals`. Neither inspects your fields unless your `equals` does.

`Comparator` defines a **total order**. `compare(a, b) == 0` is an equivalence (the quotient of the order). It matches `equals` only when the comparator is **consistent with equals**. A `TreeSet` with an inconsistent comparator can contain two elements that `equals` says are the same, contrary to `Set.add`. That is not how Java “decides equivalence” in general; it is a second relation you opted into. [[How would you explain default equals and hashCode inherited from Object]] is the default partition.

> [!warning] `==` is not the equivalence test for values
> For two references, `==` is true only when both are `null` or both denote the same object. Distinct `String`s with the same characters are not `==`. Contents are `s.equals(t)`. [[Why should arbitrary objects not be compared with double equals in Java]] is that operator.

> [!tip] Interview answer
> **Java decides object equivalence by `equals` on the left operand. The default is identity; an override defines value equality and must remain an equivalence relation. Hash maps and lists use that method. `==` tests the same reference. `compare == 0` is ordering and matches `equals` only if you keep them consistent.**
