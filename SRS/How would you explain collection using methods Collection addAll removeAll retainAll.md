<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS

# How would you explain collection bulk operations: `Collection` `addAll`, `removeAll`, `retainAll`?

> [!abstract] Short answer
> The four bulk methods are set algebra on any collection, in place: **`addAll` = union**, **`removeAll` = difference**, **`retainAll` = intersection**, and `containsAll` = the subset test. Each mutator returns `true` only when the collection actually changed, each is an optional operation (unmodifiable collections throw `UnsupportedOperationException`), and each matches elements through `equals` — hash-based implementations may shortcut with `hashCode` first.

## Contracts, not conveniences

The Javadoc pins each method down. `addAll(c)`: "adds all of the elements in the specified collection to this collection" — and its behavior is **undefined if the source collection is modified during the call, including when the source is the same nonempty collection**. `removeAll(c)`: "removes all of this collection's elements that are also contained in the specified collection" — after the call, the receiver shares nothing with `c`; for a `List` receiver that means *every* matching occurrence goes, not just the first. `retainAll(c)` keeps only elements also contained in `c`. `containsAll(c)` is the only pure query ([[What is collection]]).

```d2
direction: right
a: "A (receiver)" {
  width: 180
  height: 64
  style.fill: "#e3f2fd"
}
b: "B (argument)" {
  width: 180
  height: 64
  style.fill: "#fff3e0"
}
uni: "addAll(B)\nA ∪ B" {
  width: 190
  height: 64
  style.fill: "#e8f5e9"
}
diff: "removeAll(B)\nA \\ B" {
  width: 190
  height: 64
  style.fill: "#e8f5e9"
}
inter: "retainAll(B)\nA ∩ B" {
  width: 190
  height: 64
  style.fill: "#e8f5e9"
}
a -> uni
a -> diff
a -> inter
b -> uni
b -> diff
b -> inter: "matched via equals"
```

**Fig. 1.** The receiver mutates; the argument is untouched. Union grows, difference shrinks, intersection keeps the shared elements.

```java
Set<String> a = new HashSet<>(List.of("a", "b", "c"));
Set<String> b = new HashSet<>(List.of("b", "c", "d"));

System.out.println(a.addAll(b) + " " + a);      // union
Set<String> c = new HashSet<>(List.of("a", "b", "c"));
System.out.println(c.retainAll(b) + " " + c);   // intersection
Set<String> d = new HashSet<>(List.of("a", "b", "c"));
System.out.println(d.removeAll(b) + " " + d);   // difference
System.out.println(d.containsAll(Set.of("a"))); // subset test
```

**Listing 1.** Verified on JDK 21 — output: `true [a, b, c, d]` / `true [b, c]` / `true [a]` / `true`.

> [!warning] Bulk methods mutate the receiver and return a boolean — they do not produce a new collection
> `a.addAll(b)` is not `a ∪ b` as a value; it is a statement. That is why functional code reaches for `Set.copyOf` + `addAll` or `Stream.concat` instead, and why `a.addAll(a)` on a nonempty collection is undefined rather than a doubling. Passing a `List` argument does not preserve its duplicates — membership tests go through `equals`, so one matching element is enough ([[How do you compute the symmetric difference of two Java collections]]).

> [!tip] Interview answer
> **`addAll`, `removeAll`, `retainAll` are in-place set algebra — union, difference, intersection — plus `containsAll` as the subset query, all defined via `equals` and returning whether anything changed.** They throw `UnsupportedOperationException` on unmodifiable receivers, and `removeAll` on a list removes every occurrence of every matching element, not one.
