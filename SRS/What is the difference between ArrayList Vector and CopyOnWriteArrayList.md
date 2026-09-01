<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/List/ArrayList #Java/Collections/List/Vector #SRS

# What is the difference between `ArrayList`, `Vector`, and `CopyOnWriteArrayList`?

> [!abstract] Short answer
> All three are resizable, indexable lists. `ArrayList` is unsynchronized. `Vector` is a synchronized legacy `List` (since 1.0); use `ArrayList` when you do not need thread safety. `CopyOnWriteArrayList` is a concurrent list that **copies the backing array on every mutation**, aimed at many traversals and few writes.

## Three lists, three concurrency stories

```d2
direction: right
al: "ArrayList\nunsynchronized\nfail-fast iterator" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
vec: "Vector\nsynchronized methods\nfail-fast iterator" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
cow: "CopyOnWriteArrayList\ncopy on mutate\nsnapshot iterator" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Same `List` shape; they differ in locking, iterators, and write cost.

`ArrayList` is “roughly equivalent to `Vector`, except that it is unsynchronized.” `get` / `set` are constant time; end `add` is amortized constant time. Growth policy is unspecified beyond that amortized cost. Concurrent structural use needs an external lock or `Collections.synchronizedList` ([[What is the difference between an array and an ArrayList]]). Iterators are fail-fast (`ConcurrentModificationException`).

`Vector` (Java 1.0, retrofitted as `List` in 1.2) **is synchronized**, unlike the “new collection implementations.” If thread safety is not needed, the API recommends `ArrayList` instead ([[Why was ArrayList added when Vector already existed]]). `iterator` / `listIterator` are still fail-fast. `elements()` returns a non-fail-fast `Enumeration` whose result is **undefined** if the vector is structurally modified during enumeration. Default `Vector()` uses capacity 10 and `capacityIncrement` 0; when capacity must grow and the increment is ≤ 0, the new array is **twice** the old capacity (or `minCapacity` if that is still larger). `ArrayList` does not document that doubling rule.

`CopyOnWriteArrayList` (Java 1.5) is a thread-safe `ArrayList` variant: every mutative `add` / `set` / … allocates a **fresh copy** of the array. That is “ordinarily too costly,” but can win when **traversals vastly outnumber mutations**, and when you do not want to lock readers. The iterator is a **snapshot** of the array at construction: it never throws `ConcurrentModificationException`, it does not see later adds/removes/sets, and `remove` / `set` / `add` on the iterator throw `UnsupportedOperationException`. No extra lock is required while traversing. Actions before a publish happen-before later access/removal in another thread.

```java
List<String> local = new ArrayList<>();
local.add("a");

Vector<String> locked = new Vector<>();
locked.add("a");

CopyOnWriteArrayList<String> cow = new CopyOnWriteArrayList<>();
cow.add("a");
cow.addIfAbsent("a"); // still ["a"]; ArrayList/Vector have no addIfAbsent
```

**Listing 1.** Same `add`, different concurrency. `addIfAbsent` (and `addAllAbsent`) exist only on `CopyOnWriteArrayList`.

`Collections.synchronizedList` is the documented wrapper when you want an `ArrayList` plus a lock. Traversal must still be in `synchronized (list) { … }`; skipping that is undefined. `CopyOnWriteArrayList` is the list that documents lock-free snapshot iteration.

> [!warning] Synchronized `Vector` is not a snapshot
> A thread-safe `add` does not make a `for` loop safe. `Vector` iterators are fail-fast: another thread’s structural change can throw `ConcurrentModificationException`. `CopyOnWriteArrayList` iterators do not throw that; they also **miss** writes that happen after the snapshot.

> [!warning] Copy-on-write is not a faster `Vector`
> Each write copies the whole array; `removeAll` / `retainAll` are called out as especially expensive. Prefer `ArrayList` on one thread. Prefer `CopyOnWriteArrayList` only for read-mostly, short lists. `Vector` is the coarse synchronized 1.0 list, not the default concurrent choice.

> [!tip] Interview answer
> **`ArrayList` is the ordinary unsynchronized resizable list. `Vector` is the old synchronized one — use `ArrayList` unless you still need that API. `CopyOnWriteArrayList` copies the array on every write so readers can iterate a snapshot without a lock; that is for many reads and rare writes, not a general `Vector` replacement.**
