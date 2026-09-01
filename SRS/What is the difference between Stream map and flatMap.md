<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# What is the difference between Stream `map` and `flatMap`?

> [!abstract] Short answer
> **`map` is one-to-one (`T` → `R`). `flatMap` is one-to-many then flatten (`T` → `Stream<R>`, contents concatenated).** `map(list -> list.stream())` yields `Stream<Stream<T>>`. `flatMap(Collection::stream)` yields `Stream<T>`. Both are lazy intermediate ops. A `null` mapped stream is treated as empty; each mapped stream is closed after its contents are taken. `Optional.map` / `Optional.flatMap` are a **different** type — do not mix them up with `Stream`.

## One result vs the contents of a stream

`Stream.map(Function)` returns a stream of the results of applying the function to each element. Length stays the same; the type may change. That is **one-to-one** ([[What are map and mapToInt for in Java streams]]).

`Stream.flatMap(Function<? super T, ? extends Stream<? extends R>>)` **replaces each element with the contents** of a mapped stream, then concatenates. JavaDoc API note: one-to-many, then flatten. Canonical: `orders.flatMap(order -> order.getLineItems().stream())`. Nested lists: `lists.flatMap(Collection::stream)` ([[What are flatMap and flatMapToInt for in Java streams]]).

If the mapper returns `null`, `flatMap` uses an empty stream. Each mapped stream is **closed** after its contents are placed. Mapper must be non-interfering and stateless. Both stages are **always lazy** until a terminal ([[How would you explain intermediate operations on Java streams]]).

`mapToInt` vs `flatMapToInt`: same one-to-one vs flatten split into `IntStream`.

**Optional is not `Stream`:** `Optional.map` wraps the function’s result in an `Optional` (so a function that returns `Optional` yields `Optional<Optional<T>>`). `Optional.flatMap` unwraps one level. That is **`java.util.Optional`**, not this pair. On a `Stream<Optional<T>>`, the Stream-API flatten is `flatMap(Optional::stream)` (Java 9) ([[How does Optional.stream bridge to the Stream API]], [[When do you use Optional.flatMap instead of map]]).

```d2
direction: down
map: "map: T → R\nStream<R> same length" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
fm: "flatMap: T → Stream<R>\nconcat contents" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** `map` keeps one output per input. `flatMap` splices inner streams into one.

```java
import java.util.Collection;
import java.util.List;

class Demo {
    static List<String> flat(List<List<String>> nested) {
        return nested.stream()
            .flatMap(Collection::stream)
            .toList();
    }

    static List<List<String>> stillNested(List<List<String>> nested) {
        return nested.stream()
            .map(List::copyOf)
            .toList(); // still List<List<String>>
    }
}
```

**Listing 1.** `flatMap(Collection::stream)` is a `Stream<String>`. `map` of a list-producing function stays nested. `toList()` is Java 16.

> [!warning] `map` does not flatten, and mapped streams are one-shot
> Returning `Stream.of(a, b)` from `map` gives `Stream<Stream<…>>` until you `flatMap`. Reusing the same inner stream instance from `flatMap` is stream reuse. `flatMap` to `Stream<int[]>` is still not an `IntStream` — use `flatMapToInt(Arrays::stream)` for primitive arrays.

> [!tip] Interview answer
> **`map`: one in, one out. `flatMap`: one in, a stream out, concatenate.** Nested collections and `Optional.stream()` are the usual `flatMap` stories. If the interviewer says `Optional<Optional<T>>`, they mean **`Optional.flatMap`**, not `Stream.flatMap`.
