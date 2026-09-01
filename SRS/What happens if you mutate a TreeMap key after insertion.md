<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Immutability #SRS

# What happens if you mutate a `TreeMap` key after insertion?

> [!abstract] Short answer
> **Unspecified.** `Map` forbids changing a key in a way that affects `equals` while it sits in the map. `TreeMap` looks up by **`compare` / `compareTo`**, so changing comparison fields is the same class of bug: the node stays where it was inserted; later `get` / `containsKey` / `remove` can **miss**. Mutating **values** does not move nodes. Use immutable keys, or **remove, then mutate, then `put`**.

## The tree is built from the key at `put` time

`put` walks the red-black tree with the key’s then-current order and hangs a node there. `get` (and `remove`) start at the root and compare the **search key’s current** `compareTo`/`compare` with **each node’s current** key. Nothing re-links the node when you assign a field on that object. If those fields changed, the walk and the node’s position disagree — a miss is normal, a hit is luck.

The `Map` contract states the behavior is **not specified** if you change a key so that `equals` comparisons change. For `TreeMap`, sameness is compare-zero ([[How does TreeMap decide whether two keys are the same]]). Fields that participate in `compareTo` / the constructor `Comparator` (and usually `equals`) are the ones that must stay stable ([[What types can you use as TreeMap keys]]). Hash maps have the same rule for `hashCode` / `equals` ([[Why is a byte array a poor or unsafe choice for a HashMap key]]).

Values are not in the order. Replacing a value, or mutating a mutable value object, is not a structural modification and does not by itself invalidate key search. A map that contains **itself as a key** is also forbidden; containing itself as a **value** is allowed but makes `equals`/`hashCode` of the map ill-defined.

`TreeSet` elements are `TreeMap` keys, so mutating a set element after `add` is the same unspecified case ([[Is TreeSet implemented using TreeMap]]).

```d2
direction: down
put: "put(k, v)\nnode placed by compare(k)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
mut: "mutate k's order fields" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
get: "get(k) walks as if new order\nnode still on the old path" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
put -> mut -> get
```

**Fig. 1.** Insertion position is not updated. Search uses live `compare`.

```java
import java.util.TreeMap;

class Demo {
    static final class Id implements Comparable<Id> {
        int n;
        Id(int n) { this.n = n; }
        public int compareTo(Id o) { return Integer.compare(n, o.n); }
    }

    static void unspecifiedAfterMutate() {
        var m = new TreeMap<Id, String>();
        var k = new Id(1);
        m.put(k, "a");
        m.put(new Id(3), "c");
        k.n = 2;            // unspecified from here
        m.get(k);           // often null — walk uses n==2, node still where 1 was
        m.remove(k);        // can miss for the same reason
    }

    static void removeThenPut() {
        var m = new TreeMap<Id, String>();
        var k = new Id(1);
        m.put(k, "a");
        m.remove(k);        // while n is still 1
        k.n = 2;
        m.put(k, "a");
    }
}
```

**Listing 1.** `Id` is a mutable comparable on purpose. After `k.n = 2`, `get`/`remove` are unspecified. Change the key only off the map.

> [!warning] Unspecified is not a compiler error
> `put` / `get` / `entrySet` still compile and run. You may see a missing mapping, a key that iteration still visits, or an order that no longer matches `compareTo`. None of that is a guaranteed diagnostic. Do not write a test that “proves” a particular broken printout.

> [!warning] `remove` after the mutation can fail too
> Dump advice to “remove and re-insert” only works if you **remove first**, while comparison fields still match the node’s position. After you mutate, `remove(k)` uses the same broken walk as `get`. Prefer `String`, wrappers, records, or other immutable keys.

> [!tip] Interview answer
> **Unspecified — `TreeMap` never re-sorts a key you mutate in place. Lookup uses live `compare`/`compareTo` against nodes left where `put` placed them, so `get` and even `remove` can miss. Keep keys immutable, or remove, change, put. Mutating values is fine; mutating key order fields is not.**
