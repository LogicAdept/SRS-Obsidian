<!--
reps: 0
priority: 0
-->
#Java/Versions/9 #SRS

# What are the collection factory methods List.of Set.of and Map.of

> [!abstract] Short answer
> **The Java 9 factory methods (JEP 269) build small immutable collections in one call: `List.of(...)`, `Set.of(...)`, `Map.of(k,v,...)` up to ten pairs, with `Map.ofEntries`/`List.of()` varargs beyond.** They are **truly immutable** — not unmodifiable views — reject `null` elements and keys, reject duplicate keys (and duplicate `Set` elements), do not permit mutation of any form, and their iteration order is unspecified. `List.copyOf`/`Set.copyOf`/`Map.copyOf` (10) make defensive copies that collapse to no-copy for these types.

## The contract

Immutability here is structural: calling `add`/`remove`/`put` throws `UnsupportedOperationException` unconditionally; `null` elements throw `NullPointerException` **at creation** (fail-fast, not at first access); a repeated `Map` key or `Set` element throws `IllegalArgumentException`. Elements should be value-based and effectively immutable themselves — the collection is shallow: a mutable element inside stays mutable. `Map.of` has fixed 0–10 pair overloads to avoid varargs array allocation and heterogeneous typing; beyond ten use `Map.ofEntries(entry(...), ...)`.

These types are **value-based**: `==` identity is not guaranteed, serialization form is unspecified, and `List.copyOf(x)` on an immutable list returns the same instance — cheap defensive copying. For an unmodifiable *view* of a live collection, `Collections.unmodifiableList` or `Stream.toList()` (16+) remain the tools ([[What does Set.of return and what happens with duplicates]]).

```d2
direction: down
f: "List.of / Set.of / Map.of" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
a: "mutate -> UnsupportedOperationException" {
  width: 360
  height: 55
  style.fill: "#fff8e1"
}
b: "null element/key -> NPE at creation" {
  width: 360
  height: 55
  style.fill: "#fff8e1"
}
c: "dup key/element -> IllegalArgumentException" {
  width: 380
  height: 55
  style.fill: "#fff8e1"
}
u: "Collections.unmodifiable* / toList()\nview over a LIVE collection" {
  width: 380
  height: 65
  style.fill: "#e3f2fd"
}
f -> a
f -> b
f -> c
f -> u: "different tool"
```

**Fig. 1.** Factory collections hard-fail on mutation, nulls, and duplicates; unmodifiable views solve the opposite problem (live delegating wrapper).

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class V14_FactoryMethods {
    public static void main(String[] args) {
        List<String> list = List.of("a", "b");
        try { list.add("c"); } catch (UnsupportedOperationException e) {
            System.out.println("List.of add -> UnsupportedOperationException");
        }
        try { List.of((String) null); } catch (NullPointerException e) {
            System.out.println("List.of(null) -> NullPointerException");
        }
        try { Map.of("k", 1, "k", 2); } catch (IllegalArgumentException e) {
            System.out.println("Map.of duplicate key -> IllegalArgumentException");
        }
        try { Map.of(null, 1); } catch (NullPointerException e) {
            System.out.println("Map.of(null, 1) -> NullPointerException");
        }
        List<String> copy = new ArrayList<>(list);
        copy.add("c");
        System.out.println("wrapped copy is mutable: " + copy);
    }
}
```

**Listing 1.** Verified on JDK 21 (V14_FactoryMethods in empirics): `List.of add -> UnsupportedOperationException`, `List.of(null) -> NullPointerException`, `Map.of duplicate key -> IllegalArgumentException`, `Map.of(null, 1) -> NullPointerException`, `wrapped copy is mutable: [a, b, c]` — every contract clause fires at creation or first mutation, not later (out/V14_FactoryMethods.txt).

> [!warning] Immutable is not unmodifiable-view — and order is not a promise
> The classic bug: build a `List.of` snapshot, then mutate the backing array you *thought* it wrapped — it wraps nothing; changes are never visible. The reverse bug: expect `Collections.unmodifiableList` to freeze the source — it delegates, so the caller who keeps the original mutates your "immutable" list. `Set.of` iteration order is unspecified and may differ between JDK builds. And `Map.of` caps at ten pairs: the eleventh pair silently does not compile against the fixed overloads — use `ofEntries` ([[What was new in Java 9 besides modules]]).

> [!tip] Interview answer
> **The Java 9 factories build small, truly immutable collections: mutation throws `UnsupportedOperationException`, nulls throw NPE at creation, duplicate keys/elements throw at creation, order unspecified, up to ten `Map.of` pairs before `ofEntries`.** Unlike unmodifiable views they hold no reference to a mutable source; `copyOf` makes the cheap defensive copy idiomatic.
