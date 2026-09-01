<!--
reps: 0
priority: 0
-->
#Java/Streams/Parallel #Java/Parallelism #Java/Versions/8 #SRS

# How would you explain parallel streams in Java?

> [!abstract] Short answer
> **Same pipeline, different execution mode.** JDK streams are sequential unless you ask: `Collection.parallelStream()` or `stream.parallel()`. The mode on the stream when the **terminal** op runs applies to the whole pipeline. Results should match sequential except for explicitly nondeterministic ops (`findAny`, `forEach`). Splitting is via `Spliterator`; OpenJDK drives that with fork-join tasks.

## Mode flag, then split-and-combine

All stream operations can run serial or parallel. JDK factories create **serial** streams unless you opt in (`Collection.stream()` vs `parallelStream()`, or `IntStream.range(...).parallel()`). `isParallel()`, `sequential()`, and `parallel()` query and change the mode; the **latest** setting is what the terminal op uses ([[What is the difference between sequential and parallel streams in Java]], [[When does a Java stream pipeline actually start executing]]).

`Collection.parallelStream()` is only a **possibly** parallel stream — the default implementation builds a parallel stream from the collection’s `Spliterator`, but the contract allows a sequential one.

A `Spliterator` is the parallel analogue of an `Iterator`: advance, bulk traverse, and **split** a prefix for another worker ([[Does the Stream API use an Iterator internally]], [[Does the Java Stream API optimize for lists that implement RandomAccess]]). Reductions (`reduce`, `sum`, `collect`) combine partial results; the accumulator/combiner must be associative and stateless. Mutating a shared `ArrayList` in `forEach` is the anti-pattern the package doc replaces with `collect`.

OpenJDK `AbstractTask` (Java 8) is a `CountedCompleter` that splits the spliterator until chunks are small. Default leaf fan-out uses `ForkJoinPool.getCommonPoolParallelism() << 2`, unless the caller is already a `ForkJoinWorkerThread`, in which case it uses **that** pool’s parallelism. `ForkJoinPool.commonPool()` is the pool for `ForkJoinTask`s not submitted to a named pool. The pool does **not** guarantee extra threads when tasks block on I/O ([[What backs Java parallelStream under the hood]]).

```d2
direction: down
src: "parallelStream() / parallel()" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
spl: "Spliterator.trySplit" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
fjp: "fork-join tasks\ncommon pool by default" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
src -> spl
spl -> fjp
```

**Fig. 1.** Parallel mode splits the source spliterator and runs chunks as fork-join tasks.

```java
import java.util.List;

class Demo {
    static int sumParallel(List<Integer> nums) {
        return nums.parallelStream().reduce(0, Integer::sum);
    }

    static int[] doubled(int n) {
        return java.util.stream.IntStream.range(0, n)
            .parallel()
            .map(x -> x * 2)
            .toArray();
    }
}
```

**Listing 1.** `parallelStream().reduce` is the documented parallel sum. `range(0,5).parallel().map(x -> x*2).toArray()` still yields `[0,2,4,6,8]` — encounter-order result, not encounter-order **mapping**.

> [!warning] Shared mutable state in lambdas is a data race
> Parallel `map`/`forEach` may run on any worker thread, in any order. A `HashSet` or `ArrayList` updated from the lambda is broken without extra synchronization, and synchronizing kills the speedup. Use `reduce`/`collect`. Parallel `forEach` does not honor encounter order — use `forEachOrdered` if print order matters ([[What is the difference between forEach and forEachOrdered on a stream]]).

> [!warning] The common pool is a shared fork-join pool, not a dedicated I/O executor
> Parallel stream tasks are fork-join tasks; the common pool is what those tasks use unless they already run on another `ForkJoinWorkerThread`. Blocking I/O inside `map` can stall workers — `ForkJoinPool` does not promise to add threads for unmanaged blocking. Do not treat `new ForkJoinPool().submit(() -> list.parallelStream()…)` as a specified API for “private” parallel streams. Ordered `limit`/`distinct` on parallel pipelines can buffer heavily; `unordered()` or `sequential()` may be faster.

> [!tip] Interview answer
> **A parallel stream is the same lazy pipeline with a parallel execution flag, usually from `parallelStream()` or `.parallel()`.** The library splits a `Spliterator` and combines partial results; lambdas must stay associative and free of shared mutation. OpenJDK runs that as fork-join work on the common pool by default — blocking I/O there contends with every other common-pool task.
