<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# What are `flatMap` and `flatMapToInt` for in Java streams?

> [!abstract] Short answer
> **One-to-many, then flatten.** `flatMap` maps each element to a **stream** of values and concatenates those streams into one. `flatMapToInt` does the same into an `IntStream` (`flatMapToLong` / `flatMapToDouble` for the other primitives). `map` stays one-to-one; `flatMap` is how nested collections, split lines, or `Optional.stream()` become a single pipeline. Lazy intermediate op. A `null` mapped stream is treated as empty.

## Replace each element with the contents of a stream

`Stream.flatMap(Function<? super T, ? extends Stream<? extends R>> mapper)` returns a stream of the results of replacing each element with the **contents** of the mapped stream. That is an **intermediate** operation (always lazy). The mapper must be non-interfering and stateless. Each mapped stream is **closed** after its contents are placed into the result. If the mapper returns `null`, an **empty** stream is used instead ([[How would you explain intermediate operations on Java streams]]). A `null` **element** still NPEs if the mapper dereferences it.

JavaDoc API note: `flatMap` is a **one-to-many** transformation, then flatten. Canonical cases:

- Nested collections: `orders.flatMap(order -> order.getLineItems().stream())`
- Split text: `lines.flatMap(line -> Stream.of(line.split(" +")))`
- Present `Optional`s: `opts.flatMap(Optional::stream)` ([[How does Optional.stream bridge to the Stream API]])

`map` would leave you with `Stream<Stream<R>>` or `Stream<List<R>>`. `flatMap` unwraps one level ([[What is the difference between Stream map and flatMap]], [[What are map and mapToInt for in Java streams]]).

`flatMapToInt` is the same contract with result type `IntStream`: the mapper produces an `IntStream` per element (for example `Arrays::stream` on `int[]`, or `s -> s.chars()`). `flatMapToLong` / `flatMapToDouble` match. Zero-or-many ints per element still flatten into one primitive stream — no boxing through `Stream<Integer>`. Mixing them (`flatMapToInt(s -> s.length())`) does not compile — that mapper returns `int`, which is `mapToInt`. `IntStream.flatMap` is the same flatten **on an `IntStream` already**, not `Stream.flatMapToInt`.

`mapMulti` (Java 16) is a related one-to-many that pushes into a `Consumer` instead of allocating a stream per element; JavaDoc prefers it when each element expands to a **small** number of values.

```d2
direction: down
el: "element" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
inner: "mapped Stream / IntStream\n(0..n values, then closed)" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
out: "flattened stream" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
el -> inner
inner -> out
```

**Fig. 1.** `flatMap` / `flatMapToInt` map to a stream, then concatenate contents.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static int sumCells(int[][] rows) {
        return Arrays.stream(rows)
            .flatMapToInt(Arrays::stream)
            .sum();
    }

    static String[] words() {
        return Stream.of("H e l l o", "w o r l d !")
            .flatMap(p -> Arrays.stream(p.split(" ")))
            .toArray(String[]::new);
    }

    static IntStream digits(List<String> groups) {
        return groups.stream()
            .flatMapToInt(s -> s.chars());
    }
}
```

**Listing 1.** Each `int[]` becomes an `IntStream` via `Arrays.stream`; `flatMapToInt` flattens to one `IntStream` before `sum`. `words` is the one-to-many flatten (split each string, concatenate). `map` instead of `flatMap` would be `Stream<Stream<String>>`. (`Stream.of(rows)` would be a one-element `Stream<int[][]>`.)

> [!warning] Mapped streams are consumed and closed — do not reuse them
> The mapper must return a **fresh** stream per element (or `null`/empty). Returning the same stream twice, or a stream already consumed, is reuse. A mapper that returns `Stream<int[]>` still needs `flatMapToInt` (or a further flatten) to reach primitive `int`s — `flatMap` alone would yield `Stream<int[]>`. `stream.map(list -> list.stream())` is `Stream<Stream<T>>`; you wanted `flatMap`.

> [!tip] Interview answer
> **`flatMap` is map-then-concat: each element yields a stream, the pipeline sees the inner elements.** `flatMapToInt` is that pattern into `IntStream`. Use `map` when the type stays one-to-one; use `flatMap*` when one input should become zero, one, or many outputs. `null` inners become empty streams, and each inner stream is closed after flattening.
