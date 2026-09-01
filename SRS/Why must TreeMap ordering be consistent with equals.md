<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/HashCodeEquals #SRS

# Why must `TreeMap` ordering be consistent with `equals`?

> [!abstract] Short answer
> The `Map` contract is written in terms of **`equals`**. A `TreeMap` never uses `equals` to find a key — it uses **`compareTo` or `Comparator.compare`**. Those two tests must agree (`compare == 0` iff `equals`) or the tree is a broken `Map`: `containsKey`, `put`, and map `equals` can disagree with a `HashMap` of the same pairs. The tree’s own behavior stays defined; it just violates `Map`.

## Two equality relations, one type

`Map.containsKey` is specified as: there is a key `k` such that `key.equals(k)` (null-safe). Implementations may skip calling `equals` (for example after hash codes), but the **meaning** is still `equals`.

A sorted map instead treats two keys as the same when `compareTo` / `compare` returns **0**. `TreeMap` says that outright: those keys are equal from the tree’s standpoint. `get` looks up by that ordering ([[How does TreeMap decide whether two keys are the same]]).

**Consistent with equals** (`Comparable` / `Comparator`): `c.compare(e1, e2) == 0` has the same boolean value as `e1.equals(e2)` for every pair. Natural order uses `compareTo` in that sentence. The same rule is on `SortedMap` and on `TreeSet` (a `TreeMap` façade) ([[Is TreeSet implemented using TreeMap]]).

Break it in either direction:

| Mismatch | What the tree does | What `Map` / `Set` promised |
| --- | --- | --- |
| `compare == 0` but `!equals` | Second `put` **replaces**; one mapping | Two `equals`-distinct keys should both be present |
| `equals` but `compare != 0` | Second `put` **inserts**; two mappings | Duplicate keys are forbidden |

`Comparable`’s sorted-set example is the first row (`add` returns false, size unchanged). `Comparator`’s `TreeSet` example is the second (`add` returns true, size grows — contrary to `Set.add`). A length-only string comparator is the first row for maps ([[How do you customize TreeMap key order]]).

The class comment: behavior is **well-defined** even when inconsistent; it just **fails the `Map` contract**. You still use `TreeMap` for sorted keys — you keep `compareTo`/`compare` aligned with `equals`, or you document “inconsistent with equals” and do not treat the object as a general-purpose `Map` ([[What types can you use as TreeMap keys]]). Core library exception: `BigDecimal` `4.0` vs `4.00` (numeric order, representation `equals`).

`HashMap` keys need `equals` and `hashCode` together ([[Why should equals and hashCode be overridden together]]). `TreeMap` keys need `equals` and **compare** together. `hashCode` is unused in the tree search.

```d2
direction: down
map: "Map.containsKey\nequals" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
tree: "TreeMap.get / put\ncompare == 0" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
ok: "same pairs ⇔ correct Map" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
bad: "disagree ⇔ well-defined\nbut not a correct Map" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
map -> ok
tree -> ok
map -> bad
tree -> bad
```

**Fig. 1.** Alignment is the `Map` contract. The tree does not start calling `equals` if you skip it.

```java
import java.math.BigDecimal;
import java.util.Comparator;
import java.util.HashMap;
import java.util.TreeMap;

class Demo {
    static void lengthNotConsistent() {
        var t = new TreeMap<String, Integer>(
                Comparator.comparingInt(String::length));
        t.put("One", 1);
        t.put("Two", 2);              // compare == 0, !equals
        t.size();                     // 1 — not a correct Map
        new HashMap<>(t).size();      // still 1; HashMap.copy sees one mapping
    }

    static void bigDecimalNaturalOrder() {
        var t = new TreeMap<BigDecimal, String>();
        t.put(new BigDecimal("4.0"), "a");
        t.put(new BigDecimal("4.00"), "b"); // compareTo == 0
        t.size(); // 1
        new BigDecimal("4.0").equals(new BigDecimal("4.00")); // false
    }
}
```

**Listing 1.** Length-only order merges unequal strings. `BigDecimal` natural order is the documented core-library inconsistency with `equals`.

> [!warning] `compare == 0` is uniqueness, even when `equals` is false
> The second mapping overwrites the value. `containsKey("Two")` can be true after you inserted `"One"` only. The reverse mismatch stores two keys that `equals` says are the same — `Map` forbids that.

> [!warning] “Well-defined” is not “a valid Map”
> Dumps that say the map “will throw” are wrong. It runs. Sorted-set/`TreeSet` dumps are the same contract, not a different rule. Fix `compareTo`/`equals` (and a custom `Comparator`) together, or do not use the type as a `Map` key.

> [!tip] Interview answer
> **`Map` is `equals`; `TreeMap` is `compare`/`compareTo`. Consistent with equals means those are the same boolean. If not, `put` can drop a key or keep two that `equals` says are one — the tree still runs, it just is not a correct `Map`. Same warning on `SortedMap` and `TreeSet`. `BigDecimal` is the JDK’s own example.**
