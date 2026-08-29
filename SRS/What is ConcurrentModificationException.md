<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Collections/Iteration #Java/Collections/Concurrency #SRS

# What is `ConcurrentModificationException`?

> [!abstract] Short answer
> **It is an unchecked `RuntimeException` from a fail-fast iterator (or similar) that detected a structural change it did not make.** `ArrayList`’s enhanced `for` that calls `list.remove` is the usual demo. It is **best-effort**, often **one thread**, and not a lock. Use `Iterator.remove` or `removeIf`.

## Fail-fast, not “two threads required”

`ConcurrentModificationException` is thrown when a method detects a modification that is not allowed during that operation. Fail-fast iterators (`ArrayList`, `HashMap`, and the other general-purpose JRE collections) throw it if the collection is structurally modified after the iterator was created, except through **that iterator’s** `remove` / `add` ([[What is fail-fast iterator behavior in Java collections]], [[What counts as a structural modification for fail-fast iterators]], [[How can a single-threaded program get ConcurrentModificationException]]).

`AbstractList`-style iterators compare `modCount`. If it changes unexpectedly, `next`, `remove`, `previous`, `set`, or `add` throw. That check is optional for subclasses; it is how `ArrayList` behaves. The enhanced `for` uses `iterator()`, so `list.remove(x)` in the loop is the classic single-thread case.

Fail-fast is **best-effort**. Do not write logic that *depends* on catching CME for correctness ([[How do you avoid ConcurrentModificationException while iterating a collection]]).

**Fixes that stay on a fail-fast list:** `Iterator.remove()`; `Collection.removeIf` (default implementation removes via `Iterator.remove()`). Or iterate a copy / collect a new list.

**Different iterator contract:** `ConcurrentHashMap` iterators do **not** throw CME (weakly consistent; one thread should use a given iterator). `CopyOnWriteArrayList` uses a snapshot and never throws CME; its iterator does not support `remove` ([[Are ConcurrentHashMap iterators fail-fast]], [[What is the difference between fail-fast and fail-safe iterators]]). `next()` past the end is `NoSuchElementException`, not CME ([[What is NoSuchElementException]], [[What are common kinds of unchecked exceptions in Java]]).

```d2
direction: down
iter: "fail-fast iterator" {
  width: 280
  height: 50
}
direct: "list.remove / put during for-each" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
own: "iterator.remove / removeIf" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
iter -> direct
iter -> own
```

**Fig. 1.** Structural change through the collection is illegal during fail-fast iteration. The iterator’s own `remove` is allowed.

```java
class Demo {
    static void bad(java.util.List<String> list) {
        for (String s : list) {
            if (s.isEmpty()) {
                list.remove(s);
            }
        }
    }

    static void ok(java.util.List<String> list) {
        java.util.Iterator<String> it = list.iterator();
        while (it.hasNext()) {
            if (it.next().isEmpty()) {
                it.remove();
            }
        }
    }
}
```

**Listing 1.** `bad` typically throws `ConcurrentModificationException` on the next iterator step. `ok` uses the iterator’s `remove`. `list.removeIf(String::isEmpty)` is the same idea.

> [!warning] The name does not mean “you used threads”
> One thread calling `remove` on the list while its own enhanced `for` is running is enough.

> [!warning] Catching CME does not make the loop safe
> Fail-fast is best-effort. The collection may already be in a bad state for this iteration. Change how you mutate; do not swallow the signal. Concurrent maps and copy-on-write lists use other iterator rules — they are not “fail-fast with a try/catch.”

> [!tip] Interview answer
> **`ConcurrentModificationException` is fail-fast: the iterator saw a structural change it did not make — often `list.remove` inside a for-each, even on one thread.** Use `Iterator.remove()` or `removeIf`, or a concurrent/snapshot collection. Do not rely on catching it for correctness.
