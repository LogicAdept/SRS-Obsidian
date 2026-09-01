<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/WeakHashMap #Java/Collections/Map/HashMap #Java/Collections/Map/Hashtable #Java/Collections/Map/ConcurrentHashMap #SRS

# Does `WeakHashMap` allow null keys or values?

> [!abstract] Short answer
> **Yes — both the null key and null values.** Same permission as `HashMap`. `Hashtable` and `ConcurrentHashMap` reject both. The null-key mapping is **not** dropped by GC: internally the key is a strongly held sentinel, so that entry stays until you `remove` it. Other keys are weak.

## Nulls are legal; the null key is not a weak object

The class javadoc: both null values and the null key are supported. Lookup still uses the usual `equals` rule (`key==null ? k==null : key.equals(k)` on `get`/`remove`). One null key: a second `put(null, …)` replaces. `get` returning `null` may mean absent or mapped-to-null; use `containsKey`. [[What is WeakHashMap used for]] [[Does IdentityHashMap allow null keys or values]] [[Does LinkedHashMap allow null keys or values]]

Ordinary keys sit in `WeakReference`s. A null key cannot be a referent that the collector clears, so the implementation stores a private sentinel (`NULL_KEY`) and unmasks it for callers. That sentinel is a static object, always reachable, so the null-key entry is **not** expunged when “nothing else points at null.” Values are ordinary **strong** references (including `null`).

```d2
direction: down
put: "put(null, v)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
ok: "WeakHashMap / HashMap\nkeep it; null key stays" {
  width: 300
  height: 80
  style.fill: "#c8e6c9"
}
no: "Hashtable / ConcurrentHashMap\nreject" {
  width: 300
  height: 70
  style.fill: "#ffcdd2"
}

put -> ok
put -> no
```

**Fig. 1.** Null *permission* matches `HashMap`. Null-key *lifetime* does not match other weak keys.

```java
WeakHashMap<String, String> w = new WeakHashMap<>();
w.put(null, "v");
w.put("k", null);
w.get(null);          // "v"
w.containsKey(null);  // true
w.put(null, "w");     // still one null key

Object k = new Object();
WeakHashMap<Object, String> weak = new WeakHashMap<>();
weak.put(k, "memo");
k = null;             // this entry may disappear after GC
// weak.get(null) is the null-key mapping, not k
```

**Listing 1.** Conceptual: null key and null values are first-class. Dropping a *non-null* key’s last strong ref is the weak-eviction story; dropping “the null key” is not. [[What happens to a WeakHashMap entry when the last strong reference to the key is dropped]]

`HashMap` permits the null key and null values. `Hashtable`: any **non-null** object as key or value. `ConcurrentHashMap`: no null key or value. `putAll` throws if the **argument map** is null; that is not a ban on null entries. [[Does Hashtable allow null keys or values]] [[Does ConcurrentHashMap allow null keys or values]]

> [!warning] “WeakHashMap will GC the null key too”
> There is no weakly reachable null object. The sentinel keeps that mapping until you remove it. Do not use `get(null) == null` to mean “absent” if you store null values. A strong value that points back at a **non-null** key still pins that key.

> [!tip] Interview answer
> **Yes. `WeakHashMap` allows a null key and null values, like `HashMap`.** There is only one null key, and that mapping is not cleared by the collector because null is stored as a sentinel, not as a weak referent. `Hashtable` and `ConcurrentHashMap` allow neither.
