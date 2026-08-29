<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Exceptions/Unchecked #SRS

# Does `ConcurrentHashMap` allow null keys or values?

> [!abstract] Short answer
> **Neither.** Like `Hashtable` and unlike `HashMap`, `ConcurrentHashMap` does not allow `null` as a key or as a value. `put(null, v)` and `put(k, null)` throw `NullPointerException`. A `get` that returns `null` means the key is **absent**.

## Null is reserved for “not present”

The class specification states it outright: this map does not allow `null` to be used as a key or value. `put` documents that neither the key nor the value can be null, and throws `NullPointerException` if either is. `get`, `containsKey`, and `remove` throw NPE on a null **key**; `containsValue` throws NPE on a null **value**.

Because keys and values in the map are never null, a null result from `get` is a reliable indicator that there is no mapping. Bulk search/reduce operations use the same rule: null means “nothing there now.” That is why the map can treat a non-null `get` as bearing a happens-before relation with the write that installed that value.

`HashMap` permits the null key and null values, so `get` returning null is ambiguous there ([[Can HashMap store a null key]]). `Hashtable` also forbids both ([[Does Hashtable allow null keys or values]]). `TreeMap` is a different split: null **values** are allowed; a null **key** depends on the ordering ([[Can TreeMap have null keys or null values]]).

```d2
direction: down
chm: "ConcurrentHashMap" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
put: "put(null, v) or put(k, null)\nNullPointerException" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
get: "get(k) == null\nmeans absent" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
chm -> put
chm -> get
```

**Fig. 1.** Both null keys and null values are rejected. A null `get` is absence, not a stored null.

```java
import java.util.concurrent.ConcurrentHashMap;

class Demo {
    static void use() {
        var m = new ConcurrentHashMap<String, Integer>();
        m.put("a", 1);
        Integer missing = m.get("nope"); // null: no mapping
        m.put(null, 1);   // NullPointerException
        m.put("b", null); // NullPointerException
    }
}
```

**Listing 1.** `put` rejects a null key **or** a null value. `get` on a missing key returns null without NPE; `get(null)` throws NPE.

`computeIfAbsent` inserts the computed value unless the function returns `null`. On this map that is not a way to store a null value — values cannot be null — it is how a function declines to establish a mapping. The call is atomic; the function must not modify the map, and a null key or function is an NPE.

> [!warning] `containsKey` then `get` is still racy
> You do not need that pair to tell “absent” from “mapped to null,” because the second case cannot occur. Other threads can still insert or remove between two calls. Use one atomic method (`putIfAbsent`, `computeIfAbsent`, `compute`) when the update must see a consistent view.

> [!warning] `get(null)` is an NPE, not “absent”
> Only a non-null missing key yields a null return. Passing `null` into `get`/`containsKey` is the same ban as `put`, not a lookup of a null key.

> [!tip] Interview answer
> **No null keys and no null values — `put` throws `NullPointerException` for either. That matches `Hashtable` and differs from `HashMap`. Because a stored value can never be null, `get` returning null means the key is absent, which is a reliable concurrent signal.**
