<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS

# How would you explain the java.util.concurrent package?

> [!abstract] Short answer
> **`java.util.concurrent`** (since **1.5**) is the JDK’s **toolbox for concurrent programs**: **executors** (`Executor` / `ExecutorService` / pools / `Future` / `Callable`), **queues** (`BlockingQueue`, `ConcurrentLinkedQueue`), **synchronizers** (`Semaphore`, `CountDownLatch`, `CyclicBarrier`, `Phaser`, `Exchanger`), and **concurrent collections** (`ConcurrentHashMap`, `CopyOnWriteArrayList`, …). Sister packages: **`locks`** (`Lock`, `ReadWriteLock`) and **`atomic`**. These types **extend happens-before** (submit → run → `Future.get()`, `unlock`/`release`/`countDown` → matching acquire, putting into a concurrent collection → taking it out). Executors: [[How would you explain the ExecutorService interface in Java]]. Futures: [[How would you explain the Future interface in java.util.concurrent]]. Atomics: [[How would you explain Java atomic types in java.util.concurrent.atomic]]. Locks: [[How would you explain synchronization with synchronized and locks in Java]].

## Frameworks, not one class

**Executors.** `execute` may use a **new** thread, a **worker**, or the **caller**. `ExecutorService` adds **queueing/scheduling**, **`submit`**, and **shutdown**. `Executors` factories; `ThreadPoolExecutor` is the tunable pool; `ForkJoinPool` work-steals `ForkJoinTask`s — [[What is the Java ForkJoin framework]].

**Queues.** Non-blocking `ConcurrentLinkedQueue`; blocking `put`/`take` on `ArrayBlockingQueue`, `LinkedBlockingQueue`, `SynchronousQueue`, and others.

**Synchronizers.** Permit counts, latches, cyclic/phased barriers, two-thread swap — [[What is Semaphore]], [[How would you explain java.util.concurrent.Phaser]].

**Collections.** “**Concurrent**” means **thread-safe without one big lock** (many concurrent reads/writes on `ConcurrentHashMap`). Prefer that over `Collections.synchronizedMap` when many threads share a map. Iterators are **weakly consistent**: no `ConcurrentModificationException`, may miss later updates. **`TimeUnit`** timeouts are a **minimum** wait; `≤ 0` means **don’t wait**. JMM: [[How would you explain memory Java]].

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
try {
    Future<Integer> f = pool.submit(() -> 1);
    int n = f.get();
} finally {
    pool.shutdown();
}
```

**Listing 1.** The usual entry: factory → `ExecutorService` → `submit` → `Future`.

```d2
direction: down
pkg: "java.util.concurrent" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
ex: "Executors / Future" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
q: "Queues" {
  width: 120
  height: 36
  style.fill: "#fff8e1"
}
s: "Synchronizers" {
  width: 160
  height: 36
  style.fill: "#ffebee"
}
c: "Concurrent collections" {
  width: 220
  height: 36
  style.fill: "#f3e5f5"
}
pkg -> ex
pkg -> q
pkg -> s
pkg -> c
```

**Fig. 1.** One package, four main clusters, plus `locks` and `atomic`.

> [!warning] Concurrent is not `synchronized(map)`
> A concurrent map does **not** give you a single lock around **compound** `get`+`put`. Use `putIfAbsent` / `compute`, or one explicit lock, when the race is check-then-act.

> [!warning] Weakly consistent iterators
> They never throw `ConcurrentModificationException` and are **not** a snapshot of “now.” Do not treat `size()` under concurrent updates as a mutex.

> [!tip] Interview answer
> java.util.concurrent is the standard library for pools, futures, blocking queues, latches, and concurrent maps. I use Executors to run Callables, concurrent collections instead of a locked HashMap when many threads share data, and the synchronizers instead of wait/notify for those protocols. locks and atomic are the related packages for explicit locks and CAS counters.
