<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #SRS

# What is a ThreadFactory for and why does thread naming matter?

> [!abstract] Short answer
> **A `ThreadFactory` is the injection point where threads get created — name, daemon flag, priority, uncaught handler, platform vs virtual — so a pool's threads are configured in one place instead of hardcoded inside the pool.** Naming is the headline use: in a thread dump, profiler, or log line, `pool-1-thread-3` is noise and `order-ingest-3` is a diagnosis.

## The factory contract, measured

The interface is one method: `Thread newThread(Runnable r)`. Every pool accepts one (`new ThreadPoolExecutor(..., factory)`, `Executors.newFixedThreadPool(n, factory)`), and the default factory names threads `pool-N-thread-M` with a process-wide counter — unique, and semantically empty. A custom factory replaces that:

```java
ThreadFactory named = new ThreadFactory() {
    private int n = 0;
    public Thread newThread(Runnable r) { return new Thread(r, "worker-" + (++n)); }
};
var pool = Executors.newFixedThreadPool(2, named);
pool.submit(() -> Thread.currentThread().getName());   // "worker-1"

var def = Executors.newFixedThreadPool(2);
def.submit(() -> Thread.currentThread().getName());   // "pool-1-thread-1"

Thread.ofVirtual().name("vt-worker-", 0).factory();   // virtual: "vt-worker-0"
```

**Listing 1.** Verified on JDK 21: a task inside the custom-factory pool ran on `worker-1`, the default pool produced `pool-1-thread-1`, and the virtual-thread factory named its thread `vt-worker-0`.

## Why the name pays for itself

Thread names are the only annotation that survives into every diagnostic channel at once: `jstack` and `jcmd Thread.print` dumps, profiler flame graphs, flight recordings, and every log line that prints the emitting thread. When a dump shows two hundred `pool-2-thread-N` stuck on a lock, the first question — *which pool, doing what* — is already answered if the factory set names like `order-ingest-2` and `email-fanout-1`. The same factory call is where the rest of thread hygiene lives: `setDaemon(true)` for helper pools that must not block JVM exit, `setUncaughtExceptionHandler` to funnel pool-thread crashes into logging instead of silence (a pool swallows task exceptions into futures, but a factory-level handler catches what leaks), and — since JDK 21 — swapping platform threads for virtual ones by passing `Thread.ofVirtual().factory()` without touching pool code ([[How would you explain Virtual Threads]] for when that trade makes sense).

## The discipline it enforces

The deeper value is architectural: thread creation becomes a policy, not a side effect. Pools no longer `new Thread(...)` ad hoc; code under test can inject a factory that runs tasks on the calling thread or names threads per test; and one audit point exists for the questions that decide behavior — how many pools use daemon threads, which have handlers, whether any thread escapes unnamed. Note the split of responsibility: the factory configures the *thread*, the executor configures the *work* ([[How would you explain ThreadPoolExecutor]] for the pool-side knobs) — the factory is never called again after pool construction for a fixed-size pool, but unbounded or eager pools (`newCachedThreadPool`, virtual executors) call it per new thread, so its cost should be trivial.

> [!warning] Two popular misreadings
> "The factory's setDaemon/priority guarantees scheduling" — no: priority is a weak hint the OS may ignore ([[Can thread priority reliably control execution order in Java]]), and daemon status decides JVM exit only, not importance. "Naming is cosmetic" — no: unnamed pools make incident triage guesswork; the name is the cheapest observability you will ever add, and after the first thread-dump fire drill nobody argues.

The pool that accepts it: [[How would you explain ThreadPoolExecutor]]; the pool whose threads you will actually need to name: [[Why Executors.newCachedThreadPool()]]; the modern factory target: [[How would you explain Virtual Threads]]; diagnostics that read the names: [[What is a heap dump and a thread dump]].

> [!tip] Interview answer
> `ThreadFactory` = one-method injection point for thread creation: name, daemon flag, priority, uncaught handler, and platform-vs-virtual choice, accepted by every executor. Default names are `pool-N-thread-M` — verified on JDK 21 that a custom factory yields `worker-1`, a virtual factory yields `vt-worker-0`. The name is the only annotation that reaches thread dumps, profilers, and logs simultaneously — name pools by function, set handlers for crash visibility, and treat the factory as the single audit point for thread policy across the codebase.
