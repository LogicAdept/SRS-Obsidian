<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# What happens if you call `iterator.remove` on a collection?

> [!abstract] Short answer
> **The collection deletes the last element that `next()` returned** (optional). The same fail-fast iterator stays valid. Call it **once per** `next()`; otherwise `IllegalStateException`. If the iterator does not support removal, `UnsupportedOperationException` and the collection is unchanged. This is not `collection.remove(...)`, which typically invalidates a fail-fast iterator [[How do you already iterator for collection if invoke collection.remove]].

## Last `next()`, then the collection shrinks

`Iterator.remove()`: “Removes from the underlying collection the last element returned by this iterator (optional operation). This method can be called only once per call to `next()`.” A plain `Iterator` has no between-elements cursor; `remove` names the element `next()` already handed you. Default implementation throws `UnsupportedOperationException` and does nothing else [[How do you remove an element from a collection while iterating]].

`IllegalStateException` if `next()` has not been called, or `remove` was already called after the last `next()`. `ListIterator.remove()` uses the last `next()` **or** `previous()`, and is illegal after `add` [[Compare Iterator and ListIterator capabilities]].

On `ArrayList` (and other fail-fast types) this iterator’s `remove` is the structural change the fail-fast check **allows**: `modCount` and the iterator’s expected count stay in step, so later `next()` does not throw CME. `CopyOnWriteArrayList` iterators reject `remove` with UOE; mutate the list instead.

`collection.remove(x)` while this iterator is live is the other mutator: successful delete usually means CME on a later `next()` [[How do you already iterator for collection if invoke collection.remove]].

```d2
direction: down
nx: "it.next() → e" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
rm: "it.remove()\ncollection drops e" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
bad: "no next / twice\n→ IllegalStateException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

nx -> rm
nx -> bad
```

**Fig. 1.** The collection changes only after a legal `remove`. ISE means this cursor has no last-returned element.

```java
class IteratorRemoveOnCollection {
    static void dropMatching(java.util.Collection<String> coll) {
        java.util.Iterator<String> it = coll.iterator();
        while (it.hasNext()) {
            if (it.next().isEmpty()) {
                it.remove();
            }
        }
    }
}
```

**Listing 1.** After `remove()`, that empty string is gone from `coll`, `size` is one smaller, and the loop may continue. A second `it.remove()` before another `next()` throws `IllegalStateException`.

> [!warning] `IllegalStateException` is not CME
> Forgetting `next()` does not mean concurrent modification. CME is `coll.remove` / `add` during this iterator’s life. ISE is “nothing to delete for this cursor.”

> [!warning] Optional operation
> Unmodifiable collections and COW snapshot iterators throw `UnsupportedOperationException`; the collection does not change. `removeIf` uses `Iterator.remove()` and fails the same way on the first match.

> [!tip] Interview answer
> **`iterator.remove()` removes from the collection the last element `next()` returned, and the iterator remains usable.** Once per `next()`, or `IllegalStateException`. That is the allowed in-walk delete; `collection.remove` is the CME path on fail-fast types.
