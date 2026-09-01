<!--
reps: 0
priority: 0
-->
#Java/Streams #Java/Versions/8 #SRS

# What internal abstractions power a Java stream pipeline?

> [!abstract] Short answer
> **Publicly: a `Spliterator` driving a lazy pipeline, usually built via `StreamSupport`.** A pipeline is source + intermediate stages + one terminal. At the lowest level every stream is a spliterator (advance, bulk traverse, `trySplit`). OpenJDK then chains package-private `Sink`s (one per stage, fused into a single pass) and, if parallel, `AbstractTask` fork-join work on the common pool. `Collector` is the public mutable-reduction protocol for `collect`. `Sink` is **not** an API you import.

## Spliterator at the bottom, stages above

The package’s own model: a **stream pipeline** is a source (`Collection`, array, generator, I/O), zero or more **intermediate** ops (`filter`, `map`, …), and one **terminal** (`forEach`, `reduce`, `collect`, …). Intermediates are always lazy; the source is not walked until the terminal runs. Laziness lets filter-map-reduce **fuse** into one pass ([[What is the Java Stream API]], [[When does a Java stream pipeline actually start executing]], [[What kinds of stream operations exist in Java]]).

How `Collection.stream()` / `parallelStream()` / `Arrays.stream` are implemented: **`StreamSupport`** factories, all taking a **`Spliterator`**. A spliterator is the parallel analogue of an `Iterator`: `tryAdvance` / `forEachRemaining`, plus `trySplit` for another worker. Traversal and splitting **exhaust** it — one bulk computation per spliterator. Characteristics (`SIZED`, `ORDERED`, `CONCURRENT`, `IMMUTABLE`, …) tell the engine what it may assume. Spliterators are **not** thread-safe; parallel code hands a split-off spliterator to another thread ([[Does the Stream API use an Iterator internally]], [[What backs Java parallelStream under the hood]]).

`Collector` is the public abstraction for `collect`: supplier / accumulator / combiner / finisher plus characteristics (`CONCURRENT`, `UNORDERED`, …) ([[What is the collect terminal operation in Java streams]]).

OpenJDK (package-private, Java 8): each stage is a **`Sink`** — a `Consumer` with `begin` / `accept` / `end` and optional `cancellationRequested` for short-circuit. Intermediate ops wrap a downstream sink (`Sink.ChainedReference` and primitive twins) so `filter` then `mapToInt` then `max` is one object chain, not three materialized lists. Parallel evaluation splits the source spliterator with **`AbstractTask`** (`CountedCompleter`) ([[What backs Java parallelStream under the hood]]).

```d2
direction: down
src: "source Spliterator" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
sinks: "Sink chain (OpenJDK)\nfilter → map → terminal" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
out: "result or side-effect" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
src -> sinks
sinks -> out
```

**Fig. 1.** Public engine is the spliterator; OpenJDK fuses stages as a `Sink` chain. Parallel adds fork-join splits of that spliterator.

```java
import java.util.List;
import java.util.OptionalInt;

class Demo {
    static OptionalInt longestA(List<String> strings) {
        return strings.stream()
            .filter(s -> s.startsWith("A"))
            .mapToInt(String::length)
            .max();
    }
}
```

**Listing 1.** Same pipeline OpenJDK uses to explain `Sink`: filter emits a subset, map emits `int`s, `max` reduces. You never construct a `Sink` yourself.

> [!warning] Do not code against `Sink` / `AbstractPipeline` — and this is not CI
> Those types are package-private JDK machinery. Your extension point is a `Spliterator` plus `StreamSupport.stream(...)`, or a `Collector`. A `Spliterator` must not be used by two threads at once. This question is **Java** `java.util.stream`, not GitHub/GitLab “pipeline” YAML.

> [!tip] Interview answer
> **The public internals are `Spliterator` + `StreamSupport` (and `Collector` for `collect`).** The pipeline object is lazy stages until a terminal. OpenJDK implements those stages as `Sink`s and parallel splits as fork-join tasks. Name `Spliterator.trySplit` if they ask how `parallelStream` actually divides work.
