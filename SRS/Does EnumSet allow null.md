<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/EnumSet #Java/Language/Enum #Java/Collections/Set/HashSet #SRS

# Does `EnumSet` allow null?

> [!abstract] Short answer
> **No as an element.** `EnumSet` does not permit `null`. `add(null)` and the `of(...)` factories throw `NullPointerException`. `contains(null)` and `remove(null)` do **not** throw — they behave as “not present” (`false`). That split is what interview dumps flatten into a blanket “no nulls.”

## Insert vs query

Every element must come from the single enum type fixed when the set is created ([[What is EnumSet]]). `null` is not a constant of that type, so it cannot occupy a bit in the vector. Insertion paths reject it. Membership tests still have to answer “is this object in the set?” for a `null` argument, and the specified answer is “no,” without an exception.

```d2
direction: down
q: "null and EnumSet" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
add: "add / of / copyOf\nNullPointerException" {
  width: 260
  height: 70
  style.fill: "#ffcdd2"
}
query: "contains / remove\nfalse, no throw" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

q -> add
q -> query
```

**Fig. 1.** “Does not allow null” is about *storing* a null. Probing for one is defined and quiet.

```java
enum Color { RED, GREEN }

class Demo {
    void probe() {
        java.util.EnumSet<Color> s = java.util.EnumSet.noneOf(Color.class);
        s.add(Color.RED);

        // s.add(null);                    // NullPointerException
        // java.util.EnumSet.of(Color.RED, null); // NullPointerException

        s.contains(null); // false
        s.remove(null);   // false — set unchanged
    }
}
```

**Listing 1.** Insert throws; `contains`/`remove` return `false`. `noneOf` is empty of constants, not a set that holds `null`.

The same insertion rule is why `EnumSet.add` cannot invent a constant ([[Can you add constants to a Java enum at runtime]]). You only select among names that already exist.

## Contrast with `HashSet` and `EnumMap`

`HashSet` permits the `null` element (at most one, like any `Set`). That is the usual collections default; `EnumSet` is the exception because its universe is the enum’s constants ([[Why does Java provide EnumSet in addition to HashSet and TreeSet]]).

`EnumMap` matches `EnumSet` on **keys**: null keys are forbidden on `put`, while `containsKey(null)` / `remove(null)` are allowed. **Values** on an `EnumMap` may be null ([[What is the difference between EnumMap and EnumSet]]). Do not export the set rule to map values.

> [!warning] `contains(null)` returning `false` is not “null is allowed”
> If you only call `contains` in a test, `EnumSet` looks as null-tolerant as `HashSet`. The NPE shows up on `add`, `of`, and filling from a collection that contains `null`.

> [!warning] `HashSet` is the wrong mental model here
> “`Set` allows one null” is true of `HashSet` and `LinkedHashSet`. It is false of `EnumSet` (and of `TreeSet` under natural order). Name the type.

> [!tip] Interview answer
> **No — `EnumSet` rejects `null` on insert with `NullPointerException`.** `contains(null)` and `remove(null)` still return `false` and do not throw. `HashSet` allows one null; that is not the enum-set rule.
