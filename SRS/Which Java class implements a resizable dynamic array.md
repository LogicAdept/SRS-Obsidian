<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #SRS

# Which Java class implements a resizable dynamic array?

> [!abstract] Short answer
> **`java.util.ArrayList`**: “resizable-array implementation of the `List` interface.” Internally it is an `Object[]` plus `size()`. `Vector` is the older **synchronized** growable array. `ArrayDeque` is a resizable-array `Deque`, not a `List`.

## The `List` that grows an `Object[]`

```d2
direction: down
al: "ArrayList\nresizable-array List" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
buf: "elementData: Object[]\nsize <= length" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}

al -> buf
```

**Fig. 1.** Dynamic array = growable buffer, not a linked list ([[What design idea does ArrayList implement]], [[What backing data structure does ArrayList use internally]]).

`ArrayList` implements all optional list operations, permits `null`, and is **not synchronized**. `get`/`set` are constant time; end `add` is amortized constant time; growth policy is unspecified beyond that. It is “roughly equivalent to `Vector`, except that it is unsynchronized” ([[What is an ArrayList]], [[What is the difference between ArrayList and Vector]]).

`LinkedList` is a doubly-linked `List`/`Deque` — nodes, not a dynamic array. `Arrays.asList` is a **fixed-size** array view, not `java.util.ArrayList`.

```java
List<String> list = new ArrayList<>();
list.add("a");
list.add("b"); // may grow the backing array
```

**Listing 1.** The ordinary resizable-array `List`.

> [!warning] `Vector` is also a growable array
> Prefer `ArrayList` when you do not need method-level locks. `CopyOnWriteArrayList` copies the whole array on **every** write — a concurrent `List`, not the default dynamic array.

> [!warning] `new String[n]` is not resizable
> A Java array has a fixed `length`. `ArrayList` is the `List` that reallocates when `size` hits capacity ([[How does resize ArrayList]]).

> [!tip] Interview answer
> **`ArrayList` — a resizable-array `List` over an `Object[]`.** `Vector` is the synchronized 1.0 analogue. `LinkedList` is not an array; `ArrayDeque` is a resizable-array deque, not a `List`.
