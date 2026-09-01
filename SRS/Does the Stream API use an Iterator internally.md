<!--
reps: 0
priority: 0
-->
#Java/Streams #Java/Collections/Iteration #Java/Versions/8 #SRS

# Does the Stream API use an `Iterator` internally?

> [!abstract] Short answer
> **Not as the pipeline engine.** Java 8 streams are built from a **`Spliterator`**: `Collection.stream()` makes a sequential stream from `spliterator()`, and `StreamSupport.stream` takes a `Spliterator`, not an `Iterator`. An `Iterator` shows up as a **source adapter** (default `Collection.spliterator()` wraps the collection’s iterator) or as a **terminal escape hatch** (`BaseStream.iterator()`).

## Spliterator in, `Iterator` at the edges

The `Stream` class documentation says collections and streams look similar but streams do not offer direct element access. If the stream operations are not enough, **`BaseStream.iterator()`** and **`BaseStream.spliterator()`** exist for controlled traversal ([[What is the Java Stream API]], [[What is the difference between Collection and Stream in Java]], [[What internal abstractions power a Java stream pipeline]]). Both are **terminal** operations. The `spliterator()` javadoc calls that pair an “escape hatch.” After either call, the pipeline is consumed.

`StreamSupport.stream(spliterator, parallel)` is the low-level factory: the spliterator is traversed, split, or asked for size only after the terminal operation starts. There is no `StreamSupport` overload that takes an `Iterator`.

Where an `Iterator` still appears:

- **Into a stream:** default `Collection.spliterator()` builds a late-binding, `SIZED` (and `SUBSIZED`) spliterator **from the collection’s `Iterator`**, inheriting fail-fast. `list.stream()` uses `List.spliterator()` instead: `RandomAccess` lists walk with `get(int)`; others still wrap the list iterator ([[Does the Java Stream API optimize for lists that implement RandomAccess]]).
- **Out of a stream:** `stream.iterator()` returns an `Iterator` over remaining pipeline elements. `Spliterators.iterator(spliterator)` is the documented adapter the other way; after that, you must not keep operating the spliterator.

So “internally an `Iterator`” is true only for sources that never overrode `spliterator()`. Array-backed / `RandomAccess` lists and `StreamSupport` sources skip `Iterator` on the hot path.

```d2
direction: down
src: "Collection / array / generator" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
adapt: "default Collection.spliterator()\nwraps Iterator" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
spl: "Spliterator" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
pipe: "Stream pipeline\nStreamSupport.stream" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
out: "BaseStream.iterator()\nterminal escape hatch" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
src -> adapt
src -> spl
adapt -> spl
spl -> pipe
pipe -> out
```

**Fig. 1.** The pipeline talks to a `Spliterator`. `Iterator` is either how a default collection spliterator is built, or a terminal view of the stream.

```java
import java.util.Iterator;
import java.util.List;
import java.util.Spliterator;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

class Demo {
    static Stream<String> fromCollection(List<String> names) {
        return names.stream();
    }

    static Stream<String> fromSpliterator(Spliterator<String> s) {
        return StreamSupport.stream(s, false);
    }

    static Iterator<String> escape(Stream<String> stream) {
        return stream.iterator();
    }

    static void demo() {
        List<String> names = List.of("a", "b");
        fromCollection(names).count();
        fromSpliterator(names.spliterator()).count();
        escape(names.stream()).next();
    }
}
```

**Listing 1.** `fromCollection` still goes through `spliterator()`. `fromSpliterator` is the documented factory. `escape` is a terminal `Iterator`, not the engine.

> [!warning] `iterator()` on a stream is terminal
> `stream.iterator()` consumes the pipeline, same family as `forEach` or `collect`. A stream may be operated on only once; reuse **may** throw `IllegalStateException` if detected, but not every reuse is detectable. It is not an internal cursor you can peek at while `map` still runs. `BaseStream.spliterator()` is terminal too.

> [!warning] Default collection streams do sit on `Iterator`
> If you answer “never,” `HashSet.stream()` (and any type that keeps `Collection.spliterator()`) still walks the set iterator under the spliterator. Parallel splits on that default wrapper are weaker than a real `trySplit` on indexes or an array. Override `spliterator()` when the source can split ([[Does the Java Stream API optimize for lists that implement RandomAccess]]).

> [!tip] Interview answer
> **The Stream API is built on `Spliterator`, not `Iterator`.** `Collection.stream()` uses `spliterator()`; `StreamSupport` takes a spliterator. The default collection spliterator wraps `Iterator`, and `stream.iterator()` is a terminal escape hatch to pull elements out — that is the only sense in which an iterator is “internal.”
