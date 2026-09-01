<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Language/Enum #Java/Collections/Map/HashMap #SRS

> [!abstract] Short answer
> **Because the key universe is a small, dense list of constants, `EnumMap` is an array indexed by `ordinal()` — a `Map` with array speed and no hashing.** Basic `get`/`put` are constant time and likely faster than `HashMap`. Iteration is declaration order. Prefer it over a hand-rolled `V[]` as well: you keep the `Map` API and you do not sprinkle `ordinal()` through callers.

## Dense keys, so an array beats a hash table

`HashMap` hashes the key, finds a bucket, and may walk a chain. Enum constants already have a unique dense index: `ordinal()` ([[What does ordinal do on a Java enum]]). `EnumMap` stores `vals[key.ordinal()]` for one enum type specified at creation ([[How does EnumMap store mappings internally]], [[Must EnumMap keys all come from the same enum type]]). There is nothing to hash and no collision list.

The class javadoc says basic operations run in constant time and are **likely (not guaranteed)** faster than the `HashMap` counterparts. The map is compact: one slot per constant, not a load-factor table. Views iterate in natural order — the order the constants are declared — not hash order ([[In what order does EnumMap iterate]]).

A raw `String[] labels = new String[Day.values().length]` with `labels[day.ordinal()]` is the same layout without a `Map`. Official guidance is to use `EnumMap` in preference to that array: you get `put`/`get`/`containsKey`, null-value handling, and you do not treat `ordinal()` as a public protocol. Construct with `new EnumMap<>(Day.class)` ([[How do you create an EnumMap]]).

`EnumSet` is the set twin (bits, not values) — a different type ([[What is the difference between EnumMap and EnumSet]], [[Why does Java provide EnumSet in addition to HashSet and TreeSet]]). `EnumMap` is not synchronized ([[Is EnumMap synchronized]]). Null keys are rejected; null values are allowed ([[Does EnumMap allow null keys or null values]]).

```d2
direction: down
hm: "HashMap<Day, V>\nhashCode, buckets, hash order" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
em: "EnumMap<Day, V>\nvals[ordinal], declaration order" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

hm -> em: "keys are one enum type"
```

**Fig. 1.** Same `Map` interface. The specialized table is an array of the enum’s size.

```java
import java.util.EnumMap;
import java.util.Map;

enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

class Demo {
    static Map<Day, String> plans() {
        Map<Day, String> m = new EnumMap<>(Day.class);
        m.put(Day.MON, "gym");
        return m;
        // m.get(Day.MON) is vals[0], not a hash lookup
    }
}
```

**Listing 1.** Class token fixes the key type. `put`/`get` stay ordinary `Map` calls.

> [!warning] “Always faster than `HashMap`” is not a spec guarantee
> The API says *likely* faster. Tiny maps and a good hash can be close. The reasons to prefer `EnumMap` are still the dense array, declaration-order iteration, and a single enum key type — not a benchmark you must recite.

> [!warning] Do not index `Day.values()` with `ordinal()` instead
> Inserting a constant reshuffles ordinals. `EnumMap` still hides the index. Mixing two enum types as keys needs `HashMap`; `EnumMap` will not hold both ([[Must EnumMap keys all come from the same enum type]]).

> [!tip] Interview answer
> **Prefer `EnumMap` when every key is a constant of one enum type because it is an array indexed by `ordinal()`, not a hash table.** You get constant-time `Map` operations, compact storage, and declaration-order iteration, typically faster than `HashMap`. Prefer it over a raw array too — keep the `Map` API and keep `ordinal()` out of business code.
