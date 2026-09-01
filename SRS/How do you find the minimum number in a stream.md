<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Language/Optional #Java/Versions/8 #SRS

# How do you find the minimum number in a stream?

> [!abstract] Short answer
> **Use the terminal `min` reduction.** On an `IntStream` / `LongStream` / `DoubleStream`, `min()` returns `OptionalInt` / `OptionalLong` / `OptionalDouble` (`reduce(Integer::min)` and friends). On `Stream<Integer>`, pass a `Comparator`: `min(Integer::compareTo)`. Empty stream → empty optional; do not `get()` it.

## Reduction, not a loop

`min` is a special case of reduction and a **terminal** operation — the dual of `max` ([[How do you find the maximum number in a stream]], [[How do you sum numbers in a stream]], [[What terminal stream operations do you know in Java]]). For primitives, `IntStream.min()` is equivalent to `reduce(Integer::min)`: walk the values with associative `Integer.min`, or return empty `OptionalInt` if there was no element. `mapToInt` / `mapToLong` / `mapToDouble` gets you onto that path from boxed numbers.

`Stream.min(Comparator)` does the same for objects. `Integer::compareTo` (or `Comparator.naturalOrder()`) orders by numeric value. The result is `Optional<T>`. If the stream is empty, the optional is empty. If the **minimum element** is `null`, `min` throws `NullPointerException`.

Unwrap with `orElse` / `orElseThrow`, not `get` / `getAsInt` without a present-check ([[Why should you avoid calling get on an Optional]], [[What does orElseThrow do on Optional]], [[What are OptionalInt OptionalLong and OptionalDouble]]).

`DoubleStream.min()` is `reduce(Double::min)`. If **any** element is `NaN`, the minimum is `NaN`. Negative zero is strictly smaller than positive zero (unlike `<` / `>`).

```d2
direction: down
src: "numbers" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
prim: "IntStream.min()\nOptionalInt" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
box: "Stream<Integer>\nmin(Integer::compareTo)" {
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

**Fig. 1.** Primitive `min()` vs boxed `min(Comparator)`. Both are empty-optional on an empty stream.

```java
import java.util.List;
import java.util.OptionalInt;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static OptionalInt minInts(int[] values) {
        return IntStream.of(values).min();
    }

    static int minOrThrow(List<Integer> values) {
        return values.stream()
            .mapToInt(Integer::intValue)
            .min()
            .orElseThrow();
    }

    static int minBoxed(Stream<Integer> values) {
        return values.min(Integer::compareTo).orElseThrow();
    }

    static void demo() {
        minInts(new int[] {3, 1, 4});          // OptionalInt[1]
        minOrThrow(List.of(3, 1, 4));          // 1
        IntStream.empty().min().isPresent();   // false
    }
}
```

**Listing 1.** `minInts` stays primitive. `minOrThrow` boxes then `mapToInt`. `minBoxed` needs a `Comparator`. Empty `IntStream` yields an empty `OptionalInt`.

> [!warning] Empty stream is not `0`, and `getAsInt` still throws
> `IntStream.empty().min()` is empty, not `OptionalInt.of(0)`. `getAsInt()` / `get()` on that empty box throws `NoSuchElementException`. `orElse(Integer.MAX_VALUE)` is a chosen default, not “the min of nothing.”

> [!warning] `null`, `NaN`, and signed zero
> A `null` in `Stream<Integer>` is not a number: `naturalOrder` / `compareTo` NPEs; `Stream.min` also NPEs if the minimum element is null. Filter nulls first. For `double`, any `NaN` makes `min` `NaN`, and `-0.0` is smaller than `+0.0`. `sorted().findFirst()` still works but sorts the whole stream; `min` is the reduction meant for this.

> [!tip] Interview answer
> **`IntStream.min()` (or `mapToInt` then `min`) returns `OptionalInt`; boxed streams need `min(Integer::compareTo)`.** Empty means empty optional — use `orElseThrow`, not `get`. For doubles, remember `NaN` and that negative zero is smaller than positive zero.
