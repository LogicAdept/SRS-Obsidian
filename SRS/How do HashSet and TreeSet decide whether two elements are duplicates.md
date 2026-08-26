<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Set/TreeSet #Java/HashCodeEquals #SRS

# How do `HashSet` and `TreeSet` decide whether two elements are duplicates?

> [!abstract] Short answer
> **`HashSet` (and `LinkedHashSet`): `hashCode` then `equals`.** Membership is “no other element `e2` with `Objects.equals(e, e2)`,” implemented via a backing [[How is HashSet implemented in terms of HashMap]]. **`TreeSet`: `compareTo` or the constructor `Comparator` only.** Two elements are the same set member when that comparison returns `0`. The tree does not consult `equals` for that decision.

## Two different sameness tests

The `Set` interface defines “no duplicates” in terms of `equals`: no pair `e1`, `e2` with `e1.equals(e2)`. Implementations still choose *how* they discover that.

```d2
direction: down
add: "add(e)" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
hs: "HashSet\nhashCode → bucket\nthen equals" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
ts: "TreeSet\ncompare / compareTo\n== 0 → duplicate" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}

add -> hs
add -> ts
```

**Fig. 1.** Same `Set.add` contract, different comparison engines.

### `HashSet` / `LinkedHashSet`

Java SE 21: `HashSet` is a `Set` backed by a `HashMap`. `add(e)` adds only if the set contains no `e2` with `Objects.equals(e, e2)`. Under the hood that is map-key lookup: hash to a bin, then `equals` in the bin — same path as [[When does a hashCode collision occur in a HashMap]].

`LinkedHashSet` extends `HashSet`, so uniqueness is the same; the extra doubly linked list only fixes **encounter (insertion) order**.

```java
Set<String> s = new HashSet<>();
s.add("x");
s.add("x"); // false; size stays 1
```

**Listing 1.** Second `add` is a no-op because `equals` already holds.

### `TreeSet`

`TreeSet` is a `NavigableSet` on a `TreeMap`. It performs **all** element comparisons with `compareTo` (natural order) or the supplied `Comparator`. Elements that compare equal (`0`) are equal **from the set’s standpoint**. There is no `hashCode` step and no `equals` call on the membership path.

```java
Set<String> ci = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
ci.add("Java");
ci.add("JAVA"); // compare == 0 → rejected as duplicate
ci.size();      // 1
```

**Listing 2.** Case-insensitive order treats `"Java"` and `"JAVA"` as one element even though `equals` is false.

> [!warning] Ordering must stay consistent with `equals`
> The javadoc requires that for a correct `Set` implementation. If `compare`/`compareTo` and `equals` disagree, behavior is still defined but the set **fails the general `Set` contract** — it can keep two `equals` elements, or drop one that `equals` would distinguish. Same rule as [[Why must TreeMap ordering be consistent with equals]] / [[How does TreeMap decide whether two keys are the same]].

> [!warning] Do not say “TreeSet uses equals”
> Interview trap: assuming every `Set` uses `equals` at runtime. `TreeSet` uses the ordering relation; `equals` is the *contract* language, not the tree’s probe.

> [!tip] Interview answer
> **`HashSet` finds duplicates with `hashCode` then `equals` (via its `HashMap`). `TreeSet` finds them when `compareTo`/`Comparator` returns 0 and does not call `equals` for that check.** Keep the ordering consistent with `equals`, or the set can violate the `Set` contract. `LinkedHashSet` uses the HashSet rule plus insertion order.
