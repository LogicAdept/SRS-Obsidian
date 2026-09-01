<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/Concurrency/CopyOnWrite #SRS

# What is the difference between `CopyOnWriteArrayList` and `ArrayList`?

> [!abstract] Short answer
> `ArrayList` mutates one backing array in place and is unsynchronized. `CopyOnWriteArrayList` (Java 1.5) is a thread-safe `List` that **replaces** that array on every mutative `add` / `set` / `remove`. Iterators are a **snapshot** (no `ConcurrentModificationException`); `ArrayList` iterators are **fail-fast**.

## In-place growth vs copy-on-write

```d2
direction: down
al: "ArrayList\none array, grows in place\nexternal lock if shared" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
cow: "CopyOnWriteArrayList\nwrite → new array copy\nreaders use last published array" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
it: "iterator()\nArrayList: fail-fast\nCOWAL: snapshot reference" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}

al -> it
cow -> it
```

**Fig. 1.** Writes copy only on `CopyOnWriteArrayList`. Creating an iterator does **not** copy; it holds a reference to the array that was current then.

`ArrayList` is the ordinary resizable list: `get`/`set` constant time, end `add` amortized constant, growth policy otherwise unspecified ([[What is the difference between an array and an ArrayList]]). It is **not** synchronized. Concurrent structural use needs an external lock or `Collections.synchronizedList`. That wrapper still requires `synchronized (list)` around iterator/`Spliterator`/`Stream` traversal ([[What is the difference between ArrayList Vector and CopyOnWriteArrayList]]).

`CopyOnWriteArrayList` is documented as a thread-safe **variant of `ArrayList`**, not a faster one. Mutative operations make a **fresh copy** of the underlying array. That is “ordinarily too costly,” and pays off when **traversals vastly outnumber mutations**, or when you cannot/will not lock readers. Both are `List`s: duplicates and `null` are allowed. `CopyOnWriteArrayList` also implements `RandomAccess` and adds `addIfAbsent` / `addAllAbsent`.

```java
List<String> a = new ArrayList<>();
a.add("a");
var ait = a.iterator();
a.add("b"); // structural modification
try {
    ait.next(); // typically ConcurrentModificationException
} catch (ConcurrentModificationException expected) {
    // fail-fast, best-effort — do not depend on this throw
}

CopyOnWriteArrayList<String> c = new CopyOnWriteArrayList<>();
c.add("a");
var cit = c.iterator();
c.add("b");           // copies the array; iterator still sees ["a"]
cit.next();            // "a" — no ConcurrentModificationException
// cit.remove();       // UnsupportedOperationException
c.addIfAbsent("a");   // still one "a"; ArrayList has no such method
```

**Listing 1.** `ArrayList` fail-fast vs snapshot iterator. `ArrayList`’s own `Iterator.remove` / `add` are the documented exception to fail-fast; `CopyOnWriteArrayList` iterators reject `remove` / `set` / `add`.

The snapshot “uses a **reference** to the state of the array at the point that the iterator was created.” That array does not change for the iterator’s lifetime, so interference is impossible. Later list writes are invisible to that iterator. No extra synchronization is needed while traversing.

> [!warning] Copy happens on write, not on `iterator()`
> A dump that says “a new array is allocated every time you create an iterator” has the mechanism backwards. Writes install a new array. `iterator()` / `listIterator()` / `spliterator()` snapshot by **reference**. Readers are cheap; a large `add` is an O(n) copy.

> [!warning] Fail-fast is not a contract you wait on
> `ArrayList` documents `ConcurrentModificationException` as **best-effort**. Do not write tests or production logic that require `add` after `iterator()` to throw. On `CopyOnWriteArrayList`, iterator mutators always throw `UnsupportedOperationException` — that one is specified.

> [!tip] Interview answer
> **`ArrayList` is unsynchronized and fail-fast: one backing array, in-place growth. `CopyOnWriteArrayList` copies that array on every write so iterators can walk a snapshot without a lock and without `ConcurrentModificationException`. Use it for many reads and rare writes; for a single thread, keep `ArrayList`.**
