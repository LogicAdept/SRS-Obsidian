<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Exceptions/Unchecked #SRS

# Does `Hashtable` allow null keys or values?

> [!abstract] Short answer
> **Neither.** Any key or value must be a non-`null` object. `put` throws `NullPointerException` if the key **or** the value is `null`. `get(null)` and `containsKey(null)` also throw NPE. `HashMap` allows one null key and null values.

## Non-null objects only

The class specification: any non-null object can be used as a key or as a value. `put` states that neither the key nor the value can be `null`, and throws `NullPointerException` if the key or value is `null`. `get` returns null only when a **non-null** key has no mapping; a null key is an NPE, not a lookup. `remove` and `containsKey` NPE on a null key; `containsValue(null)` NPEs too.

`HashMap` is the contrast: it permits the null key and null values ([[Can HashMap store a null key]]). `ConcurrentHashMap` documents itself as “like `Hashtable` but unlike `HashMap`” on this point ([[Does ConcurrentHashMap allow null keys or values]]). See also [[What is the difference between HashMap and Hashtable]].

```d2
direction: down
ht: "Hashtable" {
  width: 220
  height: 50
  style.fill: "#ffebee"
}
put: "put(null, v) or put(k, null)\nNullPointerException" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
get: "get(k) == null\nmeans absent (k non-null)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
getn: "get(null)\nNullPointerException" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
ht -> put
ht -> get
ht -> getn
```

**Fig. 1.** Null is banned on insert **and** on lookup. A null `get` result still means “no mapping,” because a stored value cannot be null.

```java
import java.util.Hashtable;

class Demo {
    static void use() {
        var t = new Hashtable<String, Integer>();
        t.put("one", 1);
        Integer missing = t.get("two"); // null: no mapping
        t.put(null, 1);   // NullPointerException
        t.put("x", null); // NullPointerException
        t.get(null);      // NullPointerException
    }
}
```

**Listing 1.** `new Hashtable()` is the default constructor. Both a null key and a null value fail on `put`. `get(null)` is not “absent.”

`EnumMap` also forbids inserting a null key but still allows null **values**, and `containsKey(null)` does not throw ([[Does EnumMap allow null keys or null values]]). Do not treat every “no null keys” map as `Hashtable`.

> [!warning] Interview tables that only say “no nulls”
> Name the exception: `NullPointerException` on `put` (key or value) and on `get`/`containsKey` with a null key. “No nulls” is also true of `ConcurrentHashMap`; it is not a `Hashtable`-only trivia fact.

> [!warning] `get` returning null is absence, not a stored null
> Because values cannot be null, `get(k) == null` (with a non-null `k`) means there is no mapping. You cannot store a present-but-null value the way `HashMap` can.

> [!tip] Interview answer
> **Neither — `Hashtable` rejects a null key and a null value. `put` throws `NullPointerException` for either. `HashMap` allows one null key and null values; `ConcurrentHashMap` matches `Hashtable` here. `get(null)` also throws, it does not mean absent.**
