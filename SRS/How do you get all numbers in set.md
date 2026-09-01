<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Language/Optional #Career/Interview/Exercises #Java/Versions/8 #SRS

# How do you get all numbers in set

> [!abstract] Short answer
> **You do not “get all numbers” with a special Set API — you reduce a stream of them.** From a `Set<Integer>` use `set.stream()`; from literals use `Stream.of(...)`. Then **`mapToInt` (a `ToIntFunction`) and a primitive terminal:** `sum()` → `int` (empty is `0`); `average()` → `OptionalDouble` (empty is empty). There is no `Stream.sum()` / `Stream.average()`.

## `mapToInt` is required; `mapToInt()` is not a method

`Stream.of(5, 3, 4, 55, 2)` is a sequential ordered `Stream<Integer>`, not a `Set`. A real set is `someSet.stream()` (collections are a documented stream source). Either way you still have boxed `Integer`s. `mapToInt(ToIntFunction)` is the intermediate that yields an `IntStream` so `sum` / `average` exist ([[What are map and mapToInt for in Java streams]], [[How do you sum numbers in a stream]]).

`mapToInt()` with no mapper does not compile. Use `a -> a`, `Integer::intValue`, or `i -> i`.

`IntStream.sum()` is a terminal reduction equivalent to `reduce(0, Integer::sum)`. For `5, 3, 4, 55, 2` that is **`69`**. Empty `IntStream` → **`0`**, not an optional. The fold is `int` arithmetic: large values wrap.

`IntStream.average()` is a terminal reduction that returns `OptionalDouble` — the arithmetic mean, or empty if the stream is empty. `69 / 5` is **`13.8`**. Unwrap with `orElse` / `orElseThrow`, not a blind `getAsDouble()` ([[How do you get the average of numbers in a stream]], [[What are OptionalInt OptionalLong and OptionalDouble]], [[Why should you avoid calling get on an Optional]]).

```d2
direction: down
src: "Set.stream() or Stream.of(...)\nStream<Integer>" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
map: "mapToInt(Integer::intValue)\nIntStream" {
  width: 280
  height: 60
  style.fill: "#fff8e1"
}
sum: "sum() → int\nempty = 0" {
  width: 200
  height: 55
  style.fill: "#c8e6c9"
}
avg: "average() → OptionalDouble\nempty = empty" {
  width: 260
  height: 55
  style.fill: "#ffe0b2"
}

src -> map
map -> sum
map -> avg
```

**Fig. 1.** Same `mapToInt` hop. `sum` always yields `int`. `average` yields a box that may be empty ([[What terminal stream operations do you know in Java]]).

```java
import java.util.NoSuchElementException;
import java.util.Set;
import java.util.stream.Stream;

class Demo {
    static int sumLiterals() {
        return Stream.of(5, 3, 4, 55, 2)
                .mapToInt(Integer::intValue)
                .sum();
    }

    static double averageLiterals() {
        return Stream.of(5, 3, 4, 55, 2)
                .mapToInt(Integer::intValue)
                .average()
                .orElseThrow(NoSuchElementException::new);
    }

    static int sumSet(Set<Integer> numbers) {
        return numbers.stream()
                .mapToInt(Integer::intValue)
                .sum();
    }
}
```

**Listing 1.** `sumLiterals()` is `69`. `averageLiterals()` is `13.8`. A `Set` starts with `stream()`, and uniqueness already happened in the set — duplicates never reach `sum`. Java 8 `OptionalDouble.orElseThrow` takes a supplier; `orElse(0.0)` if empty should be zero rather than a throw.

> [!warning] `mapToInt()` without a function does not compile
> The dump’s `.mapToInt().sum()` is not the API. `mapToInt` always takes a `ToIntFunction`. `Stream<Integer>` has no `sum()`.

> [!warning] Empty `average` is not `0`, and `getAsDouble` throws
> Empty `IntStream.average()` is an empty `OptionalDouble`. `getAsDouble()` then throws `NoSuchElementException`. Empty `sum()` is `0`. Those two empty policies are easy to mix. Prefer `orElse` / `orElseThrow` / `ifPresent`.

> [!tip] Interview answer
> **`set.stream().mapToInt(Integer::intValue).sum()` for the total; `.average()` for the mean.** `sum` is `int` and `0` if empty. `average` is `OptionalDouble` — do not `getAsDouble` on empty. Literals use `Stream.of(...)`. `mapToInt` needs a mapper; there is no no-arg `mapToInt()`.
