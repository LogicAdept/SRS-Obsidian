<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Versions/8 #SRS

# How do you sum numbers in a stream?

> [!abstract] Short answer
> **Primitive streams have `sum()`:** `IntStream.sum()` is `reduce(0, Integer::sum)` and returns `int` — **empty means `0`**, not an optional. There is no `Stream.sum()`. Boxeds go `mapToInt(Integer::intValue).sum()`, or `collect(Collectors.summingInt(...))`, which is also `0` if nothing was present.

## Reduction with identity zero

`sum()` is a **terminal** special-case reduction ([[How do you get the average of numbers in a stream]], [[How do you find the maximum number in a stream]], [[What terminal stream operations do you know in Java]]). `IntStream.sum()` is documented as `reduce(0, Integer::sum)`. Empty primitive `IntStream` → identity `0`, not an empty optional (unlike `max` / `min` / `average`). `DoubleStream.sum()` is the `double` analogue, with extra floating-point rules below.

`Stream<Integer>` has no `sum()`. Map to a primitive stream, or collect with `Collectors.summingInt` / `summingLong` / `summingDouble` ([[What is the collect terminal operation in Java streams]]). Those collectors return `Integer` / `Long` / `Double`, and **if no elements are present, the result is `0`**.

Boxed `reduce(0, Integer::sum)` is the same identity fold. `reduce(Integer::sum)` without identity returns `Optional<Integer>` and is empty when the stream is empty — that is a different empty policy than `sum()`.

`DoubleStream.sum()` is **not** guaranteed equivalent to `reduce(0, Double::sum)`: floating-point add is inexact, addition order is intentionally unspecified, and the implementation may use compensated summation. Any `NaN` → `NaN`. Intermediate overflows can produce infinities of opposite sign, then `NaN`, even when every element is finite. Sign of zero need not be preserved when every element is zero.

```d2
direction: down
src: "numbers" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
sum: "IntStream.sum()\nint, 0 if empty" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
col: "Collectors.summingInt\nInteger, 0 if empty" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
opt: "reduce(Integer::sum)\nOptional, empty if empty" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
src -> sum
src -> col
src -> opt
```

**Fig. 1.** `sum()` / `summingInt` use identity `0`. Optional `reduce` without identity does not.

```java
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

class Demo {
    static int sumInts(int[] values) {
        return IntStream.of(values).sum();
    }

    static int sumBoxed(List<Integer> values) {
        return values.stream()
            .mapToInt(Integer::intValue)
            .sum();
    }

    static Integer sumOrZero(List<Integer> values) {
        return values.stream()
            .collect(Collectors.summingInt(Integer::intValue));
    }

    static void demo() {
        sumInts(new int[] {1, 2, 3});  // 6
        IntStream.empty().sum();       // 0
        sumOrZero(List.of());          // 0
    }
}
```

**Listing 1.** Primitive `sum()`, boxed `mapToInt().sum()`, and `summingInt` all yield `0` on an empty source. That is not `average()`’s empty optional.

> [!warning] Empty `sum` is `0`; empty `average` / `max` is not
> `IntStream.empty().sum()` is `0`. `average()` on that stream is an empty `OptionalDouble`; `max()` / `min()` are empty optionals. Do not unwrap `sum()` with `orElseThrow`. `reduce(Integer::sum)` *without* identity is the optional form — mixing it up with `sum()` is a common interview swap.

> [!warning] `int` sum and `double` sum are not “just add”
> `IntStream.sum()` is `int` (`Integer::sum`). For totals that may not fit in `int`, `collect(Collectors.summingLong(...))` returns `Long` (still `0` if empty). `DoubleStream.sum()` may differ from a left-to-right `reduce(0, Double::sum)`: unspecified add order, possible compensated summation, `NaN`, and overflow to infinities. `summingDouble` documents the same `NaN` rule and rounding sensitivity.

> [!tip] Interview answer
> **`mapToInt` then `sum()`, or `IntStream.sum()` — that is `reduce(0, Integer::sum)`, so an empty stream is `0`.** Boxed streams can `collect(summingInt(...))`, also `0` if empty. `Stream` has no `sum()` method; optional `reduce` without identity is a different empty policy than `sum()`.
