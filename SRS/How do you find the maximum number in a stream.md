<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Language/Optional #Java/Versions/8 #SRS

# How do you find the maximum number in a stream?

> [!abstract] Short answer
> **Use the terminal `max` reduction.** On an `IntStream` / `LongStream` / `DoubleStream`, `max()` returns `OptionalInt` / `OptionalLong` / `OptionalDouble` (`reduce(Integer::max)` and friends). On `Stream<Integer>`, pass a `Comparator`: `max(Integer::compareTo)`. Empty stream → empty optional; do not `get()` it.

## Reduction, not a loop

`max` is a special case of reduction and a **terminal** operation ([[What terminal stream operations do you know in Java]], [[How do you find the minimum number in a stream]], [[How do you sum numbers in a stream]]). For primitives, `IntStream.max()` is equivalent to `reduce(Integer::max)`: walk the values with associative `Integer.max`, or return empty `OptionalInt` if there was no element. `mapToInt` / `mapToLong` / `mapToDouble` gets you onto that path from boxed numbers.

`Stream.max(Comparator)` does the same for objects. `Integer::compareTo` (or `Comparator.naturalOrder()`) orders by numeric value. The result is `Optional<T>`. If the stream is empty, the optional is empty. If the **maximum element** is `null`, `max` throws `NullPointerException`.

Unwrap with `orElse` / `orElseThrow`, not `get` / `getAsInt` without a present-check ([[Why should you avoid calling get on an Optional]], [[What does orElseThrow do on Optional]], [[What are OptionalInt OptionalLong and OptionalDouble]]).

`DoubleStream.max()` is `reduce(Double::max)`. If **any** element is `NaN`, the maximum is `NaN`. Negative zero is strictly smaller than positive zero (unlike `>` / `<`).

```d2
direction: down
src: "numbers" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
prim: "IntStream.max()\nOptionalInt" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
box: "Stream<Integer>\nmax(Integer::compareTo)" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
empty: "empty stream\nempty optional" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
src -> prim
src -> box
prim -> empty
box -> empty
```

**Fig. 1.** Primitive `max()` vs boxed `max(Comparator)`. Both are empty-optional on an empty stream.

```java
import java.util.List;
import java.util.OptionalInt;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static OptionalInt maxInts(int[] values) {
        return IntStream.of(values).max();
    }

    static int maxOrThrow(List<Integer> values) {
        return values.stream()
            .mapToInt(Integer::intValue)
            .max()
            .orElseThrow();
    }

    static int maxBoxed(Stream<Integer> values) {
        return values.max(Integer::compareTo).orElseThrow();
    }

    static void demo() {
        maxInts(new int[] {3, 1, 4});          // OptionalInt[4]
        maxOrThrow(List.of(3, 1, 4));          // 4
        IntStream.empty().max().isPresent();   // false
    }
}
```

**Listing 1.** `maxInts` stays primitive. `maxOrThrow` boxes then `mapToInt`. `maxBoxed` needs a `Comparator`. Empty `IntStream` yields an empty `OptionalInt`.

> [!warning] Empty stream is not `0`, and `getAsInt` still throws
> `IntStream.empty().max()` is empty, not `OptionalInt.of(0)`. `getAsInt()` / `get()` on that empty box throws `NoSuchElementException`. `orElse(Integer.MIN_VALUE)` is a chosen default, not “the max of nothing.”

> [!warning] `null`, `NaN`, and signed zero
> A `null` in `Stream<Integer>` is not a number: `naturalOrder` / `compareTo` NPEs; `Stream.max` also NPEs if the maximum element is null. Filter nulls first. For `double`, any `NaN` makes `max` `NaN`, and `-0.0` loses to `+0.0`. `sorted().reduce((a, b) -> b)` still works but sorts the whole stream; `max` is the reduction meant for this.

> [!tip] Interview answer
> **`IntStream.max()` (or `mapToInt` then `max`) returns `OptionalInt`; boxed streams need `max(Integer::compareTo)`.** Empty means empty optional — use `orElseThrow`, not `get`. For doubles, remember `NaN` and that negative zero is smaller than positive zero.
