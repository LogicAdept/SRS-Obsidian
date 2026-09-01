<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/Collections/Iteration/FailFast #SRS

# Are `IdentityHashMap` iterators fail-fast?

> [!abstract] Short answer
> **Yes.** Iterators from every collection view (`keySet`, `values`, `entrySet`) are **fail-fast**: a **structural** change to the map after the iterator is created — other than that iterator’s own `remove` — makes a later iterator operation throw `ConcurrentModificationException` on a best-effort basis.

`HashMap` uses the same fail-fast story for its view iterators. That is **not** locking and is the opposite of [[Are ConcurrentHashMap iterators fail-fast]] (weakly consistent views that do **not** throw `ConcurrentModificationException`).

## What “fail-fast” means here

```d2
direction: down
create: "Create iterator\nexpectedModCount = modCount" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
next: "next() / hasNext path\ncompares modCount" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
ok: "modCount == expected\n→ continue" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
cme: "modCount != expected\n→ ConcurrentModificationException" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
safe: "iterator.remove()\nupdates expectedModCount" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

create -> next
next -> ok
next -> cme
ok -> safe: allowed remove
```

**Fig. 1.** OpenJDK’s `IdentityHashMapIterator` stores `expectedModCount` and checks it against the map’s `modCount` before advancing or removing.

A **structural** modification is an add or delete of a mapping. Replacing the value for a key that is already present is **not** structural (same wording as `HashMap`). See [[What counts as a structural modification for fail-fast iterators]].

```java
Map<Object, String> map = new IdentityHashMap<>();
Object key = new Object();
map.put(key, "a");

Iterator<Object> it = map.keySet().iterator();
map.put(key, "b"); // value replace — not structural
it.next();          // OK

map.put(new Object(), "c"); // new mapping — structural
it.next();                  // ConcurrentModificationException (typical)
```

**Listing 1.** Value replace does not bump the fail-fast counter; inserting a new key does. Exception on the last line is best-effort, not a programming API.

## Same pattern as `HashMap`, not as `ConcurrentHashMap`

| Map | View iterators |
|-----|----------------|
| `IdentityHashMap` / `HashMap` | Fail-fast → may throw `ConcurrentModificationException` |
| `ConcurrentHashMap` | Weakly consistent → do **not** throw CME |

`IdentityHashMap` itself is **not** synchronized. Fail-fast detects concurrent or overlapping structural mutation during iteration; it does **not** make the map safe for shared mutation. For concurrent access you still need external synchronization or a concurrent map.

> [!warning] Do not depend on CME for control flow
> The class javadoc states fail-fast is **best-effort** under unsynchronized concurrent modification. Use it to catch bugs, not as business logic. Prefer [[How do you avoid ConcurrentModificationException while iterating a collection]] (`iterator.remove`, collect-then-remove, or a concurrent collection).

```java
Iterator<Map.Entry<Object, String>> it = map.entrySet().iterator();
while (it.hasNext()) {
    Map.Entry<Object, String> e = it.next();
    if (drop(e.getKey())) {
        it.remove(); // allowed: updates expectedModCount
    }
}
```

**Listing 2.** Removing through the **same** iterator is the documented exception to the fail-fast rule.

> [!tip] Interview answer
> **Yes — `IdentityHashMap` view iterators are fail-fast, like `HashMap`.** After creation, a structural put/remove on the map (not a mere value replace, and not that iterator’s own `remove`) can throw `ConcurrentModificationException`. That is bug detection, not a lock; `ConcurrentHashMap` iterators are weakly consistent and do not throw CME.
