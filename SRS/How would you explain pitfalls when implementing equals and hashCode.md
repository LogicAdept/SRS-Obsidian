<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Implementation #Java/Collections/Map/HashMap #Java/Arrays #Java/Immutability #Java/Persistence/JPA #SRS

# How would you explain pitfalls when implementing `equals` and `hashCode`?

> [!abstract] Short answer
> The expensive bugs are **half-overrides**, the **wrong signature**, a **hash that sees fields `equals` ignores**, **symmetry broken by subclasses**, **`==` on `float`/`double` or arrays**, and **mutating a key already in a hash table**. Each one still compiles. Hash-based collections then miss, duplicate, or lose entries.

## Contract and signature

`equals` must be `public boolean equals(Object o)`. `equals(Name n)` is an overload: `HashSet.contains` still calls `Object.equals`. Use `@Override`. If you override `equals`, override `hashCode` from the same logical fields. [[Why should equals and hashCode be overridden together]] and [[How do you override equals correctly in Java]] are the pair.

A field that `equals` ignores must not change `hashCode` if equal instances can disagree on it. A subset of equals-fields is legal and only increases collisions. [[How would you explain which fields should be included when implementing hashCode in Java]] is that rule.

```text
WRONG  equals(MyType)          // still identity in collections
WRONG  equals only             // equal keys, different buckets
WRONG  hashCode uses color     // equals uses only x, y
WRONG  x.equals(y) != y.equals(x)   // Point / ColorPoint
```

**Listing 1.** Failures that look like working Java.

## Types that are not identity

Primitive `==` on `float`/`double` is not an equivalence relation (`NaN`, signed zeros). Use representation equivalence. `arr.equals(other)` and `arr.hashCode()` are identity; content needs `Arrays.equals` / `hashCode` (or `deepEquals` / `deepHashCode`). `Objects.hash(single)` is not `single.hashCode()`. `Math.abs(hashCode())` stays negative for `Integer.MIN_VALUE`. [[What range of int values can hashCode return in Java]] is the range. [[How would you explain symmetry requirements for the equals contract in Java]] is the subclass trap.

## After the object is a key

The `Map` specification leaves behavior **unspecified** if you change a key in a way that affects `equals` while it sits in the map. `HashMap` keeps the insertion-time stored hash; a later `get` uses the new `hashCode` and typically never finds the node. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] is that path. Comparing copies with `==` instead of `equals` is a different lie: [[Why should arbitrary objects not be compared with double equals in Java]].

JPA entities add a lifecycle pitfall: a generated id is null, then set. If `hashCode` uses that id, the integer changes after `persist` while the instance may already be in a `Set`. Persistence identity is the primary key, not every column. [[In a business context must equals consider all entity fields]] is that policy.

> [!warning] Tests that only call `a.equals(b)`
> They miss overload-vs-override, `HashSet.contains` with a second instance, and mutation-after-`put`. Add a collection check and, for entities, a persist-then-lookup check.

> [!tip] Interview answer
> **Name the traps: wrong `equals` signature, missing `hashCode`, hashing extra fields, `instanceof` plus subclass state, `==` on floats or arrays, `Objects.hash(oneArg)`, and mutating a map key. The contract is easy to recite and easy to break in a way collections will not forgive.**
