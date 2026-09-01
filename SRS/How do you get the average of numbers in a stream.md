<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Language/Optional #Java/Versions/8 #SRS

# How do you get the average of numbers in a stream?

> [!abstract] Short answer
> **Primitive streams have `average()`:** `IntStream` / `LongStream` / `DoubleStream` return `OptionalDouble` — empty if the stream is empty. There is no `Stream.average()`. Boxeds go `mapToInt` (or `mapToLong` / `mapToDouble`) then `average()`, or `collect(Collectors.averagingInt(...))`, which returns `0.0` when nothing was present.

## Arithmetic mean as a reduction

`average()` is a **terminal** special-case reduction ([[How do you sum numbers in a stream]], [[How do you find the maximum number in a stream]], [[What terminal stream operations do you know in Java]]). `IntStream.average()` describes the arithmetic mean as `OptionalDouble`, or empty if there were no elements. Same shape on `LongStream` and `DoubleStream`.

`Stream<Integer>` has no `average()`. Map to a primitive stream (`mapToInt(Integer::intValue)`) and call `average()`, or collect with `Collectors.averagingInt` / `averagingLong` / `averagingDouble` ([[What is the collect terminal operation in Java streams]]). Those collectors return `Double`. **If no elements are present, the result is `0`.**

`DoubleStream.average()` shares `sum()`’s special cases: the mean can vary numerically; if any element is `NaN` (or the running sum becomes `NaN`), the average is `NaN`. Values sorted by increasing absolute magnitude tend to be more accurate.

Unwrap `OptionalDouble` with `orElse` / `orElseThrow`, not `getAsDouble` on empty ([[Why should you avoid calling get on an Optional]], [[What are OptionalInt OptionalLong and OptionalDouble]]).

```d2
direction: down
src: "numbers" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
avg: "IntStream.average()\nOptionalDouble" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
col: "Collectors.averagingInt\nDouble, 0 if empty" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
empty: "empty IntStream\nempty optional" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
src -> avg
src -> col
avg -> empty
```

**Fig. 1.** `average()` is optional-on-empty. `averagingInt` is `0.0`-on-empty. Those are not the same empty policy.

```java
import java.util.List;
import java.util.OptionalDouble;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

class Demo {
    static OptionalDouble meanInts(int[] values) {
        return IntStream.of(values).average();
    }

    static double meanOrThrow(List<Integer> values) {
        return values.stream()
            .mapToInt(Integer::intValue)
            .average()
            .orElseThrow();
    }

    static Double meanOrZero(List<Integer> values) {
        return values.stream()
            .collect(Collectors.averagingInt(Integer::intValue));
    }

    static void demo() {
        meanInts(new int[] {2, 4, 6});     // OptionalDouble[4.0]
        meanOrThrow(List.of(2, 4, 6));     // 4.0
        IntStream.empty().average();       // empty
        meanOrZero(List.of());             // 0.0
    }
}
```

**Listing 1.** Primitive `average()` vs `averagingInt`. Empty `IntStream` is an empty optional; empty `averagingInt` is `0.0`.

> [!warning] Empty average is not `0.0` on `IntStream`
> `IntStream.empty().average()` is empty `OptionalDouble`, not `0`. `getAsDouble()` throws `NoSuchElementException`. `Collectors.averagingInt` **does** return `0` with no elements — that collector is the one whose empty policy is zero. Do not mix the two in an interview answer.

> [!warning] Integer division is not `average()`
> `(a + b) / 2` in `int` truncates. `average()` is a `double` mean. For `double` streams, any `NaN` makes the average `NaN`, same family as `sum()`. `summaryStatistics()` is a related reduction that describes various summary data about the elements when you need more than the mean.

> [!tip] Interview answer
> **`mapToInt` then `average()` gives `OptionalDouble`; empty stream means empty optional, not zero.** Boxed streams can `collect(averagingInt(...))` instead, and that returns `0.0` when there are no elements. `Stream` itself has no `average()` method.
