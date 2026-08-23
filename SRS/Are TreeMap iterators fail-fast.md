<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Iteration #SRS

# Are `TreeMap` iterators fail-fast?

> [!abstract] Short answer
> **Yes.** Iterators from every collection view (`keySet`, `values`, `entrySet`) are **fail-fast**: a **structural** change to the map after the iterator is created — other than that iterator’s own `remove` — makes a later iterator operation throw `ConcurrentModificationException` on a best-effort basis.

That matches `HashMap` / [[Are IdentityHashMap iterators fail-fast]]. It is the opposite of weakly consistent navigable maps such as `ConcurrentSkipListMap` (and of [[Are ConcurrentHashMap iterators fail-fast]] / [[Are EnumMap iterators fail-fast]]).

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

**Fig. 1.** Fail-fast views snapshot `modCount` and abort when the map’s structural counter drifts.

`TreeMap` class docs (Java SE 21): view iterators are fail-fast if the map is structurally modified after creation except through that iterator’s `remove`. The same page defines a **structural** modification as any add or delete of mappings; **merely changing the value for an existing key is not structural**. See [[What counts as a structural modification for fail-fast iterators]]. Spliterators on the views are also documented as fail-fast (and ordered / sorted as appropriate).

```java
TreeMap<String, Integer> map = new TreeMap<>();
map.put("a", 1);
map.put("c", 3);

Iterator<String> it = map.keySet().iterator();
map.put("a", 9); // value replace — not structural
it.next();       // OK

map.put("b", 2); // new mapping — structural
it.next();       // ConcurrentModificationException (typical)
```

**Listing 1.** Value replace does not trip fail-fast; inserting a new key does. Exception on the last line is best-effort, not a programming API.

## Not `ConcurrentSkipListMap`

| Map | View iterators |
|-----|----------------|
| `TreeMap` | Fail-fast → may throw `ConcurrentModificationException` |
| `ConcurrentSkipListMap` | Weakly consistent → never CME |

Interview dumps often call the concurrent sibling “fail-safe” and say it “iterates a copy.” Official wording is **weakly consistent**: no CME, may proceed with concurrent updates, may (but need not) reflect later puts/removes — not a full-map clone like CopyOnWrite.

`TreeMap` itself is **not** synchronized. Fail-fast detects overlapping structural mutation during iteration; it does **not** make the map safe for shared writers. For concurrent sorted maps use `ConcurrentSkipListMap` (or synchronize externally / `Collections.synchronizedSortedMap`).

```java
Iterator<Map.Entry<String, Integer>> it = map.entrySet().iterator();
while (it.hasNext()) {
    Map.Entry<String, Integer> e = it.next();
    if (drop(e.getKey())) {
        it.remove(); // allowed: updates expectedModCount
    }
}
```

**Listing 2.** Removing through the **same** iterator is the documented exception to the fail-fast rule.

> [!warning] Do not depend on CME for control flow
> Fail-fast is **best-effort** under unsynchronized concurrent modification. Use it to catch bugs, not as business logic. Prefer [[How do you avoid ConcurrentModificationException while iterating a collection]] (`iterator.remove`, collect-then-remove, or a concurrent collection).

> [!warning] “Fail-safe = clone” for sorted concurrent maps
> Wrong for `ConcurrentSkipListMap`. Prefer **weakly consistent** over “fail-safe snapshot.” `TreeMap` stays fail-fast like `HashMap`.

> [!tip] Interview answer
> **Yes — `TreeMap` view iterators are fail-fast**, like `HashMap`: after creation, a structural put/remove (not a mere value replace, and not that iterator’s own `remove`) can throw `ConcurrentModificationException`. That is bug detection, not a lock; `ConcurrentSkipListMap` iterators are weakly consistent and do not throw CME.
