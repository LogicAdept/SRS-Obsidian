<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `Collections.synchronizedMap` / `synchronizedList` wrap a plain collection so **every method holds one lock** on the whole object. That is correct but **serializes all access** — readers block writers and each other — so it does not scale under contention.

`java.util.concurrent` collections use **finer-grained locking and lock-free** techniques (CAS, lock striping, copy-on-write) so many threads can proceed at once.

```java
Map<String, Integer> a = Collections.synchronizedMap(new HashMap<>()); // one lock
Map<String, Integer> b = new ConcurrentHashMap<>();                    // scalable
```

Dump: concurrent collections give **weakly consistent** iterators that **never throw** `ConcurrentModificationException`. Iterating a synchronized wrapper still needs **manual synchronize on the wrapper for the whole loop**. Rule of thumb in the dump: reach for `ConcurrentHashMap` / `CopyOnWriteArrayList` first; synchronized wrappers are **legacy**.

> [!warning] Unverified traps from the dump
> - “Never throw CME” is dump wording; other lists still say fail-safe / weakly consistent, not a lock.
> - Enhorse: even with `synchronizedList`, **iteration still needs a manual lock**.
