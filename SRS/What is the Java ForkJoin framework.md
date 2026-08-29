<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Parallelism #SRS

# What is the Java ForkJoin framework?

> [!abstract] Short answer
> **Fork/Join** (Java 7) is **`ForkJoinPool`** plus **`ForkJoinTask`**: split a job into **subtasks** (`fork`), then **wait for results** (`join`). You **do not** start a **`Thread` per subtask**. The pool is an **`ExecutorService`** that **work-steals**. Subclass **`RecursiveTask<V>`** (result) or **`RecursiveAction`** (void). Workers are **daemons**. Vs generic pools: [[How would you explain thread pools and executor frameworks in Java]]. `Future`: [[How would you explain the Future interface in java.util.concurrent]]. Common pool / CF: [[How would you explain CompletableFuture]]. Threads vs parallel: [[How does multithreading differ from parallelism and async work]]. Phaser: [[How would you explain java.util.concurrent.Phaser]].

## Steal work, don’t block the workers

Submit with **`invoke` / `submit` / `execute`**, or **`ForkJoinPool.commonPool()`** (also used by **parallel streams** and **`CompletableFuture.*Async`**). Inside a computation use **`fork()` / `join()` / `invokeAll`**. Join **innermost-first** (`b.fork(); a.fork(); a.join(); b.join()` is the slow pattern). Avoid **`synchronized`**, blocking I/O, and cyclic **`join`** (DAG only). Blocking needs **`ManagedBlocker`** or you stall the pool. **`asyncMode`** fits event-style tasks that are **never joined**.

```java
class Sum extends RecursiveTask<Long> {
    final int[] a; final int lo, hi;
    Sum(int[] a, int lo, int hi) { this.a = a; this.lo = lo; this.hi = hi; }
    protected Long compute() {
        if (hi - lo < 10_000) { /* sequential */ long s = 0; for (int i = lo; i < hi; i++) s += a[i]; return s; }
        int mid = (lo + hi) >>> 1;
        Sum left = new Sum(a, lo, mid);
        left.fork();
        return new Sum(a, mid, hi).compute() + left.join();
    }
}
long total = new Sum(data, 0, data.length).invoke();
```

**Listing 1.** Fork one half, compute the other, **join**. Trivial range is sequential.

```d2
direction: down
t: "task" {
  width: 80
  height: 32
  style.fill: "#fff8e1"
}
l: "fork left" {
  width: 100
  height: 32
  style.fill: "#e3f2fd"
}
r: "compute right" {
  width: 120
  height: 32
  style.fill: "#e8f5e9"
}
j: "join" {
  width: 80
  height: 32
  style.fill: "#f3e5f5"
}
t -> l
t -> r
l -> j
r -> j
```

**Fig. 1.** Recursive split. Idle workers **steal** queued subtasks.

> [!warning] Not a general thread pool for blocking I/O
> Fork/Join wants **CPU-ish, isolated** subtasks. Blocking `get` on the **common pool** can **starve** other FJ work (including some `CompletableFuture` tasks).

> [!warning] Join is still required to wait
> Parallel QuickSort still **joins** (or equivalent) so the caller knows the range is done. “No join phase” only fits **fire-and-forget** async tasks.

> [!tip] Interview answer
> Fork/Join is a work-stealing pool for recursively split tasks: fork subtasks, join results. I subclass RecursiveTask or RecursiveAction and keep compute small and non-blocking. The common pool is shared with parallel streams and CompletableFuture async methods.
