<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# What are `map` and `mapToInt` for in Java streams?

> [!abstract] Short answer
> **One-to-one transform, still lazy.** `map(Function)` applies a function to each element and returns a `Stream` of the results (type may change). `mapToInt(ToIntFunction)` does the same into an `IntStream` so you can `sum()`, `average()`, `max()` without boxing. `mapToLong` / `mapToDouble` match. One input element → one output element. Zero-or-many needs `flatMap` / `flatMapToInt`.

## Apply a function, keep one result per element

`Stream.map(Function<? super T, ? extends R> mapper)` returns a stream consisting of the results of applying the given function to the elements of this stream. It is an **intermediate** operation: always lazy, mapper not run until a terminal starts. The mapper must be non-interfering and stateless ([[How would you explain intermediate operations on Java streams]], [[Which functional interface does Stream map use]]).

That is **one-to-one**. Length of the stream does not change; `filter` is what drops elements. If the function returns a collection or a stream, you still have `Stream<List<…>>` or `Stream<Stream<…>>` until you `flatMap` ([[What is the difference between Stream map and flatMap]], [[What are flatMap and flatMapToInt for in Java streams]]).

`mapToInt` is the primitive specialization: `ToIntFunction.applyAsInt` in, `IntStream` out. The package-summary widgets example is this shape: `.mapToInt(w -> w.getWeight()).sum()`. `IntStream` carries `sum`, `average`, `min`, `max` without wrapping each value in `Integer`. `map(Widget::getWeight)` would be `Stream<Integer>` and `sum()` would not exist on that stream — you would `reduce` or `collect(summingInt)` instead ([[How do you sum numbers in a stream]], [[How do you print unique squares of numbers using map]]). `Integer::parseInt` matches `ToIntFunction<String>`: `parseInt(String)` returns `int` and throws `NumberFormatException` if the string is not a signed decimal integer — that exception surfaces when the **terminal** runs, not when you build the pipeline. After `mapToInt`, `toArray()` is `int[]`.

`IntStream.map(IntUnaryOperator)` is **not** `Stream.mapToInt`: it maps `int` → `int` on a stream that is already primitive.

On an **ordered** source, the mapped *results* stay in encounter order even if, in parallel, the function runs on different threads at unpredictable times. Side effects in the mapper are not a substitute for `forEach` and may be **elided** (for example by `count()` on a sized source).

```d2
direction: right
in: "T" {
  width: 80
  height: 40
  style.fill: "#e3f2fd"
}
fn: "Function / ToIntFunction" {
  width: 220
  height: 50
  style.fill: "#fff8e1"
}
out: "R or int" {
  width: 120
  height: 40
  style.fill: "#e8f5e9"
}
in -> fn
fn -> out
```

**Fig. 1.** `map` / `mapToInt`: one element in, one mapped value out. `map` stays in object streams; `mapToInt` drops into `IntStream`.

```java
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static int totalWeight(List<Widget> widgets) {
        return widgets.stream()
            .mapToInt(Widget::weight)
            .sum();
    }

    static List<String> upper(List<String> words) {
        return words.stream()
            .map(String::toUpperCase)
            .toList();
    }

    static int[] parseInts(Stream<String> tokens) {
        return tokens.mapToInt(Integer::parseInt).toArray();
    }
}
```

**Listing 1.** `mapToInt` feeds primitive `sum`. `map` changes `String` → `String`. `parseInts` is `mapToInt` then `int[]` — `map(Integer::parseInt)` would be `Stream<Integer>` and could not `sum()` without another unbox. `toList()` is Java 16; `collect(Collectors.toList())` is the Java 8 form.

> [!warning] `map` does not flatten, and `map(Integer::parseInt)` is not `IntStream`
> `map(list -> list.stream())` yields `Stream<Stream<T>>`, not a flat `Stream<T>`. A stateful mapper (`seen.add(e)`) makes parallel results nondeterministic. Prefer `mapToInt` when the next step is a primitive reduction — `map` to `Integer` plus later unbox is extra allocation. `mapToInt` cannot drop an element; skip bad tokens with `filter` or `flatMapToInt` to an empty inner stream. `parseInt` on `null` / `""` throws at the terminal, not at pipeline build.

> [!tip] Interview answer
> **`map` is the lazy one-to-one transform (`Function` → `Stream<R>`).** **`mapToInt` is the same idea into `IntStream` (`ToIntFunction`),** which is what you want before `sum`/`average`. Many-valued expansion is `flatMap` / `flatMapToInt`, not `map`. `IntStream.map` is a different method on a stream that is already `int`s.
