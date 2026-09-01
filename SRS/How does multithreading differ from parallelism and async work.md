<!--
reps: 0
priority: 0
-->
#Java/Concurrency #Java/Parallelism #Java/Async #SRS

# How does multithreading differ from parallelism and async work?

> [!abstract] Short answer
> **Multithreading** means more than one **thread of execution** (the JVM interleaves them; they may share **one** core). **Parallelism** means work actually proceeds on **several workers at once** (ForkJoin / parallel streams target **CPU-heavy** split tasks; default parallelism is `availableProcessors()`). **Async** means the **caller does not sit in `get`/`run` until the result exists**: `Executor` / `Future` / `CompletableFuture`. That work may run on a **new** thread, a **pool** thread, or even the **caller**. Concurrent vs async: [[What is the difference between being async and being concurrent]].

## Three different questions

A `Thread` is a thread of execution. Many threads are **concurrent**: their steps can overlap in time. That does not require two CPUs. Creating one: [[How do you create a thread in Java]].

**Parallel** libraries assume **compute** that splits. `ForkJoinPool` is an executor for `ForkJoinTask`s with a work-stealing scheduler “for computation-intensive **parallel** processing.” `Stream` pipelines are sequential or parallel (`Collection.parallelStream()`, `BaseStream.parallel()`). Parallel `forEach` may run on **whatever thread** the library chooses — you still synchronize shared state. Default FJP parallelism is **`Runtime.availableProcessors()`**. Mechanism: [[What backs Java parallelStream under the hood]], [[What is the difference between sequential and parallel streams in Java]].

**Asynchronous** APIs return a **`Future`** (“result of an asynchronous computation”) or a **`CompletionStage`**. `ExecutorService` is an “asynchronous task execution framework.” `Executor.execute` may use a new thread, a pooled thread, or **the thread that called `execute`**. `CompletableFuture` non-async dependents may run on the **completing** thread; `*Async` methods without an executor use **`ForkJoinPool.commonPool()`** (or a new `Thread` if common-pool parallelism is below two). Composition: [[How would you explain CompletableFuture for composing async work]].

You can have async on one thread (caller-runs, NIO callbacks), threads without parallelism (one core), and parallel work that is still synchronous for the caller (`parallelStream().sum()` waits).

```java
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executors;
import java.util.List;

public final class ThreeStyles {
    public static void main(String[] args) throws Exception {
        new Thread(() -> {}).start();

        int sum = List.of(1, 2, 3).parallelStream().mapToInt(i -> i).sum();

        var exec = Executors.newVirtualThreadPerTaskExecutor();
        Integer n = CompletableFuture.supplyAsync(() -> 1, exec).get();
        exec.close();
        System.out.println(sum + n);
    }
}
```

**Listing 1.** A thread, a parallel reduction (waits), an async supply (waits only at `get`). The three lines answer three different design questions.

```d2
direction: down
m: "multithreading\nseveral Thread objects" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
p: "parallelism\nsplit CPU work, FJP / parallelStream" {
  width: 320
  height: 55
  style.fill: "#e8f5e9"
}
a: "async\nFuture / CF, caller not blocked in the task" {
  width: 340
  height: 55
  style.fill: "#fff8e1"
}
```

**Fig. 1.** Overlap in tools (`commonPool` serves both parallel streams and CF `*Async`) does not make the words synonyms.

> [!warning] `parallelStream` is not “async”
> The calling thread typically **waits** for the pipeline. Extra threads are for **data parallelism**, not for returning a `Future`.

> [!warning] `supplyAsync` is not “I started a named Thread”
> Default async CF uses the **common pool**. Pinning a `Thread` object and `start()` is multithreading. Mixing them without a happens-before is still a race.

> [!tip] Interview answer
> Threads are concurrent units of execution; they might share one core. Parallelism is splitting CPU work across workers, usually ForkJoin or parallel streams. Async is a result you wait for later via a `Future` — it might not even run on another thread.
