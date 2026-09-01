<!--
reps: 0
priority: 0
-->
#Java/Streams/Parallel #Java/Parallelism #Java/Versions/8 #SRS

# What is the difference between sequential and parallel streams in Java?

> [!abstract] Short answer
> **Same pipeline, different execution mode.** JDK streams are **sequential unless you opt in** (`Collection.stream()` vs `parallelStream()`, or `.parallel()`). The **last** `sequential()` / `parallel()` before the **terminal** wins for the **whole** pipeline — not per op. Results should match except for explicitly nondeterministic ops (`findAny`, `forEach`). Parallel splits a `Spliterator` onto fork-join workers (`ForkJoinPool.commonPool()` by default). `parallelStream()` is only **possibly** parallel.

## Mode flag, not a second API

All stream operations can run serial or parallel. JDK factories create **serial** streams unless you opt in. `Collection.stream()` is sequential; `parallelStream()` is the parallel twin (the contract still **allows** a sequential stream). `IntStream.range` is sequential until `.parallel()`. `isParallel()`, `sequential()`, and `parallel()` query and change the mode; the **latest** setting is what the terminal uses. `isParallel()` answers whether a terminal **if run now** would be parallel ([[What is Stream]], [[When does a Java stream pipeline actually start executing]]).

Package doc: the serial vs parallel widgets example differs **only** in `stream()` vs `parallelStream()`. Execution mode is the mode of the stream **on which the terminal is invoked**. Encounter-order **results** (for example `map` then `toArray` on an ordered source) stay ordered; **when** the mapper runs, and **which thread**, is not ordered ([[What is the difference between forEach and forEachOrdered on a stream]]).

A `Spliterator` is the parallel analogue of an `Iterator`: advance, bulk traverse, and **split** a prefix for another worker ([[Does the Stream API use an Iterator internally]], [[Does the Java Stream API optimize for lists that implement RandomAccess]]). Reductions (`reduce`, `sum`, `collect`) combine partial results; the accumulator/combiner must be associative and stateless. Mutating a shared `ArrayList` in `forEach` is the anti-pattern the package doc replaces with `collect`.

OpenJDK `AbstractTask` (Java 8) is a `CountedCompleter` that splits the spliterator until chunks are small. Default leaf fan-out uses `ForkJoinPool.getCommonPoolParallelism() << 2`, unless the caller is already a `ForkJoinWorkerThread`, in which case it uses **that** pool’s parallelism. The common pool does **not** guarantee extra threads when tasks block on I/O. Cap size with `java.util.concurrent.ForkJoinPool.common.parallelism`. `unordered()` drops the ordered constraint for **later** ops; it does not skip a `sorted()` you already paid for. Poor splits (iterator-backed lists) and ordered `limit` / `distinct` can erase the speedup ([[What backs Java parallelStream under the hood]]).

```d2
direction: down
seq: "stream() / sequential()\none thread, encounter order easy" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
par: "parallelStream() / parallel()\nsplit Spliterator, common pool" {
  width: 320
  height: 55
  style.fill: "#fff8e1"
}
```

**Fig. 1.** Sequential vs parallel is a property of the stream at the terminal, not a different set of operators.

```java
import java.util.List;

class Demo {
    static int seq(List<Widget> widgets) {
        return widgets.stream()
            .filter(w -> w.color() == Color.RED)
            .mapToInt(Widget::weight)
            .sum();
    }

    static int par(List<Widget> widgets) {
        return widgets.parallelStream()
            .filter(w -> w.color() == Color.RED)
            .mapToInt(Widget::weight)
            .sum();
    }
}
```

**Listing 1.** Package-summary pair: identical pipeline; only the source mode changes. `sum` is associative, so both should agree. `IntStream.range(0, 5).parallel().map(x -> x * 2).toArray()` still yields `[0, 2, 4, 6, 8]` — encounter-order **result**, not encounter-order mapping.

> [!warning] You cannot parallelize “just the `map`”
> `parallel()` / `sequential()` change **pipeline mode**, not a single op. A dump that wires `peek` sequential, `map` parallel, `reduce` sequential still has **one** mode: whichever call is last. `parallelStream()` is allowed to return a sequential stream.

> [!warning] Shared mutable state in lambdas is a data race
> Parallel `map`/`forEach` may run on any worker thread, in any order. A `HashSet` or `ArrayList` updated from the lambda is broken without extra synchronization, and synchronizing kills the speedup. Use `reduce`/`collect`. Parallel `forEach` does not honor encounter order — use `forEachOrdered` if print order matters ([[What is the difference between forEach and forEachOrdered on a stream]]). Tiny lists and ordered `limit` often lose to sequential.

> [!warning] The common pool is a shared fork-join pool, not a dedicated I/O executor
> Parallel stream tasks are fork-join tasks; the common pool is what those tasks use unless they already run on another `ForkJoinWorkerThread`. Blocking I/O inside `map` can stall workers — `ForkJoinPool` does not promise to add threads for unmanaged blocking. Do not treat `new ForkJoinPool().submit(() -> list.parallelStream()…)` as a specified API for “private” parallel streams. Ordered `limit`/`distinct` on parallel pipelines can buffer heavily; `unordered()` or `sequential()` may be faster.

> [!tip] Interview answer
> **Sequential is the default; parallel is the same lazy pipeline with a parallel flag at the terminal.** Last `parallel()`/`sequential()` before the terminal wins for **all** ops. Results match except `findAny` / parallel `forEach`. Underneath: `Spliterator` + `ForkJoinPool.commonPool()`, not a magic faster loop. Lambdas must stay associative and free of shared mutation. Opt in only when the work is CPU-heavy, associative, and the source splits well.
