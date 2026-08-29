<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Exceptions/Unchecked #SRS

# Does `EnumMap` allow null keys or null values?

> [!abstract] Short answer
> **No null keys; yes null values.** Inserting a null key (`put`) throws `NullPointerException`. Null values are permitted. `containsKey(null)` and `remove(null)` do **not** throw — they behave as “no such key.” A `get` that returns `null` may mean “mapped to null” or “no mapping.”

## Keys are enum constants; `null` is not one

All keys in an `EnumMap` must come from a single enum type fixed when the map is created. `null` is not an enum constant, so it cannot be inserted. The class specification: null keys are not permitted; attempts to insert a null key throw `NullPointerException`; attempts to **test for** a null key or **remove** one still function properly. Null values are permitted.

`put` lists NPE only for a null **key**, not for a null value. `get` uses identity (`key == k`) — enum constants are unique — and states that a null return can be a stored null or a missing key. Distinguish with `containsKey`.

That is the opposite of `HashMap` on the key side (`HashMap` allows one null key) and unlike `ConcurrentHashMap` / `Hashtable` (neither null keys nor null values). See [[Can HashMap store a null key]], [[Does ConcurrentHashMap allow null keys or values]], [[Can TreeMap have null keys or null values]].

```d2
direction: down
em: "EnumMap" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
key: "put(null, v)\nNullPointerException" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
val: "put(constant, null)\nallowed" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
probe: "containsKey(null) / remove(null)\nno throw; no mapping" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
em -> key
em -> val
em -> probe
```

**Fig. 1.** Ban is on **inserting** a null key. Queries for a null key are defined. Values may be null. Prefer `EnumMap` when keys are enum constants — [[Why prefer EnumMap when the keys are enum constants]].

```java
import java.util.EnumMap;

enum Color { RED, GREEN }

class Demo {
    static void use() {
        var m = new EnumMap<Color, String>(Color.class);
        m.put(Color.RED, null);
        m.containsValue(null);   // true
        m.containsKey(null);     // false, no NPE
        m.get(Color.RED);       // null: stored value
        m.get(Color.GREEN);     // null: no mapping
        m.put(null, "x");        // NullPointerException
    }
}
```

**Listing 1.** Null value on `RED` is stored. `get` is ambiguous until you call `containsKey`. Inserting a null key fails.

The map constructor also NPEs if you pass a null `Class` key type. Keys must all be that one enum; mixing enums is not an `EnumMap` ([[Can you use a Java enum with TreeSet or TreeMap]]).

> [!warning] Opposite of `HashMap` on the key, not on the value
> Interview tables that say “`HashMap` allows nulls, `EnumMap` does not” lump keys and values. `EnumMap` allows null **values**. `get(k) == null` is not proof of absence.

> [!warning] `get(null)` is not the same as `ConcurrentHashMap`
> On `ConcurrentHashMap`, `get(null)` throws NPE. On `EnumMap`, probing a null key is specified to work for `containsKey`/`remove`. Do not assume every “no null keys” map NPEs on lookup.

> [!tip] Interview answer
> **Null keys no, null values yes. `put(null, v)` throws `NullPointerException`; `put(constant, null)` is fine. `containsKey(null)` does not throw. Because values may be null, `get` returning null is ambiguous — use `containsKey`.**
