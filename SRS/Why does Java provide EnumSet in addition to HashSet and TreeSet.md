<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/EnumSet #Java/Collections/Set/HashSet #Java/Collections/Set/TreeSet #Java/Language/Enum #SRS

> [!abstract] Short answer
> **Because `HashSet` and `TreeSet` are general sets, and an enum is not a general element type.** Constants of one enum are a closed, dense, declaration-ordered universe. `EnumSet` stores that as a bit vector: constant-time membership, compact flags, iteration in source order. `HashSet` still hashes arbitrary objects; `TreeSet` still pays *O(log n)* for a sorted set. Java added `EnumSet` *beside* them, it did not replace them.

## The structure that matches a closed universe

`HashSet` assumes an open-ended type: compute `hashCode`, find a bucket, iterate in hash order, allow `null`. That is correct for `String` and application objects. For `Day.MON`…`Day.SUN` it hashes seven singletons you already numbered 0..6 ([[What does ordinal do on a Java enum]]). Hash iteration order is not the weekday order interviewers mean by “Monday then Tuesday.”

`TreeSet` assumes you need a `NavigableSet`: each op is *O(log n)* `compareTo` (or a `Comparator`). Useful when order is not the enum’s source order, or the set is large and mixed. For one enum, natural order *is* declaration order and *n* is tiny — a red-black tree is overhead ([[Can you use a Java enum with TreeSet or TreeMap]]).

`EnumSet` is the `Set` that uses those facts. Internally a bit per constant (`long` if there are ≤64, `long[]` beyond that). Basic ops are constant time and **likely (not guaranteed)** much faster than `HashSet`. Bulk ops (`containsAll`, `retainAll`, …) against another `EnumSet` are constant-time bit operations. Iteration is declaration order. Factories (`noneOf`, `allOf`, `of`, `range`, `complementOf`) replace `new` ([[What is EnumSet]]). The other stated purpose is a typesafe replacement for `int` bit flags (`BOLD | ITALIC` becomes `EnumSet.of(Style.BOLD, Style.ITALIC)`).

`HashSet<Day>` and `TreeSet<Day>` remain legal. Prefer `EnumSet` when the collection *is* that enum ([[What special collections exist for Java enums]]). The map-side twin is `EnumMap`, for the same density reason ([[Why prefer EnumMap when the keys are enum constants]], [[What is the difference between EnumMap and EnumSet]]).

```d2
direction: down
need: "Set of one enum type" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
wrong: "HashSet hashes  /  TreeSet trees" {
  width: 300
  height: 50
  style.fill: "#ffebee"
}
right: "EnumSet bits — O(1), source order, flags" {
  width: 340
  height: 55
  style.fill: "#e8f5e9"
}

need -> wrong: "general Set"
need -> right: "universe is the enum"
```

**Fig. 1.** Extra type, not a new rule that `HashSet` rejects enums.

```java
import java.util.EnumSet;
import java.util.Set;

enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

class Demo {
    static Set<Day> weekend() {
        Set<Day> work = EnumSet.range(Day.MON, Day.FRI);
        return EnumSet.complementOf(work); // SAT, SUN — bit complement
        // new HashSet<Day>() still compiles; it just hashes
        // new TreeSet<Day>() sorts by compareTo, O(log n)
    }
}
```

**Listing 1.** `range` / `complementOf` are enum-shaped operations. `HashSet` and `TreeSet` have no equivalent.

> [!warning] “In addition” means `HashSet` is not forbidden
> `set.add(Day.MON)` on a `HashSet` works. Interview “enums only go in `EnumSet`” is wrong. You reach for `EnumSet` when the universe is that one enum — compactness, *O(1)*, declaration order, bit flags. Keep `TreeSet` when a `Comparator` must disagree with source order.

> [!warning] Speed is “likely,” and `null` differs
> The spec does not promise a faster `HashSet`. Bulk *O(1)* requires the other collection to be an `EnumSet` too. `EnumSet` rejects `null`; `HashSet` does not ([[Does EnumSet allow null]]).

> [!tip] Interview answer
> **Java provides `EnumSet` in addition to `HashSet` and `TreeSet` because enum constants are a closed bit list, not an open hash universe or a large sorted set.** Membership is a bit vector: *O(1)*, compact, declaration order, typesafe flags. Use `HashSet` for arbitrary elements and `TreeSet` when you need a `Comparator` or navigable order that is not the enum declaration.
