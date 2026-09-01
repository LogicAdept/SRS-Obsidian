<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Set/HashSet #SRS

# How would you explain HashSet from HashMap?

> [!abstract] Short answer
> **Two different “from HashMap” stories.** The set **type** is a `HashMap` whose keys are the elements. To **copy the keys of an existing map** into a standalone `HashSet`, use `new HashSet<>(map.keySet())`. `map.keySet()` itself is a live view, not a `HashSet`.

## Copy the keys (the one-liner)

`Map.keySet()` returns a `Set` **view** of the keys. It is backed by the map: changes flow both ways. Removal via `Iterator.remove`, `Set.remove`, `removeAll`, `retainAll`, or `clear` **deletes the mapping**. `add` / `addAll` are unsupported.

`HashSet(Collection)` constructs a **new** set containing those elements, with capacity enough for the collection (load factor 0.75). After that copy, mutating the `HashSet` does not change the map, and mutating the map does not change the `HashSet` ([[How do you convert an ArrayList to a HashSet in one line]]).

```java
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.put("b", 2);

Set<String> keysCopy = new HashSet<>(map.keySet());
keysCopy.remove("a");     // map still has "a"

Set<String> keysView = map.keySet();
keysView.remove("b");     // mapping "b" is gone from the map
```

**Listing 1.** The copy constructor snapshots membership. The view is the map’s key side. `new HashSet<>(map.keySet())` throws `NullPointerException` only if the **map reference** is null (`keySet()` is not a null collection).

`new HashSet<>(map.values())` is a set of **values**: duplicate values collapse; it is not “the HashSet of the map.” `entrySet()` is a set of `Map.Entry`, not of keys ([[How do you create a HashMap from a HashSet of Map entries]]).

## The type is already a HashMap of keys

`HashSet` “implements the `Set` interface, backed by a hash table (actually a `HashMap` instance).” Elements are keys; `add`/`contains`/`remove` follow hash-map key rules (one `null`, expected constant time, no order). That implementation story is [[How is HashSet implemented in terms of HashMap]] — do not confuse it with copying `keySet()`.

```d2
direction: down
map: "HashMap<K,V>" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
view: "map.keySet()\nlive Set view, no add" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
copy: "new HashSet<>(keySet)\nindependent HashSet" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

map -> view
view -> copy
```

**Fig. 1.** View vs copy. Internally a `HashSet` you `new` is still a `HashMap`; that is a different object than `map`.

> [!warning] `keySet()` is not a `HashSet`
> The runtime type is a private map view. `add("x")` throws `UnsupportedOperationException`. `remove` on the view **removes from the map**. If you need a mutable set of keys that the map does not see, copy.

> [!warning] Do not pass `entrySet` when you wanted keys
> `new HashSet<>(map.entrySet())` is a set of entries. Clearing it through a view would clear the map; the copy constructor copies entry objects, not keys. For keys only, `keySet()`.

> [!tip] Interview answer
> **To take keys off a `HashMap`, `new HashSet<>(map.keySet())` copies them; `map.keySet()` is a live view that cannot `add` and whose `remove` hits the map.** Separately, `HashSet` itself is implemented as a `HashMap` of elements-as-keys. Those are two different explanations.
