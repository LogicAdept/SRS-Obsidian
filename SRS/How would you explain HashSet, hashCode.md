<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/HashSet #Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Immutability #SRS

# What happens if you change `hashCode` fields of an object in a `HashSet`?

> [!abstract] Short answer
> **`contains` / `remove` typically miss, and the `Set` contract calls that unspecified.** `HashSet` is a `HashMap` whose keys are the elements. After you change a field that `equals` / `hashCode` use, lookup hashes to a **different** bucket than the one that still holds the object. You have not deleted it — you just cannot find it by value.

## `HashSet` looks up like a `HashMap` key

`HashSet` is “backed by a hash table (actually a `HashMap` instance).” `add` / `contains` / `remove` treat two elements as the same when `Objects.equals` is true, after the element’s `hashCode` picks a bucket — the same path as a `HashMap` key. Constant-time `contains` assumes hashes **disperse**. [[How is HashSet implemented in terms of HashMap]] [[What is the difference between HashMap and HashSet]]

The `Set` interface: behavior is **not specified** if you change an element in a way that affects `equals` comparisons while it is in the set. That is the same warning `Map` gives for mutable keys. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]]

```text
add(e)                 bucket ← e.hashCode()
mutate e's equals/hash fields
contains(e)            bucket ← new hashCode()
                       stored node is still in the old bucket
                       → typically false
remove(e)              same miss
size()                 still counts e
```

**Listing 1.** Lookup uses the **current** hash; the table slot does not move. [[What requirements apply to keys used in a HashMap]]

```d2
direction: down
add: "add(e)\nbucket from hashCode" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
mut: "Change equals / hashCode fields" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
miss: "contains(e) / remove(e)\ntypically miss" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}

add -> mut -> miss
```

**Fig. 1.** The element stays in the old bin. Value lookup does not walk the whole table.

```java
final class Item {
    int id;
    Item(int id) { this.id = id; }

    @Override
    public boolean equals(Object o) {
        return (o instanceof Item i) && id == i.id;
    }

    @Override
    public int hashCode() {
        return id;
    }
}

Item e = new Item(1);
Set<Item> set = new HashSet<>();
set.add(e);
e.id = 2;
set.contains(e); // typically false — unspecified Set behavior
set.remove(e);   // typically false
set.size();      // still 1
```

**Listing 2.** Conceptual: mutate after `add`. Prefer immutable elements (`String`, records with immutable components). [[Why are mutable keys such as byte arrays risky in a HashMap]]

A `HashMap` key has the same trap. Identity maps are the exception: mutating fields does not change `==`. [[Must IdentityHashMap keys be immutable]]

> [!warning] “Lost” is not `remove`
> Interview shorthand “you lose the object” means **lost to `contains`/`remove`**, not GC. The set still references it (`size` stays up; iteration can still visit it). You may be unable to drop it except by iterating and removing through the iterator, or `clear()`. Do not mutate `equals`/`hashCode` state of a live set element.

> [!tip] Interview answer
> **`HashSet` is a `HashMap` of elements. Change a field used by `hashCode`/`equals` after `add`, and `contains` usually returns false — the contract says unspecified.** The object is still in the table, just in the old bucket. Use immutable elements, or don’t mutate them while they sit in the set.
