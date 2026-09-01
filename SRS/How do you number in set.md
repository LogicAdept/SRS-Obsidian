<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Language/Optional #Career/Interview/Exercises #Java/Versions/8 #SRS

# How do you number in set

> [!abstract] Short answer
> **`mapToInt` then `max()` / `min()`.** Those terminals return `OptionalInt` (`reduce(Integer::max)` / `reduce(Integer::min)`). For `Stream.of(5, 3, 4, 55, 2)` the max is **55** and the min is **2**. Empty stream → empty optional; `getAsInt()` then throws `NoSuchElementException`. There is no `Stream.max()` without a `Comparator`.

## Primitive reduction, not a loop and not `sum`

A `Set<Integer>` starts with `set.stream()`. Literals use `Stream.of(...)`. Either way you have boxed `Integer`s. `mapToInt(ToIntFunction)` yields an `IntStream` so the primitive `max` / `min` terminals exist ([[What are map and mapToInt for in Java streams]], [[How do you find the maximum number in a stream]], [[How do you find the minimum number in a stream]]).

`IntStream.max()` is a terminal special-case reduction equivalent to `reduce(Integer::max)`. `min()` is `reduce(Integer::min)`. If the stream is empty, the result is an **empty** `OptionalInt` — not `0`. That is the opposite of `IntStream.sum()`, which is `reduce(0, Integer::sum)` and **is** `0` when empty ([[How do you sum numbers in a stream]], [[How do you get all numbers in set]]).

`getAsInt()` returns the value if present, otherwise **`NoSuchElementException`**. Prefer `orElse` / `orElseThrow(supplier)` / `ifPresent` ([[What are OptionalInt OptionalLong and OptionalDouble]], [[Why should you avoid calling get on an Optional]]).

`Stream<Integer>.max(Comparator)` / `min(Comparator)` is the boxed form (`Integer::compareTo`). A `null` minimum or maximum element throws `NullPointerException`.

```d2
direction: down
src: "Set.stream() or Stream.of(...)\nStream<Integer>" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
map: "mapToInt(Integer::intValue)\nIntStream" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
mx: "max() → OptionalInt\nempty = empty" {
  width: 240
  height: 55
  style.fill: "#c8e6c9"
}
mn: "min() → OptionalInt\nempty = empty" {
  width: 240
  height: 55
  style.fill: "#ffe0b2"
}

src -> map
map -> mx
map -> mn
```

**Fig. 1.** Same hop as sum/average. `max` / `min` never invent a number for an empty stream ([[What terminal stream operations do you know in Java]]).

```java
import java.util.NoSuchElementException;
import java.util.Set;
import java.util.stream.Stream;

class Demo {
    static int maxLiterals() {
        return Stream.of(5, 3, 4, 55, 2)
                .mapToInt(Integer::intValue)
                .max()
                .orElseThrow(NoSuchElementException::new);
    }

    static int minLiterals() {
        return Stream.of(5, 3, 4, 55, 2)
                .mapToInt(Integer::intValue)
                .min()
                .orElseThrow(NoSuchElementException::new);
    }

    static int maxSet(Set<Integer> numbers) {
        return numbers.stream()
                .mapToInt(Integer::intValue)
                .max()
                .orElseThrow(NoSuchElementException::new);
    }
}
```

**Listing 1.** `maxLiterals()` is `55`. `minLiterals()` is `2`. Java 8 `OptionalInt.orElseThrow` takes a supplier. A `Set` has already dropped duplicates before the reduction.

> [!warning] Empty `max` / `min` is not `0`, and `getAsInt` throws
> Empty `IntStream.max()` / `min()` is an empty `OptionalInt`. `getAsInt()` then throws `NoSuchElementException`. Empty `sum()` is `0`. Do not copy the sum empty-policy onto min/max.

> [!warning] `Stream.max()` needs a `Comparator`
> `Stream.of(5, 3, 4).max()` does not compile. Either `mapToInt(...).max()` or `max(Integer::compareTo)`. `mapToInt` still needs a mapper — there is no no-arg `mapToInt()`.

> [!tip] Interview answer
> **`set.stream().mapToInt(Integer::intValue).max()` and `.min()`, then unwrap the `OptionalInt`.** For `5, 3, 4, 55, 2` that is 55 and 2. Empty means empty optional, not zero — `getAsInt` throws. Literals use `Stream.of`. Boxed `Stream.max` needs a `Comparator`.
