<!--
reps: 0
priority: 0
-->
#Java/Streams #Java/Versions/8 #SRS

# What is the Java Stream API?

> [!abstract] Short answer
> **`java.util.stream` (Java 8): functional-style aggregate pipelines over a sequence of elements — not `java.io`, not a second collection type.** The types are `Stream`, `IntStream`, `LongStream`, `DoubleStream`. A pipeline is source + lazy intermediate ops + one terminal. Streams do not store elements, do not modify the source, may be infinite, and are consumed after the terminal. Sequential by default; `parallelStream()` / `.parallel()` opt in.

## The `java.util.stream` package

Package summary: classes for functional-style operations on streams of elements, such as map-reduce on collections. The key abstraction is **stream**. `Stream` is object elements; `IntStream` / `LongStream` / `DoubleStream` are primitive specializations ([[What is Stream]]).

Streams **differ from collections**: no storage; functional (ops do not mutate the source); lazy intermediates; possibly unbounded; consumable (one visit, like an `Iterator` — get a new stream to revisit) ([[What is the difference between Collection and Stream in Java]]).

A **pipeline**: source (`Collection.stream()`, `Arrays.stream`, `Stream.of`, `IntStream.range`, `Files.lines`, `Random.ints()`, …) + zero or more intermediates (`filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, …) + one terminal (`forEach`, `reduce`, `collect`, `count`, `sum`, …) ([[What ways exist to create a Java stream]], [[What kinds of stream operations exist in Java]], [[What terminal stream operations do you know in Java]]). Intermediates are **always lazy**. Traversal starts at the terminal ([[When does a Java stream pipeline actually start executing]]). Laziness lets the implementation **fuse** filter-map-reduce into (usually) one pass with little intermediate storage, and skip leftover input after a short-circuit (`findFirst`, `limit`).

Behavioral parameters are functional-interface instances (`Predicate`, `Function`, `Consumer`, …): non-interfering, usually stateless ([[Which functional interface represents a filter or predicate in the Stream API]], [[Which functional interface does Stream map use]]). JDK streams are **serial** unless you request parallel; mode at the terminal applies to the whole pipeline ([[What is the difference between sequential and parallel streams in Java]]). `Collector` / `Collectors` implement mutable reduction for `collect` ([[What is the collect terminal operation in Java streams]]).

Most collection-backed streams need no `close()`. I/O-backed ones (`Files.lines`) are `AutoCloseable` and belong in try-with-resources.

```d2
direction: right
src: "source" {
  width: 100
  height: 40
  style.fill: "#e3f2fd"
}
api: "java.util.stream\nfilter / map / collect" {
  width: 240
  height: 55
  style.fill: "#fff8e1"
}
out: "value or side-effect" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
src -> api
api -> out
```

**Fig. 1.** The Stream API is the pipeline library: source in, aggregate result out.

```java
import java.util.Collection;

class Demo {
    static int redWeight(Collection<Widget> widgets) {
        return widgets.stream()
            .filter(w -> w.color() == Color.RED)
            .mapToInt(Widget::weight)
            .sum();
    }
}
```

**Listing 1.** Package-summary shape: `stream` → `filter` → `mapToInt` → `sum`. That *is* the Stream API: a query on a collection, not a new `List` of widgets.

> [!warning] Not `java.io`, not reusable storage, not `Map.stream()`
> `InputStream` is bytes. `java.util.stream.Stream` is a pipeline. After a terminal, open a **new** stream. Reuse (two terminals, or “forking” the same stream) is illegal; the implementation **may** throw `IllegalStateException` if it notices — some ops return the same object, so reuse is not always detectable. `Map` has no `stream()` — use `entrySet()` / `keySet()` / `values()`. Do not treat `forEach` + `ArrayList.add` as the API’s reduction; that is `collect`. `toList()` (Java 16) is an unmodifiable list.

> [!warning] Do not mutate the source during the terminal, and do not trust intermediate side effects
> Changing a non-concurrent collection while the pipeline runs can throw or yield nonsense. You **may** mutate a well-behaved JDK collection **before** the terminal starts; those additions are visible. `map`/`filter`/`peek` side effects can be **elided** (`count()` on a sized list may skip `peek`).

> [!tip] Interview answer
> **The Stream API is Java 8’s lazy map-filter-reduce library in `java.util.stream`.** Name `Stream` plus primitive streams, source → intermediates → terminal, and the five contrasts with collections (no storage, functional, lazy, unbounded, consumable). Sequential by default; parallel is a mode flag.
