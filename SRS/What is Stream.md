<!--
reps: 0
priority: 0
-->
#Java/Streams #Java/Versions/8 #SRS

# What is `Stream`?

> [!abstract] Short answer
> **`java.util.stream.Stream` (Java 8) is a lazy, one-shot sequence of elements for aggregate ops — not a collection and not `java.io`.** A pipeline is source + intermediate ops (always lazy, each returns a **new** stream) + one terminal that starts the walk and consumes the pipeline. Sequential by default; `parallel()` / `parallelStream()` opt in. `IntStream` / `LongStream` / `DoubleStream` are the primitive twins (`sum`, `average`, …). `Map` has no `stream()` — stream `keySet()`, `values()`, or `entrySet()`.

## A pipeline, not a bag of elements

`Stream` is “a sequence of elements supporting sequential and parallel aggregate operations.” It does **not** store elements. It conveys them from a source (collection, array, generator, I/O) through a pipeline ([[What is the Java Stream API]], [[What is the difference between Collection and Stream in Java]]).

Package split:

- **Intermediate** (`filter`, `map`, `sorted`, …) — return another `Stream`, **always lazy**. Calling them does not walk the source.
- **Terminal** (`forEach`, `collect`, `count`, `reduce`, …) — produce a value or a side-effect. Traversal starts here. Afterward the pipeline is **consumed**; operate on a stream only once (`IllegalStateException` if reuse is detected).

That is **not** the same object returned from every `filter`/`map`. You chain **new** streams. The Thread/`start()` analogy is course slang, not the spec: the accurate statement is “no source walk until the terminal” ([[When does a Java stream pipeline actually start executing]], [[What kinds of stream operations exist in Java]]).

Sources include `Collection.stream()`, `Arrays.stream`, `Stream.of`, `IntStream.range`, `Files.lines`, … ([[What ways exist to create a Java stream]]). **`Map` is not a `Collection`** and has no `stream()`. `HashMap` is fine as a source of **views**: `map.keySet().stream()`, `values()`, `entrySet()` — those views are collections ([[What is the difference between Collection and Stream in Java]]).

JDK factories create **sequential** streams unless you ask. Sequential vs parallel should not change the result except explicitly nondeterministic ops (`findAny`, `forEach`) ([[How would you explain parallel streams in Java]]).

Most pipelines do **not** need `close()`. `Stream` is `AutoCloseable`; I/O-backed streams (`Files.lines`) must be closed (try-with-resources). After a terminal, the pipeline is consumed even if `close()` was never called.

Primitive streams: `IntStream`, `LongStream`, `DoubleStream`. They take primitive functional interfaces (`IntPredicate`, `IntFunction`, …) and add reductions such as `sum()` and `average()`. **`mapToObj` is intermediate**, not a terminal.

```d2
direction: right
src: "source\nCollection / array / range" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
mid: "intermediate\n(new Stream, lazy)" {
  width: 200
  height: 60
  style.fill: "#fff8e1"
}
term: "terminal\n(consumes)" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
src -> mid
mid -> term
```

**Fig. 1.** A `Stream` is a pipeline: source, lazy intermediates, one terminal.

```java
import java.util.List;

class Demo {
    static int redWeight(List<Widget> widgets) {
        return widgets.stream()
            .filter(w -> w.color() == Color.RED)
            .mapToInt(Widget::weight)
            .sum();
    }
}
```

**Listing 1.** `Collection.stream()` → `filter` → `mapToInt` → `sum`. Package-summary shape. `HashMap` would use `entrySet().stream()`, not `map.stream()`.

> [!warning] Package name, reuse, and maps
> The type is `java.util.stream.Stream`, not `java.util.Stream`, and not `java.io.InputStream`. After a terminal, get a **new** stream from the source. Intermediates return a new stream, not “the same” instance. `mapToObj` does not finish the pipeline. Do not call `close()` on a collection-backed stream expecting a required ritual — do call it for `Files.lines`.

> [!tip] Interview answer
> **`Stream` is a lazy, consumable pipeline over a source (Java 8), not a second `List`.** Intermediates are lazy and return streams; one terminal runs it. Sequential by default. Primitives: `IntStream`/`LongStream`/`DoubleStream`. Maps: stream the views, there is no `Map.stream()`.
