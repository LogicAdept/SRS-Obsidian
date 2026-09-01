<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #Java/Exceptions/Unchecked #SRS

# What is fail-fast iterator behavior in Java collections?

> [!abstract] Short answer
> **The iterator fails immediately with `ConcurrentModificationException` if the collection is structurally changed after the iterator was created, except through that iterator’s own `remove` (and list-iterator `add`).** `ArrayList` and `HashMap` view iterators are the usual examples. Detection is **best-effort** (`modCount`), not a lock, and **one thread** is enough. It exists to avoid later nondeterministic traversal, not to make concurrent mutation safe.

## Fail quickly instead of walking a moving structure

General-purpose JRE collections document fail-fast iterators: if the collection is structurally modified at any time after the iterator is created, in any way except through the iterator’s own `remove` (ArrayList also: list-iterator `add`), the iterator throws `ConcurrentModificationException`. The alternative they contrast is “arbitrary, non-deterministic behavior at an undetermined time in the future” [[What is ConcurrentModificationException]], [[What counts as a structural modification for fail-fast iterators]].

**Structural** means add/delete (and on `ArrayList`, an explicit backing-array resize). `List.set` and `HashMap.put` of an **existing** key are not. Enhanced `for` is a hidden fail-fast iterator, so `list.remove` in the body is the classic one-thread case [[How can a single-threaded program get ConcurrentModificationException]].

**`modCount`:** `AbstractList` counts structural modifications. The iterator stores the value at creation (`expectedModCount`). If it differs, `next` / `remove` / `previous` / `set` / `add` throw CME. Not every iterator method checks: OpenJDK `ArrayList.hasNext` is `cursor != size` only.

Fail-fast **cannot be guaranteed** under unsynchronized concurrent modification. CME is best-effort and must not be used for program correctness — only to detect bugs [[How do you avoid ConcurrentModificationException while iterating a collection]].

**Not fail-fast:** `CopyOnWriteArrayList` snapshot (no CME). `ConcurrentHashMap` weakly consistent (no CME). Hashtable `keys()` / Vector `elements()` — not fail-fast; results **undefined**. Do not call those “fail-safe” as if they were COW [[What is the difference between fail-fast and fail-safe iterators]], [[What are examples of fail-safe iterators in Java]].

```d2
direction: down
it: "fail-fast iterator\nexpectedModCount" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ok: "it.remove()\ncounts stay aligned" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
cme: "coll.add / coll.remove\n→ CME on next()" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

it -> ok
it -> cme
```

**Fig. 1.** Fail-fast compares modification counts. The iterator’s own `remove` is the structural change it expects.

```java
class FailFastDemo {
    static void throwsCme(java.util.List<String> list) {
        for (String s : list) {
            list.add("x"); // structural, not iterator.remove
        }
    }
}
```

**Listing 1.** Typical fail-fast failure: one thread, enhanced `for`, collection `add`. CME on a later `next()`. `list.set(0, "x")` would not be this exception.

> [!warning] Best-effort is not a memory barrier
> Two threads without a lock may still corrupt the list **without** CME. Catching the exception does not repair the collection. Do not write `try { iterate } catch (ConcurrentModificationException e)`.

> [!warning] `hasNext` may not throw
> After an illegal write, `ArrayList.hasNext` can still return a boolean. CME is on `next()` / `remove()`, or the loop ends with a skipped tail and no throw. “No exception” is not “still valid.”

> [!tip] Interview answer
> **Fail-fast means the iterator throws `ConcurrentModificationException` if the collection is structurally changed except via that iterator’s `remove` — `ArrayList` and `HashMap` do this, even on one thread.** It uses `modCount` on a best-effort basis. CopyOnWriteArrayList and ConcurrentHashMap iterators are not fail-fast.
