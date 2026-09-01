<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #Java/Collections/Map/TreeMap #SRS

# Does `LinkedHashMap` allow null keys or values?

> [!abstract] Short answer
> **Yes — like `HashMap`: one null key, and null values.** The class “permits null elements.” It extends `HashMap`, whose javadoc allows the null key and null values. A second `put(null, …)` replaces. This is not `TreeMap` (natural order forbids a null key) and not `Hashtable` / `ConcurrentHashMap`.

## Same null policy as `HashMap`

`LinkedHashMap` is a `HashMap` plus a doubly-linked list for encounter order. Optional `Map` operations are provided; null elements are permitted. `get` is specified with the usual null-safe `equals` test (`key==null ? k==null : key.equals(k)`), so a null key is a real mapping, not an error. `get` returning `null` may mean “absent” or “mapped to null”; use `containsKey`. [[What is the difference between HashMap and LinkedHashMap]] [[Does IdentityHashMap allow null keys or values]]

A map still cannot have duplicate keys, so there is **one** null key. Any number of keys may map to `null`.

```d2
direction: down
put: "put(null, v)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
ok: "LinkedHashMap / HashMap\nkeep the mapping" {
  width: 280
  height: 70
  style.fill: "#c8e6c9"
}
tree: "TreeMap natural order\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ht: "Hashtable / ConcurrentHashMap\nreject nulls" {
  width: 300
  height: 70
  style.fill: "#ffcdd2"
}

put -> ok
put -> tree
put -> ht
```

**Fig. 1.** Linked hash maps sit with `HashMap` on nulls. Sorted maps and the synchronized legacy/concurrent pair do not.

```java
LinkedHashMap<String, String> lhm = new LinkedHashMap<>();
lhm.put(null, "v");
lhm.put("k", null);
lhm.get(null);         // "v"
lhm.containsKey(null); // true
lhm.put(null, "w");    // still one null key

HashMap<String, String> hm = new HashMap<>();
hm.put(null, "v");     // same policy
```

**Listing 1.** Conceptual: null key and null values are legal. Access-order vs insertion-order does not change that. `putAll` still throws if the **argument map** is null.

`TreeMap.put` throws `NullPointerException` if the key is null and the map uses natural ordering, or its comparator does not permit null keys. That is the interview mix-up: “ordered map” is not “linked hash map.” [[Can TreeMap have null keys or null values]] [[Does Hashtable allow null keys or values]] [[Does ConcurrentHashMap allow null keys or values]]

> [!warning] “Linked means sorted, so no null key”
> Encounter order is insertion-order or access-order, not `Comparable`. `TreeMap` is the class that NPEs on a null key under natural order. `get(null) == null` is still ambiguous when values may be null.

> [!tip] Interview answer
> **Yes. `LinkedHashMap` allows a null key and null values, the same as `HashMap`.** There is only one null key. `TreeMap` with natural ordering rejects a null key; `Hashtable` and `ConcurrentHashMap` reject null keys and values.
