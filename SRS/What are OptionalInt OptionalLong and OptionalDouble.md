<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Language/Primitives #SRS

# What are `OptionalInt`, `OptionalLong`, and `OptionalDouble`?

> [!abstract] Short answer
> **They are Java 8 containers for a possibly absent primitive `int`, `long`, or `double` — not `Optional<Integer>` / `Long` / `Double`.** Unwrap with `getAsInt` / `getAsLong` / `getAsDouble` (there is no `get()`). Primitive streams return them: `IntStream.max()` is `OptionalInt`; `IntStream.average()` is `OptionalDouble`.

## Primitive `Optional`, same “return type” job

Each is a value-based class since 1.8: “a container object which may or may not contain” an `int`, `long`, or `double`. Like `Optional`, they are meant as a **method return type**; the variable itself must not be `null` ([[What is Optional]]).

Factories are only `of(primitive)` and `empty()`. There is no `ofNullable`: a primitive argument cannot be `null`. `OptionalInt.of(0)` is **present** with value `0`. Empty means “no result,” not zero ([[What are Optional.ofNullable and Optional.empty]]).

Accessors match the primitive: `getAsInt()`, `getAsLong()`, `getAsDouble()`. Empty throws `NoSuchElementException`. The preferred alternative is `orElseThrow()` (Java 10 no-arg, same as on `Optional`). `orElse` / `orElseGet` supply a primitive default ([[Why should you avoid calling get on an Optional]], [[What does orElseThrow do on Optional]]).

The Java SE 17 API has no `map`, `flatMap`, or `filter` on these types. Pipeline transforms stay on `Optional<T>` or on the primitive stream before the terminal ([[How does Optional.map work]], [[When do you use Optional.flatMap instead of map]]). `stream()` (Java 9) is an `IntStream` / `LongStream` / `DoubleStream` of 0 or 1 elements (`flatMapToInt(OptionalInt::stream)` and the long/double twins).

`IntStream` terminals that can miss a value return these types: `max`, `min`, `findFirst`, `findAny`, and `reduce(IntBinaryOperator)` are `OptionalInt`; `average()` is `OptionalDouble` (empty stream → empty optional, not `NaN`).

```d2
direction: down
oi: "OptionalInt" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
as: "getAsInt / orElseThrow" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
nsee: "empty → NoSuchElementException" {
  width: 300
  height: 50
  style.fill: "#ffebee"
}
zero: "of(0) is present" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
max: "IntStream.max()\nOptionalInt" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
avg: "IntStream.average()\nOptionalDouble" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
oi -> as
oi -> nsee
oi -> zero
max -> oi
```

**Fig. 1.** `get()` does not exist. Zero is a value. `average()` is `OptionalDouble` even on an `IntStream`.

```java
import java.util.OptionalDouble;
import java.util.OptionalInt;
import java.util.stream.IntStream;

class Demo {
    static OptionalInt maxOf(int... xs) {
        return IntStream.of(xs).max();
    }

    static int maxOrZero(int... xs) {
        return IntStream.of(xs).max().orElse(0);
    }

    static double avgOrZero(int fromInclusive, int toInclusive) {
        return IntStream.rangeClosed(fromInclusive, toInclusive)
            .average()
            .orElse(0);
    }

    static OptionalInt zeroIsPresent() {
        return OptionalInt.of(0);
    }
}
```

**Listing 1.** `maxOf(3, 7, 2)` is present; `maxOf()` (empty varargs) is empty — `getAsInt()` would throw. `avgOrZero(1, 5)` uses `OptionalDouble.orElse`. `zeroIsPresent` is not empty.

> [!warning] There is no `get()`
> The compiler error is `getAsInt` / `getAsLong` / `getAsDouble`. On empty they still throw `NoSuchElementException`. Prefer `orElse` / `orElseThrow`. Do not copy `optional.get()` onto these types.

> [!warning] `0` and `NaN` are present values
> `OptionalInt.of(0)` is present. An empty `IntStream`’s `max()` is empty — not `0`. `OptionalDouble.of(Double.NaN)` is present; `IntStream.empty().average()` is empty. `OptionalDouble` equality uses `Double.compare(...) == 0`, so two present `NaN` boxes compare equal.

> [!tip] Interview answer
> **`OptionalInt`, `OptionalLong`, and `OptionalDouble` are primitive optionals: they hold `int`/`long`/`double` and are what `IntStream.max` and friends return.** Unwrap with `getAsInt` (not `get`) or `orElse`. There is no `ofNullable` and no `map`/`filter`; `of(0)` is present, empty means no result.
