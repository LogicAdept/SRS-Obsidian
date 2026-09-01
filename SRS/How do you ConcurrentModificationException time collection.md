<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #Java/Collections/Concurrency #SRS

# How do you ConcurrentModificationException time collection?

> [!abstract] Short answer
> **During a fail-fast walk, do not call `collection.remove` / `add` (or `put` of a new key).** CME is thrown later, on the iterator’s `next()` / `remove()` (not always on `hasNext()`), even on one thread. Avoid it with `Iterator.remove()` / `removeIf`, a copy/`toArray()` walk, or CHM / COW iterators. `ListIterator` is **not** fail-safe. `synchronized` does **not** stop that one-thread CME.

## When it fires, and what actually avoids it

Fail-fast iterators throw `ConcurrentModificationException` if the collection is structurally modified after the iterator is created, except through **that** iterator’s `remove` (list-iterator `add`). Enhanced `for` is a hidden iterator, so `list.remove` in the body is the usual case. The check is on `next` / iterator `remove` (and list-iterator `previous` / `set` / `add`), **best-effort** [[How can a single-threaded program get ConcurrentModificationException]], [[How do you avoid ConcurrentModificationException while iterating a collection]].

Dump “use ListIterator as fail-safe” is wrong. `ArrayList.listIterator()` is fail-fast, same `modCount` story. Extra `set` / `add` / `previous` are list-cursor operations, not a snapshot [[Compare Iterator and ListIterator capabilities]].

**Does avoid CME:** `Iterator.remove()` after `next()`; `removeIf`; iterate `toArray()` / `new ArrayList<>(coll)` (the array/`List` copy is not the fail-fast cursor); `ConcurrentHashMap` iterators (weakly consistent, no CME); `CopyOnWriteArrayList` snapshot iterators (no CME; iterator `remove` is UOE) [[Are ConcurrentHashMap iterators fail-fast]], [[How do you remove an element from a collection while iterating]].

`Collection.toArray()` allocates a **new** array the collection does not keep. For-each over that array uses an index, so later `list.remove` does not CME the array loop.

**Does not avoid one-thread CME:** locking the list while this thread does for-each + `list.remove`. External `synchronized` (or `Collections.synchronizedList`) is for **other threads** mutating structurally. This thread can still break the iterator contract while holding the lock.

```d2
direction: down
during: "during fail-fast iteration" {
  width: 280
  height: 50
}
bad: "ListIterator as fail-safe\nsync + list.remove" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ok: "iterator.remove / removeIf\ntoArray copy\nCHM / COW" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}

during -> bad
during -> ok
```

**Fig. 1.** CME time is the next iterator check after an illegal structural change. Avoidance is a legal mutator or a different cursor, not `ListIterator` magic or a lock on the same `remove`.

```java
class DuringIteration {
    static void stillCme(java.util.List<String> list) {
        synchronized (list) {
            for (String s : list) {
                if (s.isEmpty()) {
                    list.remove(s); // still typically CME — one thread
                }
            }
        }
    }

    static void arrayCopy(java.util.List<String> list) {
        for (Object o : list.toArray()) {
            String s = (String) o;
            if (s.isEmpty()) {
                list.remove(s); // array loop is not the list iterator
            }
        }
    }
}
```

**Listing 1.** `stillCme` is the dump’s `synchronized` idea failing. `arrayCopy` walks a detached array (`toArray` must allocate). Prefer `removeIf` over either for an in-place delete.

> [!warning] `ListIterator` is fail-fast on `ArrayList`
> Same CME as `iterator()`. Use it for `previous` / `set` / `add`, not as a “safe” cursor.

> [!warning] A lock is not a snapshot
> Multi-thread structural mutation needs external sync on `ArrayList`. That is unrelated to this thread’s for-each + `remove`. COW/CHM are different iterator contracts, not faster `ArrayList`.

> [!tip] Interview answer
> **CME shows up on a later iterator `next()`, if you structurally changed a fail-fast collection during that walk — one thread is enough.** Avoid with `Iterator.remove` / `removeIf`, a `toArray`/copy walk, or CHM/COW. ListIterator is not fail-safe; `synchronized` does not fix single-thread `list.remove`.
