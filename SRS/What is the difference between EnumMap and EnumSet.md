<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Collections/Set/EnumSet #Java/Language/Enum #SRS

> [!abstract] Short answer
> **`EnumMap` is a `Map` from one enum type’s constants to values. `EnumSet` is a `Set` of those constants.** Same universe — every key or element from a single enum type specified at creation — different job: associate data vs record membership. Internally the map is an array indexed by `ordinal()`; the set is a bit vector.

## Map of values vs set of bits

`EnumMap<K extends Enum<K>, V>` implements `Map`. You construct it with a class token: `new EnumMap<>(Day.class)`. Keys must all be that enum ([[Must EnumMap keys all come from the same enum type]]). The table is `vals[key.ordinal()]` ([[How does EnumMap store mappings internally]]). Null **keys** throw on insert; null **values** are allowed ([[Does EnumMap allow null keys or null values]]).

`EnumSet<E extends Enum<E>>` implements `Set`. It is abstract: factories (`noneOf`, `allOf`, `of`, `range`, `complementOf`) not `new` ([[What is EnumSet]]). Membership is a bit per constant. Null elements are not permitted ([[Does EnumSet allow null]]).

Both iterate in declaration order, are unsynchronized, and specify constant-time basic ops. Both are the specialized collections for a closed enum universe ([[What special collections exist for Java enums]]). Prefer `EnumMap` over `HashMap` when keys are enums ([[Why prefer EnumMap when the keys are enum constants]]); prefer `EnumSet` over `HashSet`/`TreeSet` when the elements are enums ([[Why does Java provide EnumSet in addition to HashSet and TreeSet]]). Official wording is “likely faster,” not a language rule.

```d2
direction: down
e: "enum Day { MON … SUN }" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
m: "EnumMap<Day, V>\narray of values, Map" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
s: "EnumSet<Day>\nbit vector, Set" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

e -> m: "key type"
e -> s: "element type"
```

**Fig. 1.** One enum type, two collection roles.

```java
import java.util.EnumMap;
import java.util.EnumSet;
import java.util.Map;
import java.util.Set;

enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

class Demo {
    static int demo() {
        Map<Day, String> labels = new EnumMap<>(Day.class);
        labels.put(Day.MON, "start");
        Set<Day> weekend = EnumSet.of(Day.SAT, Day.SUN);
        return labels.size() + weekend.size();
        // EnumSet.of maps nothing — membership only
        // new EnumSet<>(Day.class) does not compile
    }
}
```

**Listing 1.** `EnumMap` takes a `Class` token and `put`s values. `EnumSet` is created by factories and only holds constants.

`EnumMap<Day, Boolean>` is still a map of objects. A typesafe flag set is `EnumSet` — that is the replacement for int bit flags, not a `Boolean` map.

> [!warning] `EnumSet` is not a tiny `EnumMap`
> Membership (`contains` / `add` / `remove`) is the set. A value per constant (`get` / `put`) is the map. If you need both “is this day selected” and “what string is attached,” you want a set **or** a map, not the other type renamed.

> [!warning] You can `new EnumMap`; you cannot `new EnumSet`
> `EnumSet` is abstract (regular vs jumbo bit vector). Forgetting the class token on `EnumMap` does not compile; passing the wrong enum `Class` is a different map, not a mixed-key map.

> [!tip] Interview answer
> **`EnumMap` is a `Map` (array of values, keys from one enum); `EnumSet` is a `Set` (bit vector of constants from one enum).** Construct the map with `new EnumMap<>(E.class)`; construct the set with factories such as `noneOf` / `of`. Use the map when constants carry data, the set when you only need membership.
