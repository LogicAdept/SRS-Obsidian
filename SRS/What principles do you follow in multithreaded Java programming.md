<!--
reps: 0
priority: 0
-->
#Java/Concurrency #OperatingSystems/Concurrency #SRS

# What principles do you follow in multithreaded Java programming?

> [!abstract] Short answer
> **Share less.** Mutable data that **is** shared needs a **happens-before** story (`synchronized` / `volatile` / atomics / j.u.c) so you **do not data-race**. Prefer **`ExecutorService`** over raw `Thread`, **j.u.c** over **`wait`/`notify`**, **immutable** objects where you can. **Interrupt is cooperative** — restore the flag or rethrow. **Name threads.** **Short** lock regions, **private** mutexes, **one lock-order**. **No** universal “add `synchronized`” fix. HB: [[How would you explain the happens-before guarantee in the Java Memory Model]]. Race vs data race: [[What is the difference between a race condition and a data race]]. No silver bullet: [[Is there a universal fix for race conditions in concurrent code]]. Interrupt: [[How would you explain InterruptedException in Java threads]]. Pools: [[What advantages does ExecutorService offer over creating raw threads]]. Deadlock: [[How do you avoid deadlock in Java]]. Immutable: [[How would you explain immutability and its benefits in Java]]. VTs: [[How would you explain Virtual Threads]].

## Memory, APIs, cancellation

**JMM:** conflicting unsynchronized accesses are a **data race**. Correctly synchronized programs **appear sequentially consistent**. Compound actions still need **one** atomic protocol (`putIfAbsent`, one lock).

**Tools:** `ExecutorService` + `Future.get`; **`ConcurrentHashMap`** for maps, not a **synchronized `HashMap`**. **`ThreadLocal.remove`** on **pooled** workers. **Do not pool virtual threads.**

**Locks:** hold **only** the fields they guard; **don’t** lock `this` if callers can too. **`try`/`finally`** on **`Lock.unlock`**. Same two locks → **same order** everywhere.

**Threads:** `start` not `run`. Catch **`InterruptedException`**, **don’t swallow**. `pool-N-thread-M` from the default factory; set names on custom workers.

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
try {
 Future<Integer> f = pool.submit(() -> work());
 return f.get();
} catch (InterruptedException e) {
 Thread.currentThread().interrupt();
 throw new RuntimeException(e);
} finally {
 pool.shutdown();
}
```

**Listing 1.** Pool, handle, restore interrupt, shut down. Not `new Thread` per call.

```d2
direction: down
share: "don't share / immutable" {
 width: 220
 height: 36
 style.fill: "#e8f5e9"
}
hb: "else happens-before" {
 width: 200
 height: 36
 style.fill: "#fff8e1"
}
api: "j.u.c / ExecutorService" {
 width: 220
 height: 36
 style.fill: "#e3f2fd"
}
share -> hb: "must share mutable"
hb -> api: "prefer library"
```

**Fig. 1.** Isolation first. Then a documented memory protocol. Then the concurrent library.

> [!warning] There is no one keyword that fixes races
> `volatile` is not `i++`. `ConcurrentHashMap` is not a **transaction**. `synchronized` on the wrong object is a **no-op** for the field you meant.

> [!warning] Do not invent a core-count formula
> Pool size is **workload** and **queue/reject** policy, not `N×(1+wait/compute)` from a book.

> [!tip] Interview answer
> I avoid sharing mutable state, and when I must share I pick a happens-before story instead of hoping. I use executors and java.util.concurrent instead of rolling wait and notify, and I treat interrupt as a real cancel. I keep locks short and ordered, and I do not pretend one synchronized will fix every race.
