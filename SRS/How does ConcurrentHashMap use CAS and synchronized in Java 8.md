<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Versions/8 #Java/Collections/Concurrency #SRS

# How does `ConcurrentHashMap` use CAS and `synchronized` in Java 8?

> [!abstract] Short answer
> **Empty bin: CAS the first `Node` in. Occupied bin: `synchronized` on that first node, then write.** `get` uses neither — it acquire-reads the bin and walks `volatile` `val` / `next`. Segment locks are gone ([[How does ConcurrentHashMap use Segment locks in Java 7]]).

## Two update paths in the same `put`

Java 8 rebuilt the table as a `Node[]` of bins (list, or a `TreeBin` of red-black `TreeNode`s). Table slots are published with `tabAt` / `casTabAt` (acquire / CAS on the array element). There is still no whole-table lock ([[Does ConcurrentHashMap get lock the whole table]]).

`putVal` is a retry loop:

1. Null table → `initTable()`.
2. Bin empty (`tabAt` is null) → `casTabAt` a new `Node`. Success: done, **no monitor**. Failure: another thread won the slot; loop and take the occupied path.
3. Head hash is `MOVED` (`-1`) → a forwarding node; `helpTransfer` and retry on the new table.
4. Otherwise → `synchronized (f)` on the bin head, **re-check** `tabAt` is still `f`, then append or replace on the list / `TreeBin`. After the lock, if the list length reached `TREEIFY_THRESHOLD` (8), `treeifyBin`.

```d2
direction: down
put: "putVal" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
empty: "bin == null\ncasTabAt first Node" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
moved: "head.hash == MOVED (−1)\nhelpTransfer" {
  width: 240
  height: 70
  style.fill: "#fff8e1"
}
lock: "synchronized(head)\nre-check still head\nlist or TreeBin write" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
put -> empty
put -> moved
put -> lock
```

**Fig. 1.** CAS and `synchronized` are different arms of one `put`, not alternatives for the whole map.

The lock object **is** the first node. After you enter the monitor you must see it is still the bin head — a resize or a deleted head would make `f` stale. New list nodes are appended, so a surviving head stays the lock until that node is removed or the bin is forwarded. Other keys in the same bin share that monitor; other bins do not.

Treeification is not “8 collisions ⇒ tree” in every table: if capacity is under `MIN_TREEIFY_CAPACITY` (64), `treeifyBin` resizes instead. Untreeify on split uses `UNTREEIFY_THRESHOLD` (6). `get` hashes, `tabAt`s, matches the head or walks the list / `find` on a negative-hash special node — no CAS, no `synchronized` ([[How does ConcurrentHashMap size work]] is a different striped counter, not this bin lock).

```java
// Conceptual — putVal’s lock story, not a JDK listing
V putVal(K key, V value) {
    int h = spread(key.hashCode());
    for (Node<K,V>[] tab = table;;) {
        Node<K,V> f; int i;
        if (tab == null || tab.length == 0)
            tab = initTable();
        else if ((f = tabAt(tab, i = (tab.length - 1) & h)) == null) {
            if (casTabAt(tab, i, null, new Node<>(h, key, value)))
                break;                 // empty bin: CAS only
        } else if (f.hash == MOVED)    // −1, forwarding node
            tab = helpTransfer(tab, f);
        else {
            synchronized (f) {         // occupied bin: monitor on head
                if (tabAt(tab, i) == f) {
                    // list append/replace, or TreeBin.putTreeVal
                }
            }
            if (binCount >= TREEIFY_THRESHOLD) // 8
                treeifyBin(tab, i);    // tree only if table length >= 64
            break;
        }
    }
    addCount(1L, binCount);
    return oldVal;
}
```

**Listing 1.** Empty-bin CAS can fail; the loop then treats the bin as occupied. `MOVED` is an internal hash, not `key.hashCode()`.

Why segments were dropped, and how this pairs with CAS: [[Why did ConcurrentHashMap drop segment locks in Java 8]]. Broader Java 8 map picture: [[How would you explain ConcurrentHashMap Java 8]].

> [!warning] CAS does not replace `synchronized` on this map
> Interview shorthand “Java 8 is CAS” skips the common colliding-put path. Only the **first** node in an empty bin is installed with CAS. A second key in that bin takes `synchronized` on the head. `get` still takes no lock.

> [!warning] `MOVED == -1` is not your key’s hash
> Forwarding nodes use negative hashes (`MOVED` −1, `TREEBIN` −2, `RESERVED` −3). User keys get `spread` and `HASH_BITS` so normal hashes are non-negative. Do not treat −1 as a failed `hashCode()`. Treeify at 8 also needs table size ≥ 64; a tiny table resizes first.

> [!tip] Interview answer
> **Java 8 `ConcurrentHashMap` dropped segment locks.** `put` CASes the first node into an empty bin and `synchronized`s on the bin head when the bin already has a node — then re-checks that head is still first. `get` is volatile/acquire reads only. Lists treeify at 8 nodes once the table is large enough (64). `MOVED` (−1) means “this bin has moved; help resize.”
