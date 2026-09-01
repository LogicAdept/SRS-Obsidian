<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration/FailFast #SRS

# How do you remove an element from a collection while iterating?

> [!abstract] Short answer
> **Use that iterator’s `remove()` after `next()`, or `Collection.removeIf` (Java 8; default implementation does the same).** `remove()` deletes the last element `next()` returned, once per `next()`. Do not call `coll.remove(...)` from a fail-fast enhanced `for` — that is a different mutator and usually `ConcurrentModificationException`. Some iterators (`CopyOnWriteArrayList`) reject `Iterator.remove()` with `UnsupportedOperationException`.

## The iterator’s `remove`, not the collection’s

`Iterator.remove()` is the specified way to change the backing collection during a walk. It is optional. The default implementation throws `UnsupportedOperationException`. When supported, it may be called only once per `next()`; otherwise `IllegalStateException` (no `next()` yet, or `remove` already used since the last `next()`). Behavior is unspecified if the collection is modified in any other way while this iterator is in progress, unless the class documents a concurrent-modification policy [[What happens if you call iterator.remove on a collection]].

A fail-fast `ArrayList` iterator’s own `remove` / `add` is the exception to that rule; `list.remove` during the same walk is not. Enhanced `for` compiles to a hidden iterator, so the body cannot call `Iterator.remove()` [[Can you modify a collection while iterating with a for-each loop]], [[What is ConcurrentModificationException]].

`Collection.removeIf(Predicate)` (Java 8) is the bulk form. The default implementation traverses `iterator()` and removes matches with `Iterator.remove()`. If the iterator does not support removal, `UnsupportedOperationException` is thrown on the first match.

`ListIterator.remove()` is the same idea after `next()` or `previous()` (still once per those calls; illegal after `add`) [[How do you iterate a List in reverse using ListIterator]].

`CopyOnWriteArrayList` iterators are a snapshot: they are guaranteed not to throw `ConcurrentModificationException`, and `remove` / `set` / `add` on the iterator throw `UnsupportedOperationException`. Removing from the **list** during a for-each mutates the live list, not the snapshot the loop is walking.

```d2
direction: down
it: "Iterator.next()" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
own: "iterator.remove()\nremoveIf" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
coll: "coll.remove / add\nin the same walk" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
cow: "COW iterator.remove\n→ UOE" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}

it -> own
it -> coll
it -> cow
```

**Fig. 1.** Only the iterator that is driving the loop may structurally remove (when the operation is supported). Collection mutators during a fail-fast walk are unspecified / CME.

```java
class RemoveWhileIterating {
    static void withIterator(java.util.Collection<String> coll) {
        java.util.Iterator<String> it = coll.iterator();
        while (it.hasNext()) {
            if (it.next().equals("Two")) {
                it.remove();
            }
        }
    }

    static void withRemoveIf(java.util.Collection<String> coll) {
        coll.removeIf("Two"::equals);
    }
}
```

**Listing 1.** After `next()` returns `"Two"`, `remove()` drops that element. A second `remove()` before another `next()` is `IllegalStateException`. `removeIf` is the same contract without a manual loop.

```java
class IllegalRemove {
    static void fromForEach(java.util.List<String> list) {
        for (String s : list) {
            if (s.equals("Two")) {
                list.remove(s);
            }
        }
    }
}
```

**Listing 2.** Collection `remove` during enhanced `for`. On `ArrayList` this is the classic one-thread CME (or a silent skip of the tail — `hasNext` does not check `modCount`). Not `Iterator.remove()`.

> [!warning] `remove()` is not `next()`
> Calling `iterator.remove()` before any `next()`, or twice for one `next()`, throws `IllegalStateException`, not CME. Unmodifiable collections and snapshot iterators throw `UnsupportedOperationException` instead of deleting.

> [!warning] For-each cannot reach `Iterator.remove()`
> The iterator exists but is compiler-generated. `list.remove` in that body is the fail-fast / skip story. Prefer an explicit iterator or `removeIf` [[How do you avoid ConcurrentModificationException while iterating a collection]].

> [!tip] Interview answer
> **Call `Iterator.remove()` after `next()`, or use `removeIf`.** That is the iterator’s own delete; `coll.remove` inside a for-each is unspecified and often `ConcurrentModificationException`. `remove()` once per `next()`, or `IllegalStateException`. Copy-on-write iterators do not support `remove` at all.
