<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Collections/Iteration/FailFast #SRS

# How would you explain write collection throw ConcurrentModificationException?

> [!abstract] Short answer
> **One thread: fail-fast iterator (enhanced `for`) plus a structural write on the collection — `add`, `remove` at an index, `remove(Object)` of a present element, `put` of a new key.** CME is thrown on a later iterator `next()`, not always at the `list.remove` line. `Iterator.remove()` is the write that does **not** throw. The name does not require two threads.

## A write the iterator did not own

Fail-fast iterators throw `ConcurrentModificationException` if the collection is structurally modified after the iterator is created, except through **that** iterator’s `remove` (list-iterator `add`). Enhanced `for` is a hidden iterator, so `list.add` / `list.remove` in the body is that illegal write — **one thread is enough** [[How can a single-threaded program get ConcurrentModificationException]], [[What is ConcurrentModificationException]], [[Can you modify a collection while iterating with a for-each loop]].

`List.set` and `HashMap.put` of an **existing** key are not structural [[What counts as a structural modification for fail-fast iterators]]. `it.remove()` after `it.next()` is the specified in-walk delete [[How do you remove an element from a collection while iterating]].

Dump `list.remove(1)` on `List<Integer>` is `remove(int index)`, not `remove(Object)`. Both are structural if they actually delete. On `[1, 2, 3]` the next `next()` typically CME. On a two-element list, `remove(1)` can make `cursor == size` so `hasNext` is false and **no** CME — the tail was dropped silently (`ArrayList.hasNext` does not check `modCount`).

```d2
direction: down
fe: "for (E e : list)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
w: "list.add / list.remove\n(not it.remove)" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
cme: "it.next() → CME" {
  width: 220
  height: 50
  style.fill: "#ffebee"
}

fe -> w -> cme
```

**Fig. 1.** The write hits the collection. The exception hits the iterator’s next check.

```java
class WriteThrowsCme {
    public static void main(String[] args) {
        java.util.List<Integer> list = new java.util.ArrayList<>();
        list.add(1);
        list.add(2);
        list.add(3);
        for (Integer n : list) {
            list.remove(1); // List.remove(int) — structural; typically CME
        }
    }

    static void objectRemoveAlsoCme(java.util.List<Integer> list) {
        for (Integer n : list) {
            list.remove(Integer.valueOf(1));
        }
    }
}
```

**Listing 1.** Single-thread CME demo. `remove(1)` is index 1, not “Integer 1”. Three elements make CME on the second iterator `next()` typical; do not rely on CME for a two-element list.

> [!warning] `List.remove(1)` is an index
> Autoboxing does not apply to `remove(int)`. Use `remove(Integer.valueOf(1))` if you meant the element. Either write can CME; they delete different things.

> [!warning] The throw is usually the next `next()`, not the write
> Fail-fast is best-effort. `hasNext` on `ArrayList` can return false after a write and skip CME. Catching CME is not a write API.

> [!tip] Interview answer
> **Write a one-thread for-each over an `ArrayList` and `add`/`remove` on the list inside the loop — CME on a later `next()`.** That write is structural and not `Iterator.remove()`. `set` of an existing slot is not this exception. Two threads are not required.
