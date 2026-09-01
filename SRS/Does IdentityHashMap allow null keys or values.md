<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Map/HashMap #Java/Collections/Map/WeakHashMap #Java/Collections/Map/Hashtable #Java/Collections/Map/ConcurrentHashMap #SRS

# Does `IdentityHashMap` allow null keys or values?

> [!abstract] Short answer
> **Yes — one null key, and null values.** Same story as `HashMap` and `WeakHashMap`. `Hashtable` and `ConcurrentHashMap` reject both. `get` returning `null` is ambiguous: missing key versus a mapping to `null`; use `containsKey`.

## Null is allowed; there is still only one null

The class permits the null key and null values. Keys match with `==`, and there is only one `null`, so a second `put(null, …)` replaces the value. That is not a second “null object.” Values may be null independently of the key. [[How does IdentityHashMap decide whether two keys are the same]] [[What is the difference between HashMap and IdentityHashMap]]

Empty slots in the linear-probe table are `null`, so a null key cannot sit in the array as-is. The implementation stores a private sentinel (`NULL_KEY`) and unmasks it on the way out. Callers still see `null`. A null **value** is stored as a real `null` next to a non-empty key slot.

```d2
direction: down
q: "put(null, v)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
ok: "IdentityHashMap, HashMap,\nWeakHashMap: keep it" {
  width: 280
  height: 80
  style.fill: "#c8e6c9"
}
no: "Hashtable,\nConcurrentHashMap: reject" {
  width: 280
  height: 80
  style.fill: "#ffcdd2"
}

q -> ok
q -> no
```

**Fig. 1.** Null policy is a map-family split, not an identity-map quirk. Identity maps sit with `HashMap`, not with `Hashtable`.

```java
IdentityHashMap<String, String> id = new IdentityHashMap<>();
id.put(null, "v");
id.put("k", null);
id.get(null);          // "v"
id.containsKey(null);  // true
id.put(null, "w");     // still one null key; value now "w"

HashMap<String, String> hm = new HashMap<>();
hm.put(null, "v");     // also legal
```

**Listing 1.** Conceptual: null key and null values are first-class. A second `put(null, …)` replaces. `get` needs `containsKey` when values may be null.

`HashMap` is “roughly equivalent to `Hashtable`, except that it is unsynchronized and permits nulls.” `WeakHashMap` also supports the null key and null values. `Hashtable`: any **non-null** object as key or value. `ConcurrentHashMap`: like `Hashtable`, no null key or value. [[Does Hashtable allow null keys or values]] [[Does WeakHashMap allow null keys or values]] [[Does ConcurrentHashMap allow null keys or values]]

> [!warning] “Identity maps should reject null like ConcurrentHashMap”
> Null permission follows `HashMap`, not the concurrent/`Hashtable` rule. Do not probe with `get(null) == null` if you store null values. Do not expect two null keys: identity has one `null`. `putAll` throws if the **argument map** is null; that is not a ban on null entries inside this map.

> [!tip] Interview answer
> **Yes. `IdentityHashMap` allows a null key and null values, like `HashMap` and `WeakHashMap`.** There is only one null key, because keys compare with `==`. `Hashtable` and `ConcurrentHashMap` allow neither. Use `containsKey` when `get` might mean “mapped to null.”
