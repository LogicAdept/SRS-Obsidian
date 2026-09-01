<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #Java/Versions/8 #SRS

# How does `HashMap` behave when two keys have the same `hashCode` but `equals` is false?

> [!abstract] Short answer
> **Both mappings stay.** Same `hashCode` is a **collision**, not equality. The mixed hash picks one bucket; `equals` (after `==`) decides whether to **replace** a value or **insert** another node. Unequal keys with the same hash share that bin as a list, or as a tree once the bin is long enough (Java 8+).

## `hashCode` picks the bin; `equals` picks the node

`Object.hashCode` does **not** require unequal objects to have distinct hashes. It only requires: if `equals` is true, `hashCode` is equal. Two keys with `equals == false` and the same `hashCode` are therefore legal, and a `HashMap` may hold **both**. Overwrite happens only when the keys are the same mapping: `key == k` or `key.equals(k)`. [[Why can two unequal objects share the same hashCode value]] [[Can a HashMap contain two equal keys at the same time]]

OpenJDK 21 `HashMap.hash` mixes `key.hashCode()` with `h ^ (h >>> 16)`, then the bucket is `(n - 1) & hash`. Equal `hashCode`s therefore land in the **same** slot. The index is not the raw `hashCode`. [[When does a hashCode collision occur in a HashMap]] [[What is the internal structure of HashMap]]

```d2
direction: down
put: "put(k2, v2)\nhashCode(k2) == hashCode(k1)\nk1.equals(k2) == false" {
  width: 360
  height: 90
  style.fill: "#e3f2fd"
}
bin: "same bucket\n(n-1) & mixedHash" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
walk: "walk nodes:\n== then equals" {
  width: 260
  height: 70
  style.fill: "#ffe0b2"
}
ins: "append new node\n(or tree insert)" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

put -> bin
bin -> walk
walk -> ins
```

**Fig. 1.** Collision path: one bin, no equal key, a second entry. `put` does not replace `k1`’s value.

On `put`, if the slot is empty, the node goes there. If the slot has nodes, OpenJDK walks them: match stored `hash`, then identity, then `equals`. No match in a **list** bin: link a new node on the **tail** (`p.next = newNode(...)`). If the head is already a `TreeNode`, insertion is `putTreeVal`, not “append to a list.” After a list bin reaches `TREEIFY_THRESHOLD` (8), `treeifyBin` either **resizes** (table smaller than `MIN_TREEIFY_CAPACITY` 64) or turns the bin into a tree. `get` is the same walk: first node, then tree or chain. [[What are hash collisions in HashMap bucket chains]] [[Is equals invoked when a HashMap bucket contains a single element]]

```java
final class Collide {
    final String id;
    Collide(String id) { this.id = id; }

    @Override public int hashCode() { return 42; }

    @Override public boolean equals(Object o) {
        return o instanceof Collide c && id.equals(c.id);
    }
}

Map<Collide, String> map = new HashMap<>();
map.put(new Collide("a"), "A");
map.put(new Collide("b"), "B");
map.size(); // 2
map.get(new Collide("a")); // "A" — equals distinguishes the colliding keys
```

**Listing 1.** Same `hashCode`, different `equals` → two mappings. A dump that says “the second `put` overwrites because the hashes match” is describing `equals`, not `hashCode`.

`HashMap` javadoc: many keys with the same `hashCode()` are “a sure way to slow down” a hash table; if keys are `Comparable`, comparison may break ties (the tree). A map of only colliding keys is still correct; `get`/`put` become linear in the bin, then tree-ish. [[What happens to HashMap if all keys share the same hashCode]] [[How does HashMap handle collisions]]

> [!warning] Same hash is not the same key — and the bin is not always a list
> Interview answers that stop at “added at the end of the linked list” miss Java 8+ trees and miss `==` before `equals`. They also confuse collision with identity: `put` replaces only when `equals` holds. Keep `hashCode` consistent with `equals` so equal keys share a bin **and** match; colliding unequal keys are allowed, just slower. [[Why should equals and hashCode be overridden together]]

> [!tip] Interview answer
> **If two keys have the same `hashCode` but `equals` is false, `HashMap` keeps both. The hash chooses the bucket; `equals` (after `==`) decides replace versus insert. Colliding keys chain in that bin, and Java 8+ may treeify a long bin. Same hash never means “overwrite.”**
