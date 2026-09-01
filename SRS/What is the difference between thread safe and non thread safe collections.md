<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #SRS

# What is the difference between thread-safe and non-thread-safe collections?

> [!abstract] Short answer
> **A thread-safe collection allows concurrent method calls without extra locking on each call; a non-thread-safe one does not.** `HashMap`, `ArrayList`, and `HashSet` are not synchronized: if two threads share one and either mutates it, you must synchronize externally or wrap it. Thread-safe types (`ConcurrentHashMap`, `CopyOnWriteArrayList`, `Hashtable`, `Collections.synchronizedMap`) still have their own iterator and compound-action rules.

## “Not synchronized” versus safe concurrent calls

General-purpose implementations document that they are **not synchronized**. If multiple threads access a `HashMap` and at least one mutates it structurally, you must lock some encapsulating object, or wrap with `Collections.synchronizedMap`. The same rule is the default for `ArrayList`, `HashSet`, `ArrayDeque`, `PriorityQueue`, `LinkedHashMap`, `IdentityHashMap`. One thread, or a fully published immutable snapshot, does not need that. [[Is java.util.HashMap thread safe]] [[Is HashSet synchronized]] [[Is PriorityQueue thread-safe]] [[Is LinkedHashMap synchronized]]

Thread-safe collections are built so many threads may call them. Three styles:

- **Synchronized types** — `Hashtable`, `Vector`: one lock on the whole object for every method.
- **Synchronized wrappers** — `Collections.synchronizedList` / `Set` / `Map`: same one-lock idea around an unsynchronized backing collection. All access must go through the wrapper; iteration still needs `synchronized (wrapper)`.
- **Concurrent collections** — `ConcurrentHashMap`, `ConcurrentLinkedQueue`, `CopyOnWriteArrayList`, blocking queues: thread-safe **without** a single client-visible exclusion lock. Retrievals may overlap; iterators are weakly consistent or snapshot-style, not fail-fast.

[[How do you obtain synchronized wrappers for standard Java collections]] [[Why use concurrent collections instead of Collections synchronized wrappers]] [[How does Hashtable differ from ConcurrentHashMap]] [[What thread-safe collections exist in Java]]

Thread-safe does **not** mean a sequence of calls is one atomic action. `containsKey` then `put` is still a race on a wrapper (two lock acquires) and on a concurrent map (use `putIfAbsent` / `compute`). It also does not mean you ignore iterators: fail-fast views throw `ConcurrentModificationException` under concurrent structural change; a synchronized wrapper’s for-each is unsafe without locking the wrapper; concurrent iterators do not throw that exception and are not a freeze of the whole collection. [[What are CopyOnWriteArrayList thread safety tradeoffs]] [[How would you explain thread safety for shared mutable state]]

```java
Map<String, Integer> unsafe = new HashMap<>();           // not synchronized
Map<String, Integer> wrapped = Collections.synchronizedMap(new HashMap<>());
Map<String, Integer> concurrent = new ConcurrentHashMap<>();

unsafe.put("a", 1);                    // fine from one thread only
wrapped.put("a", 1);                   // one lock per call
concurrent.put("a", 1);                // concurrent map, no whole-table lock
```

**Listing 1.** Same `Map` calls; three safety stories.

```java
if (!wrapped.containsKey("a")) {
    wrapped.put("a", 1);               // still a race: two separate locked calls
}
concurrent.putIfAbsent("a", 1);        // one atomic map operation
```

**Listing 2.** Thread-safe methods are not an atomic compound action unless the type gives you one.

```d2
direction: right
Unsafe: HashMap {
  note: external lock or don't share
}
Safe: {
  sync: Hashtable / synchronizedMap
  conc: ConcurrentHashMap
}
Unsafe -> race: concurrent mutate
Safe.sync -> one lock
Safe.conc -> overlapping calls
```

**Fig. 1.** Non-thread-safe: do not share with a writer. Thread-safe: synchronized (one lock) or concurrent (no exclusive table lock).

> [!warning] Thread-safe is not “no rules”
> Sharing a `HashMap` across threads without a lock is a data race, not “eventually consistent.” A synchronized wrapper does not make a for-each loop safe by itself. `ConcurrentHashMap` does not make check-then-act safe without `putIfAbsent` / `compute`, and you cannot lock that map to freeze it. Prefer concurrent types under many threads; use a wrapper or a private lock when you truly need several calls to be exclusive.

> [!tip] Interview answer
> **Non-thread-safe collections like `HashMap` and `ArrayList` need external synchronization if more than one thread might mutate them.** Thread-safe collections allow concurrent calls: either one lock on the whole object, or a concurrent implementation with no exclusive table lock. That still does not make a multi-step update atomic, and iterators have separate rules. Under contention, reach for concurrent collections rather than a synchronized wrapper.
