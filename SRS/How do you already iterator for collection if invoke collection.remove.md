<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Collections/Iteration/FailFast #SRS

# How do you already iterator for collection if invoke collection.remove?

> [!abstract] Short answer
> **A fail-fast iterator created earlier becomes invalid if `collection.remove(...)` actually deletes an element.** The next `next()` / `remove()` (and list-iterator `previous` / `set` / `add`) typically throws `ConcurrentModificationException`. `hasNext()` on `ArrayList` often still returns a boolean — it does **not** check `modCount`. Use `iterator.remove()` if this iterator is the one walking. Concurrent / snapshot iterators do not throw CME.

## `Collection.remove` is not this iterator’s `remove`

`Iterator` contract: behavior is unspecified if the backing collection is modified during the walk in any way other than **this** iterator’s `remove`. Fail-fast JRE collections detect that via `modCount` and throw CME on the iterator operations that check it [[What is ConcurrentModificationException]], [[What happens to an iterator if the backing collection is modified externally]].

`Collection.remove(Object)` is a **collection** mutator. A successful remove is structural (an element left the collection). It does **not** update the iterator’s `expectedModCount`. One thread is enough: create the iterator, call `coll.remove`, then `it.next()` [[How can a single-threaded program get ConcurrentModificationException]], [[What counts as a structural modification for fail-fast iterators]].

If `remove` finds **no** matching element, the collection is unchanged — no structural modification, the iterator stays valid.

`ArrayList.Itr.next()` / `remove()` call `checkForComodification`; `hasNext()` is `cursor != size` only. So after `coll.remove`, `hasNext()` may still look “fine” and the CME appears on `next()`. Some `remove`s that shift the tail so `cursor == size` end the loop **without** CME — still a corrupted walk.

The legal in-walk delete is `it.remove()` after `it.next()` — that iterator owns the change [[How do you remove an element from a collection while iterating]]. `CopyOnWriteArrayList` / `ConcurrentHashMap` iterators do not throw CME for later `coll.remove`.

```d2
direction: down
it: "Iterator it = coll.iterator()" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
rm: "coll.remove(x)\nnot it.remove()" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
nx: "it.next() / it.remove()\n→ CME (fail-fast)" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

it -> rm -> nx
```

**Fig. 1.** The iterator already exists. A later successful `Collection.remove` is an external structural change for that cursor.

```java
class IteratorThenCollectionRemove {
    static void invalidates(java.util.List<String> list) {
        java.util.Iterator<String> it = list.iterator();
        list.remove("a"); // structural if "a" was present
        it.next();        // typically ConcurrentModificationException
    }

    static void ownedByIterator(java.util.List<String> list) {
        java.util.Iterator<String> it = list.iterator();
        while (it.hasNext()) {
            if (it.next().equals("a")) {
                it.remove();
            }
        }
    }
}
```

**Listing 1.** `invalidates` is the dump scenario. `ownedByIterator` is the specified mutator for that same iterator.

> [!warning] Not every iterator method throws immediately
> On `ArrayList`, `hasNext` does not check `modCount`. CME is best-effort. Do not write `if (it.hasNext())` as proof the iterator is still valid after `coll.remove`.

> [!warning] No-op `remove` is not a modification
> `set.remove(missing)` returns `false` and leaves the set unchanged. The existing iterator is still valid. Concurrent maps never used CME for this story.

> [!tip] Interview answer
> **If you already have a fail-fast iterator and then call `collection.remove` (and something is actually removed), the next `next()` or iterator `remove()` typically throws `ConcurrentModificationException`.** One thread is enough. `hasNext` may not throw. To delete during this walk, use `iterator.remove()`, not `collection.remove`.
