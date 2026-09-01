<!--
reps: 0
priority: 0
-->
#Java/Streams/Parallel #Java/Parallelism #Java/Versions/8 #SRS

# What backs Java `parallelStream` under the hood?

> [!abstract] Short answer
> **A `Spliterator` plus fork-join tasks, not a hidden `Iterator` loop.** `Collection.parallelStream()` (Java 8) is specified to return a **possibly** parallel stream; the default implementation builds that stream from the collection’s `spliterator()`. At the lowest level every stream is driven by a `Spliterator` (`StreamSupport`). OpenJDK splits with `trySplit` on `CountedCompleter` tasks (`AbstractTask`) and runs them as `ForkJoinTask`s — by default on `ForkJoinPool.commonPool()`.

## Spliterator in, fork-join out

`Collection.parallelStream()` returns a possibly parallel `Stream` with the collection as source. It is **allowable** to return a sequential stream. The default implementation **creates a parallel `Stream` from the collection’s `Spliterator`**. `Collection.stream()` is the sequential twin from the same spliterator ([[How would you explain parallel streams in Java]], [[What is the difference between sequential and parallel streams in Java]]).

Package doc: `StreamSupport` is how `stream()` / `parallelStream()` / `Arrays.stream` are built. A `Spliterator` is the **parallel analogue of an `Iterator`**: advance, bulk traverse, and **split** a prefix for another worker. Poor splits (iterator wrapped with unknown size) parallelize badly. `List` that is `RandomAccess` typically splits by index; an iterator-backed list does not ([[Does the Stream API use an Iterator internally]], [[Does the Java Stream API optimize for lists that implement RandomAccess]], [[What internal abstractions power a Java stream pipeline]]).

When the terminal op runs in parallel mode, OpenJDK `AbstractTask` (a `CountedCompleter`) repeatedly `trySplit`s until chunks are small (`getCommonPoolParallelism() << 2` leaf target, unless the caller is already a `ForkJoinWorkerThread` — then that pool’s parallelism). Those tasks are `ForkJoinTask`s. `ForkJoinPool.commonPool()` is the pool for tasks **not** submitted to a named pool. The pool does **not** guarantee extra workers for blocked I/O. There is no `stream.forkJoin()` — “fork/join” is the JDK engine, not a user-facing Stream method.

`.parallel()` on an existing sequential stream is the same machinery: the **mode at the terminal** applies to the whole pipeline. Associative `reduce` / `collect` combine partial results; mutating a shared `ArrayList` in `forEach` is the anti-pattern.

```d2
direction: down
ps: "parallelStream()" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
sp: "Spliterator.trySplit" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
at: "AbstractTask\n(CountedCompleter)" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
fjp: "ForkJoinPool.commonPool()\n(unless already in a FJP worker)" {
  width: 320
  height: 60
  style.fill: "#fce4ec"
}
ps -> sp
sp -> at
at -> fjp
```

**Fig. 1.** Default `parallelStream`: spliterator splits, OpenJDK fork-join tasks, common pool.

```java
import java.util.List;

class Demo {
    static int sum(List<Integer> nums) {
        return nums.parallelStream().reduce(0, Integer::sum);
    }
}
```

**Listing 1.** Documented parallel reduction. The list’s `spliterator()` is what actually splits; `Integer::sum` is associative so partial sums combine.

> [!warning] “Parallel” is a request, and the common pool is shared
> `parallelStream()` may still be sequential. A source whose `trySplit` always fails runs as one chunk. Blocking I/O inside `map` can stall common-pool workers — `ForkJoinPool` does not promise compensation. Wrapping `parallelStream()` in `new ForkJoinPool().submit(...)` is **not** a specified API for a private pool. Ordered `limit`/`distinct` on parallel pipelines can buffer heavily.

> [!tip] Interview answer
> **Under `parallelStream` is a `Spliterator` (`StreamSupport`), not an `Iterator` engine.** OpenJDK turns splits into fork-join (`AbstractTask` / common pool). Quality of `trySplit` and associativity of the terminal decide whether you get speedup or just shared-pool contention. Name “not `Iterator`” if they ask what the engine is.
