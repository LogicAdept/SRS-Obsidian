<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/HashCodeEquals #SRS

# What is `java.util.HashMap` at a high level?

> [!abstract] Short answer
> **A `Map` that finds a value by hashing the key into a bucket, then matching with `equals`.** Order of entries is unspecified and may change. Expected `get` / `put` are constant-time if hashes spread; iteration walks **buckets plus entries**. Class contract: [[What is a HashMap]]. Bucket layout: [[What is the internal structure of HashMap]].

## The one-picture model

```text
key.hashCode()  →  pick a bucket
in that bucket  →  find the node whose key equals
miss            →  empty bucket, or no equal key in the chain
```

**Listing 1.** High-level `get` / `put`. `Map.containsKey` is specified as `equals` after implementations may skip `equals` when hashes already differ.

```d2
direction: down
k: "key" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
h: "hashCode\n→ bucket index" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
b: "that bucket\nempty / chain / (impl) tree" {
  width: 260
  height: 80
  style.fill: "#ffe0b2"
}
eq: "equals → value\nor no mapping" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
k -> h -> b -> eq
```

**Fig. 1.** Whiteboard `HashMap`. Not a sorted tree. Not an insertion-order list.

Colliding hashes share a bucket. The public javadoc still calls these **buckets** of a hash table. Java 8+ may treeify a long bin; that is implementation, not a `Map` contract change. Many identical `hashCode()` values slow the table. [[How does HashMap handle collisions]]

## What “high level” leaves out on purpose

No guaranteed encounter order — `LinkedHashMap` adds a list through all entries for that. No compare-based sort — `TreeMap` is a red-black `NavigableMap` with guaranteed log(n). No monitor on each call — not synchronized. One `null` key and `null` values are allowed. [[How do HashMap, TreeMap, and LinkedHashMap differ at a high level]]

Capacity and load factor only matter once you care about **when** the table grows and **why** iteration can be slower than `size()`. Defaults and resize: [[What are the initial capacity and load factor parameters of HashMap]].

> [!warning] “It’s a hash table, so O(1) always”
> The class javadoc’s constant-time claim is **assuming** the hash disperses keys among buckets. Worst case is a degenerate bin, not a language guarantee. [[Does HashMap guarantee its documented lookup time complexity]]

> [!tip] Interview answer
> **At a high level `HashMap` is hash-to-bucket, then `equals` in that bucket. Unspecified order, expected constant-time if hashes spread, iteration over capacity plus size. Reach for `LinkedHashMap` or `TreeMap` when order is the point.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Иерархия исключений в Java.**

Throwable → Error (системные, не ловим) и Exception. От Exception → checked и RuntimeException (unchecked).

**Способы создать поток в Java.**

extends Thread, implements Runnable, через Callable + ExecutorService, через CompletableFuture. На Java 21+ — Virtual Threads.

**Способы создать поток в Java.**

extends Thread, implements Runnable / Callable, ExecutorService, CompletableFuture, Virtual Thread (Java 21+).
