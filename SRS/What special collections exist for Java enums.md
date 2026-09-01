<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Collections/Set/EnumSet #Java/Language/Enum #SRS

> [!abstract] Short answer
> **Two: `java.util.EnumSet` and `java.util.EnumMap`.** They shipped with language enums in Java 5. `EnumSet` is a `Set` of constants from one enum type (bit vector). `EnumMap` is a `Map` whose **keys** are constants from one enum type (array indexed by `ordinal()`). There is no `EnumList`.

## The two `java.util` types added for enums

Ordinary collections accept enum values: a `HashSet<Day>`, `ArrayList<Day>`, or `HashMap<String, Day>` is legal. The **specialized** types exist because an enum’s universe is finite and ordered by declaration ([[What is the advantage of a Java enum over int and String constant patterns]]).

`EnumSet<E extends Enum<E>>` records membership. Factories (`noneOf`, `allOf`, `of`, `range`, `complementOf`), not `new`. One enum type per set ([[What is EnumSet]]). That is the typesafe stand-in for int bit flags, which is why it exists beside `HashSet` and `TreeSet` ([[Why does Java provide EnumSet in addition to HashSet and TreeSet]]).

`EnumMap<K extends Enum<K>, V>` records a value per constant. Construct with `new EnumMap<>(E.class)` ([[How do you create an EnumMap]]). Keys from one enum; values are unrestricted (including `null`). Internals are an array, not a hash table ([[How does EnumMap store mappings internally]], [[Why prefer EnumMap when the keys are enum constants]]).

They are different jobs — set vs map — not two names for one structure ([[What is the difference between EnumMap and EnumSet]]). `TreeSet`/`TreeMap` also work via `Enum`’s `compareTo`; they are general sorted collections, not enum-specific implementations ([[Can you use a Java enum with TreeSet or TreeMap]]).

```d2
direction: down
e: "enum E { … }" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
s: "EnumSet<E>\nSet, bits" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
m: "EnumMap<E, V>\nMap, array of values" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

e -> s: "elements"
e -> m: "keys"
```

**Fig. 1.** The only two enum-specialized collections in `java.util`.

```java
import java.util.EnumMap;
import java.util.EnumSet;
import java.util.Map;
import java.util.Set;

enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

class Demo {
    static int demo() {
        Set<Day> weekend = EnumSet.of(Day.SAT, Day.SUN);
        Map<Day, String> labels = new EnumMap<>(Day.class);
        labels.put(Day.MON, "start");
        return weekend.size() + labels.size();
    }
}
```

**Listing 1.** `EnumSet` for membership. `EnumMap` for a value hanging off a constant.

> [!warning] Enums are allowed in `HashSet` and `HashMap`
> The specialized types are not a language requirement. Interview “you must use `EnumSet`” is efficiency and a closed universe, not “`HashSet.add(Day.MON)` fails.” Prefer them when the set/map is *about* that enum type.

> [!warning] There is no `EnumList`, and `EnumMap` is not for enum *values*
> A list of constants is `List`/`ArrayList`. A map from strings to enums is an ordinary `Map`. `EnumMap` requires enum **keys**.

> [!tip] Interview answer
> **Java provides `EnumSet` and `EnumMap` as the specialized collections for enum types.** `EnumSet` is a bit-vector `Set` of one enum’s constants; `EnumMap` is an array-backed `Map` keyed by one enum type. Other collections still work; use these two when the universe is that enum. There is no `EnumList`.
