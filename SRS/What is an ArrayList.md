<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# What is an `ArrayList`?

> [!abstract] Short answer
> `java.util.ArrayList` is a **resizable-array `List`**: all optional list operations, `null` allowed, **not synchronized**. It is “roughly equivalent to `Vector`, except that it is unsynchronized.” Internally it is an `Object[]` plus a logical `size()`.

## A growable `List` over an array

```d2
direction: right
api: "List\nget, set, add, remove, size" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
impl: "ArrayList\nObject[] + size\nunsynchronized" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}

api -> impl
```

**Fig. 1.** You usually declare `List<E>`. The implementation is the dynamic array ([[What design idea does ArrayList implement]], [[What backing data structure does ArrayList use internally]]).

Specified costs (Java SE 21): `size` / `isEmpty` / `get` / `set` / `iterator` / `listIterator` are **constant time**; end `add` is **amortized** constant (`n` adds are O(n)); other operations are **linear**, with a low constant factor compared to `LinkedList` ([[Does ArrayList always add elements in O(1) time]]). Capacity ≥ `size()`; `ensureCapacity` can grow ahead of a burst; `trimToSize` shrinks the buffer. Growth policy otherwise unspecified.

It is **not** thread-safe. Concurrent structural use needs an external lock or `Collections.synchronizedList`. Fail-fast iterators throw `ConcurrentModificationException` on a best-effort basis. For many readers and few writes, `CopyOnWriteArrayList` is the concurrent `List` the JDK documents instead ([[What is the difference between ArrayList Vector and CopyOnWriteArrayList]]).

```java
List<String> names = new ArrayList<>();
names.add("Ada");
names.add("Grace");
names.get(0);       // "Ada"
names.size();       // 2
names.contains("Ada");
```

**Listing 1.** Ordinary `List` use. A language array cannot grow; this list can ([[What is the difference between an array and an ArrayList]]). Member of the Java Collections Framework since 1.2.

> [!warning] Empty constructor is empty, not ten elements
> `new ArrayList<>()` has `size() == 0`. The “capacity of ten” is a buffer hint (OpenJDK delays the ten-slot array until the first `add`). `get(0)` throws `IndexOutOfBoundsException` until you `add`.

> [!warning] Not a hash table and not a `LinkedList`
> `contains` is a linear `equals` scan. `LinkedList` is nodes + `Deque` ends. `List.of(...)` is unmodifiable and is not an `ArrayList`.

> [!tip] Interview answer
> **`ArrayList` is Java’s unsynchronized resizable-array `List`.** O(1) index, amortized O(1) append, linear insert/delete in the middle. Use it as the default `List`; reach for `LinkedList` or `CopyOnWriteArrayList` only when their documented tradeoffs match.
