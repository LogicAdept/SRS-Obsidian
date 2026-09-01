<!--
reps: 0
priority: 0
-->
#Java/Collections/List #SRS

# Which classes implement the Java List interface?

> [!abstract] Short answer
> **Collections Framework workhorses: `ArrayList`, `LinkedList`, `Vector` (and `Stack`), plus `CopyOnWriteArrayList`.** Skeletal types: `AbstractList` and `AbstractSequentialList`. Many **`List` instances are not those class names**: `List.of` / `List.copyOf`, `Arrays.asList`, `Collections.synchronizedList` / `unmodifiableList`. Program to `List`; pick a class for cost and concurrency.

## Named implementations vs other `List` objects

`ArrayList` is the resizable-array `List`: all optional operations, `null` allowed, unsynchronized, roughly `Vector` without locks. `get` / `set` / size queries are constant time; `add` is amortized constant [[What is an ArrayList]] [[What is the difference between ArrayList and Vector]].

`LinkedList` is a doubly-linked `List` and a `Deque` (hence `Queue`). It extends `AbstractSequentialList`, not the array skeletal type. Index `get` is a walk [[Is Java LinkedList a singly or doubly linked list]] [[Does LinkedList implement Queue and Deque in Java]] [[What design idea does LinkedList implement]].

`Vector` is a synchronized growable array, `RandomAccess`, retrofitted as a `List` in 1.2. Prefer `ArrayList` unless you need that legacy lock. `Stack` extends `Vector` with LIFO `push`/`pop`; the spec tells you to prefer `Deque` (e.g. `ArrayDeque`) [[How would you explain java.util.Vector and why it is legacy]].

`CopyOnWriteArrayList` (`java.util.concurrent`) is a thread-safe array `List`: mutators copy the array; iterators are snapshots and do not throw `ConcurrentModificationException` [[What is the difference between ArrayList Vector and CopyOnWriteArrayList]].

`AbstractList` is the random-access skeleton (`implements List`); its known subclasses include `AbstractSequentialList`, `ArrayList`, and `Vector`. Custom sequential lists should extend `AbstractSequentialList`. You cannot correctly implement both `List` and `Set` (`equals` contracts conflict) [[What is the List interface in Java]].

Factories still return `List`: `List.of` / `copyOf` (unmodifiable, no `null`, `RandomAccess`); `Arrays.asList` (fixed-size, array-backed, `RandomAccess`); `Collections.synchronizedList` / `unmodifiableList` (wrappers). Those runtime classes are not the interview names above.

```d2
direction: down
list: "List" {
  width: 80
  height: 40
}
abs: "AbstractList" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
seq: "AbstractSequentialList" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
al: "ArrayList" {
  width: 120
  height: 50
  style.fill: "#e3f2fd"
}
vec: "Vector" {
  width: 100
  height: 50
  style.fill: "#e3f2fd"
}
st: "Stack" {
  width: 80
  height: 40
  style.fill: "#bbdefb"
}
ll: "LinkedList" {
  width: 120
  height: 50
  style.fill: "#e8f5e9"
}
cow: "CopyOnWriteArrayList" {
  width: 200
  height: 50
  style.fill: "#f3e5f5"
}

list -> abs
list -> cow
abs -> seq -> ll
abs -> al
abs -> vec -> st
```

**Fig. 1.** Public Framework types. `CopyOnWriteArrayList` implements `List` without extending `AbstractList`.

```java
java.util.List<String> a = new java.util.ArrayList<>();
java.util.List<String> b = new java.util.LinkedList<>();
java.util.List<String> c = new java.util.Vector<>();
java.util.List<String> d = new java.util.concurrent.CopyOnWriteArrayList<>();
java.util.List<String> e = java.util.List.of("x");          // not ArrayList
java.util.List<String> f = java.util.Arrays.asList("y");    // fixed-size
```

**Listing 1.** Conceptual: several classes (and factories) satisfy `List`. `List.of` is not `new ArrayList`.

> [!warning] `List` is not `ArrayList`
> Default to `ArrayList` for a mutable random-access list, not because “List means array.” `LinkedList` is a `List` with `O(n)` `get`. `List.of` rejects `add`. `Stack` is a `List` you should not reach for on new code.

> [!warning] Synchronized ≠ the concurrent list
> `Vector` / `Collections.synchronizedList` lock the whole list. `CopyOnWriteArrayList` copies on write and is for read-heavy snapshots. Do not mix those stories. Other JDK modules can ship extra `List` types; interviews want the Framework names.

> [!tip] Interview answer
> **`ArrayList`, `LinkedList`, `Vector`/`Stack`, `CopyOnWriteArrayList`.** Plus `AbstractList` / `AbstractSequentialList` if they ask how to write your own. Mention `List.of` and `Arrays.asList` as `List` values that are not those classes. `LinkedList` is also a `Deque`. Prefer `ArrayList` or `ArrayDeque`, not `Vector`/`Stack`.
