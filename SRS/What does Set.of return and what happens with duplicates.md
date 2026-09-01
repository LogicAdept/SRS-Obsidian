<!--
reps: 0
priority: 0
-->
#Java/Collections/Set #Java/Versions/9 #SRS

# What does `Set.of` return and what happens with duplicates?

> [!abstract] Short answer
> **`Set.of(...)` (Java 9) returns an unmodifiable `Set`.** Duplicate arguments throw **`IllegalArgumentException` at creation** — they are not silently dropped the way `HashSet.add` ignores a second equal element. `null` throws `NullPointerException`. Mutators (`add`, `remove`, `clear`, …) throw `UnsupportedOperationException`.

## Unmodifiable factory, not a `HashSet`

`Set.of` is a family of static factories on `java.util.Set`: zero through ten fixed-arity overloads plus `@SafeVarargs of(E... elements)`. The result is **unmodifiable**: elements cannot be added or removed. Calling any mutator **always** throws `UnsupportedOperationException`. That is stricter than `Collections.unmodifiableSet`, which is a view that still sees later changes to a backing set ([[What is the Set interface in Java]]).

Duplicates are rejected **up front**. Two-arg and larger overloads document `IllegalArgumentException` if any elements are duplicates (`Objects.equals`). A normal `Set.add` on a mutable set leaves the set unchanged and returns `false` ([[How do HashSet and TreeSet decide whether two elements are duplicates]]).

```java
Set<String> s = Set.of("a", "b", "c");
s.add("d");                 // UnsupportedOperationException

Set<String> dup = Set.of("a", "a"); // IllegalArgumentException
```

**Listing 1.** Compact constants. The second call never returns a one-element set.

`Set.copyOf(collection)` (Java **10**) is the other unmodifiable factory. If the collection already contains duplicates, **an arbitrary one is kept** — no `IllegalArgumentException`. Null collection or null elements still throw `NPE`. If the argument is already an unmodifiable `Set`, `copyOf` generally does not copy.

```d2
direction: down
of: "Set.of(a, b, …)\nJava 9" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ok: "distinct, non-null\nunmodifiable Set" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
dup: "any Objects.equals pair\nIllegalArgumentException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
npe: "null element or null array\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

of -> ok
of -> dup
of -> npe
```

**Fig. 1.** Creation-time checks. `HashSet` would accept the duplicate and skip it; `Set.of` refuses to build.

## Other documented properties

- **No `null`:** creating with a null element (or a null varargs array) throws `NPE`. `HashSet` allows one `null` ([[Does HashSet allow a null element]]).
- **Iteration order** is unspecified and **subject to change** — not insertion order, not sorted order. Need encounter order or a comparator → `LinkedHashSet` / `TreeSet` ([[When should you choose HashSet LinkedHashSet or TreeSet]]).
- **Value-based:** treat equal instances as interchangeable. Do not synchronize on them; identity is not promised. Factories may reuse instances.
- **Serializable** if every element is.
- **Varargs vs one array:** `of(E...)` also accepts a single array; the set’s element type is the **component** type and the size is the array length. For a set whose one element *is* an array, call `Set.<String[]>of(array)` so the one-arg `of(E)` is used.

Need a mutable copy later: `new HashSet<>(Set.of(...))`. Mutating that copy does not change the original factory set.

> [!warning] Unmodifiable is not “deeply immutable”
> If an element is mutable, the set can appear to change even though you cannot `add`/`remove`. Do not put a mutable object in `Set.of` and then mutate fields that `equals` / `hashCode` depend on — set behavior is already unspecified for that pattern.

> [!warning] Duplicates: `of` throws, `copyOf` keeps one
> `Set.of("a", "a")` is `IllegalArgumentException`. `Set.copyOf` from a `List`/`Collection` that already contains two equal elements keeps one of them. Do not assume every unmodifiable factory rejects duplicates.

> [!tip] Interview answer
> **`Set.of` is the Java 9 unmodifiable set factory: no nulls, unspecified order, mutators throw `UnsupportedOperationException`.** Duplicates at creation throw `IllegalArgumentException`, unlike `HashSet.add` which returns `false`. `Set.copyOf` is the Java 10 cousin that quietly keeps one of any duplicates.
