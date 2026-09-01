<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #SRS

# What thread-safe collections exist in Java?

> [!abstract] Short answer
> **Concurrent types in `java.util.concurrent`, `Collections.synchronizedXxx` wrappers, and the legacy synchronized `Hashtable` / `Vector`.** Maps: `ConcurrentHashMap`, `ConcurrentSkipListMap`. Sets: `newKeySet()`, `ConcurrentSkipListSet`, `CopyOnWriteArraySet`. Lists: `CopyOnWriteArrayList`. Queues: concurrent-linked and `BlockingQueue` implementations. There is no `ConcurrentHashSet` class.

## Concurrent, wrapped, or legacy-synchronized

General-purpose `HashMap` / `ArrayList` / `HashSet` are not synchronized. Thread-safe replacements fall into three families. [[What is the difference between thread safe and non thread safe collections]] [[Why use concurrent collections instead of Collections synchronized wrappers]]

**Maps.** `ConcurrentHashMap` is the usual concurrent hash table. `ConcurrentSkipListMap` is the concurrent sorted map (prefer it to a synchronized `TreeMap` when many threads share it). `Hashtable` is the legacy whole-table lock. `Collections.synchronizedMap` / `synchronizedSortedMap` / `synchronizedNavigableMap` wrap an unsynchronized map. [[How does Hashtable differ from ConcurrentHashMap]]

**Sets.** There is no `ConcurrentHashSet`. Use `ConcurrentHashMap.newKeySet()`, `ConcurrentSkipListSet` for a concurrent sorted set, or `CopyOnWriteArraySet` for a small read-mostly set. Or wrap with `Collections.synchronizedSet`. [[How do you get a concurrent Set in Java]] [[What is ConcurrentSkipListSet]] [[What is CopyOnWriteArraySet]]

**Lists.** `CopyOnWriteArrayList` is the concurrent list (copy the array on write). `Vector` is the legacy synchronized list. `Collections.synchronizedList` wraps an `ArrayList`. [[What are Java CopyOnWrite collections]] [[How do you obtain synchronized wrappers for standard Java collections]]

**Queues and deques.** Non-blocking: `ConcurrentLinkedQueue`, `ConcurrentLinkedDeque`. Blocking: `ArrayBlockingQueue`, `LinkedBlockingQueue`, `LinkedBlockingDeque`, `PriorityBlockingQueue`, `DelayQueue`, `SynchronousQueue`, and `LinkedTransferQueue`. [[What is ConcurrentLinkedQueue]] [[How do you implement producer-consumer with a BlockingQueue]] [[What is the difference between ConcurrentLinkedQueue and a BlockingQueue]]

```java
Map<String, Integer> map = new ConcurrentHashMap<>();
Set<String> set = ConcurrentHashMap.newKeySet();
Set<String> sorted = new ConcurrentSkipListSet<>();
List<Runnable> listeners = new CopyOnWriteArrayList<>();
Queue<String> pipeline = new ConcurrentLinkedQueue<>();
BlockingQueue<String> buffer = new LinkedBlockingQueue<>();
Map<String, Integer> wrapped = Collections.synchronizedMap(new HashMap<>());
```

**Listing 1.** The types you actually name in an interview. Wrappers still count as thread-safe.

```d2
direction: down
Safe: thread-safe collections {
  conc: java.util.concurrent
  wrap: Collections.synchronizedXxx
  legacy: Hashtable / Vector
}
conc -> maps: ConcurrentHashMap / ConcurrentSkipListMap
conc -> sets: newKeySet / SkipListSet / COWAS
conc -> lists: CopyOnWriteArrayList
conc -> q: CLQ / BlockingQueue impls
```

**Fig. 1.** Three families. Concurrent types are the default under many threads; wrappers and `Hashtable` / `Vector` still lock the whole object.

> [!warning] `HashMap` is not on this list, and `ConcurrentHashSet` is not a class
> Sharing a `HashMap` or `ArrayList` across threads is not “a concurrent collection.” `Collections.synchronizedMap` is thread-safe and still one lock — including a manual lock around iteration. `newKeySet()` is the concurrent hash set; do not look for `new ConcurrentHashSet()`.

> [!tip] Interview answer
> **Name three families: `java.util.concurrent`, synchronized wrappers, and legacy `Hashtable` / `Vector`.** For a map use `ConcurrentHashMap`; for a set `newKeySet()` or `ConcurrentSkipListSet`; for a list `CopyOnWriteArrayList`; for hand-off a `BlockingQueue` or `ConcurrentLinkedQueue`. There is no `ConcurrentHashSet` class. Under contention prefer concurrent types over a synchronized wrapper.
