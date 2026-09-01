<!--
reps: 0
priority: 0
-->
#Java/Collections/Set #SRS

# How do you compute union, intersection, and difference of two Sets?

> [!abstract] Short answer
> **Copy into a mutable `Set`, then `addAll` (union), `retainAll` (intersection), or `removeAll` (asymmetric difference).** Those three bulk mutators *are* the collections-framework set algebra. They change the receiver; they do not allocate a new set.

## The three bulk operations

On `Set` since **1.2**, each method is an optional operation. When the argument is also a `Set`:

- `a.addAll(b)` — `a` becomes **A ∪ B**
- `a.retainAll(b)` — `a` becomes **A ∩ B**
- `a.removeAll(b)` — `a` becomes **A \ B** (asymmetric difference, not B \ A)

Each returns `true` when the receiver changed. `containsAll` is the related **subset** test, not a fourth mutator. There is no `Set.union` / `Set.intersection` factory.

General-purpose implementations supply a copy constructor. `new HashSet<>(a)` is a new set with the same elements, so the original `a` is left alone ([[What is a HashSet]], [[What does Set.of return and what happens with duplicates]]).

```d2
direction: right
copy: "result = new HashSet<>(a)" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
op: "result.addAll(b)\nresult.retainAll(b)\nresult.removeAll(b)" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
out: "union / intersection / A minus B" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

copy -> op
op -> out
```

**Fig. 1.** Algebra lives on a **mutable** receiver. Copy first when the caller still needs the original set.

```java
Set<Integer> a = Set.of(1, 2, 3);
Set<Integer> b = Set.of(3, 4, 5);

Set<Integer> union = new HashSet<>(a);
union.addAll(b);              // members {1, 2, 3, 4, 5}

Set<Integer> intersection = new HashSet<>(a);
intersection.retainAll(b);    // members {3}

Set<Integer> difference = new HashSet<>(a);
difference.removeAll(b);      // members {1, 2}
```

**Listing 1.** Copy, then mutate the copy. `a` and `b` stay unchanged (`Set.of` cannot be mutated). `removeAll` is A minus B; copying `b` and `removeAll(a)` is B minus A.

## Who gets iterated

`HashSet` inherits `retainAll` from `AbstractCollection`: it walks **this** set and keeps an element only when the **argument** `contains` it. `HashSet.contains` is expected constant time, so `new HashSet<>(smaller).retainAll(larger)` does about `|smaller|` lookups. Copying the larger set instead walks the larger one.

`removeAll` on `AbstractSet` (and therefore `HashSet` / `TreeSet`) compares `size()` and iterates the **smaller** side: either this set with `c.contains`, or `c` with `this.remove`. Two hash sets are usually cheap. Mixing a hash set with a `List` (linear `contains`) or a `TreeSet` (comparator membership, not `equals`) can make both cost and *which* membership test runs depend on relative sizes ([[How do HashSet and TreeSet decide whether two elements are duplicates]]).

Symmetric difference (in exactly one of the two sets) is not a single method: union minus intersection, using the same trio ([[How would you explain collection using methods Collection addAll removeAll retainAll]]).

> [!warning] `addAll` / `retainAll` / `removeAll` mutate the receiver
> `a.addAll(b)` is union **into `a`**. On `Set.of`, `Set.copyOf`, and `Collections.unmodifiableSet`, those calls throw `UnsupportedOperationException`. Copy into a `HashSet` (or `LinkedHashSet` / `TreeSet`) before the bulk op if you must keep the original, or if the original cannot be mutated.

> [!warning] Intersection cost follows who is `this`
> `retainAll` does not pick the smaller set for you. Copy the smaller `HashSet` and `retainAll` the larger one. If the argument’s `contains` is linear (`ArrayList`), every lookup is a scan.

> [!tip] Interview answer
> **Union is `addAll`, intersection is `retainAll`, difference is `removeAll` — they mutate the set you call them on.** Copy first (`new HashSet<>(a)`) unless in-place is intended. `removeAll` is A minus B, not the symmetric difference; for intersection on hash sets, copy the smaller set so `retainAll` walks fewer elements.
