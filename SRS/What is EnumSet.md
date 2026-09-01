<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/EnumSet #Java/Language/Enum #SRS

> [!abstract] Short answer
> **`java.util.EnumSet` is a specialized `Set` whose elements must all be constants of one enum type.** You never write `new EnumSet`: the type is abstract. Factories (`noneOf`, `allOf`, `of`, `range`, `complementOf`, `copyOf`) fix that enum type when the set is created. Membership is a bit vector; iteration follows declaration order.

## One enum type, factories, bits

Every element must come from a single enum class stored as `elementType` ([[Must EnumMap keys all come from the same enum type]] is the map twin). `noneOf(E.class)` builds an empty set of that type and, internally, picks `RegularEnumSet` when there are at most 64 constants and `JumboEnumSet` otherwise. `allOf`, `of`, `range`, and `complementOf` go through the same path. `add` of a constant from another enum throws `ClassCastException`.

`null` is not a constant of that type: insert/`of`/`range` throw `NullPointerException`; `contains(null)` / `remove(null)` return `false` ([[Does EnumSet allow null]]). The class is not synchronized; wrap with `Collections.synchronizedSet` at creation if threads share a mutable set.

```d2
direction: down
e: "enum Day { MON … SUN }" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
f: "noneOf / allOf / of / range / complementOf" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}
s: "EnumSet<Day> — bit vector, declaration order" {
  width: 340
  height: 50
  style.fill: "#e8f5e9"
}

e -> f: "element type"
f -> s
```

**Fig. 1.** One enum universe, factories instead of `new`, membership as bits.

```java
import java.util.EnumSet;

enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

class Demo {
    static EnumSet<Day> weekend() {
        EnumSet<Day> work = EnumSet.range(Day.MON, Day.FRI);
        return EnumSet.complementOf(work); // SAT, SUN
        // EnumSet.noneOf(Day.class) empty
        // EnumSet.allOf(Day.class)  seven days
        // EnumSet.of(Day.SAT, Day.SUN) same weekend
    }
}
```

**Listing 1.** `range` is inclusive of both endpoints. `from.compareTo(to) > 0` throws `IllegalArgumentException`.

The iterator walks constants in natural order — the order they are declared — not hash order. It is **weakly consistent**: it never throws `ConcurrentModificationException`, and it may or may not show adds/removes that happen during iteration. That is not a fail-fast `HashSet` iterator and not a snapshot copy.

Basic ops are specified as constant time, and bulk ops are constant time when the other collection is also an `EnumSet`. That bit-vector design is why `EnumSet` exists beside `HashSet` and `TreeSet` ([[Why does Java provide EnumSet in addition to HashSet and TreeSet]], [[What special collections exist for Java enums]]). `EnumMap` is the map counterpart, not a set ([[What is the difference between EnumMap and EnumSet]]). `add` never declares a new constant ([[Can you add constants to a Java enum at runtime]]).

> [!warning] The iterator is not a fail-safe copy
> Dump wording that it “works on a copy” is wrong. Weakly consistent means no `ConcurrentModificationException` **and** no promise of a frozen snapshot. Do not mutate the set and assume the iterator still lists the old members.

> [!warning] `copyOf` on an empty non-`EnumSet` collection fails
> `EnumSet.copyOf(someEnumSet)` clones even when empty. `EnumSet.copyOf(emptyList)` throws `IllegalArgumentException` because a plain collection needs at least one element to infer the enum type. Prefer `noneOf(E.class)` for an empty set.

> [!tip] Interview answer
> **`EnumSet` is a `Set` of constants from one enum type, created with factories such as `noneOf`, `allOf`, `of`, `range`, and `complementOf`.** It stores membership as a bit vector, iterates in declaration order, rejects `null` on insert, and is not synchronized. The iterator is weakly consistent — never `ConcurrentModificationException`, not a snapshot. Use it instead of `HashSet` when the universe is an enum.
