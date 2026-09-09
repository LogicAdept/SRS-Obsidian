<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# How do you compute the symmetric difference of two Java collections?

> [!abstract] Short answer
> The symmetric difference is the set of elements present in **exactly one** of the two collections. With `Collection` bulk operations: compute the intersection and subtract it from the union — `u = A ∪ B; i = A ∩ B; u.removeAll(i)` — or build the two one-sided differences and `addAll` them. Copy both inputs first: the bulk methods mutate their receiver, and on a `HashSet` the whole recipe runs in expected O(|A| + |B|).

## Two equivalent recipes

Both formulations come straight from the bulk-operation contracts ([[How would you explain collection using methods Collection addAll removeAll retainAll]]). Recipe A: union minus intersection. Recipe B: `(A \ B) ∪ (B \ A)` — two `removeAll` calls joined by `addAll`. The membership test behind both is `equals`, which is why `HashSet` is the natural receiver: it can decide membership in expected constant time instead of scanning ([[What is a HashSet]], [[How is HashSet implemented in terms of HashMap]]).

```d2
direction: right
a: "A\na · b · c" {
  width: 190
  height: 76
  style.fill: "#e3f2fd"
}
b: "B\nb · c · d" {
  width: 190
  height: 76
  style.fill: "#fff3e0"
}
sym: "A △ B\na · d\n(b, c in both — dropped)" {
  width: 280
  height: 92
  style.fill: "#e8f5e9"
}
a -> sym: "keep a (only in A)"
b -> sym: "keep d (only in B)"
```

**Fig. 1.** Elements shared by both sides fall out; the result keeps the ones that appear on a single side.

```java
Set<Character> a = new HashSet<>(List.of('a', 'b', 'c'));
Set<Character> b = new HashSet<>(List.of('b', 'c', 'd'));

Set<Character> union = new HashSet<>(a);  union.addAll(b);
Set<Character> inter = new HashSet<>(a);  inter.retainAll(b);
union.removeAll(inter);
System.out.println(union);                          // recipe A

Set<Character> diff = new HashSet<>(a);   diff.removeAll(b);
Set<Character> back = new HashSet<>(b);   back.removeAll(a);
diff.addAll(back);
System.out.println(diff);                           // recipe B
```

**Listing 1.** Verified on JDK 21 — output: `[a, d]` twice.

> [!warning] Never call the bulk methods on the input collections themselves
> `a.removeAll(b)` destroys `a`, so a second step silently works on garbage — always wrap inputs in fresh copies (`new HashSet<>(a)`). With `List` receivers the semantics drift too: `removeAll` strips *all* occurrences of shared elements, so the "symmetric difference" of two lists is defined by membership, not by position or count — that is why the set-typed copy is the honest medium.

> [!tip] Interview answer
> **Symmetric difference = union minus intersection, or equivalently the two one-sided differences combined: copy both sides, use `removeAll`/`retainAll`/`addAll` on the copies, and get elements belonging to exactly one input.** Use `HashSet` copies for expected O(n + m) time, mind that inputs are untouched, and remember that membership is `equals`-based, so hash-based sets also need a consistent `hashCode`.
