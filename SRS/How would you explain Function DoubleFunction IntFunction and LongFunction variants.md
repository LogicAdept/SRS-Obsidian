<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain Function DoubleFunction IntFunction and LongFunction variants?

> [!abstract] Short answer
> **`Function<T,R>` is one value in, a result out:** SAM `R apply(T)`. `IntFunction<R>` / `LongFunction<R>` / `DoubleFunction<R>` are the **argument-primitive** specializations (`apply(int)` / `apply(long)` / `apply(double)` → `R`). They do **not** extend `Function` and have **no** `compose` / `andThen` / `identity`. `ToIntFunction` is the other direction (reference in, `int` out). Java 8. `Stream.map` takes `Function`; `IntStream.mapToObj` takes `IntFunction`.

## `apply(T)` versus `apply(int)`

`Function<T,R>` “represents a function that accepts one argument and produces a result.” The SAM is `apply`. Defaults: `compose(before)` runs `before` then this; `andThen(after)` runs this then `after`; static `identity()` returns the argument unchanged. A `null` `before` / `after` throws `NullPointerException`. `UnaryOperator<T>` is `Function<T,T>` ([[How would you explain UnaryOperator DoubleUnaryOperator IntUnaryOperator and LongUnaryOperator]], [[How would you explain core functional interfaces in java.util.function]]).

`IntFunction<R>` is “the `int`-consuming primitive specialization for `Function`”: SAM `R apply(int value)`. `LongFunction` / `DoubleFunction` match that for `long` / `double`. They list **no** superinterfaces and **no** default methods — only `apply`. You cannot assign an `IntFunction<String>` to `Function<Integer,String>`, and you cannot `andThen` on it.

```d2
direction: down
f: "Function<T,R>\nR apply(T)\ncompose / andThen / identity" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
arg: "Int / Long / DoubleFunction<R>\nR apply(int / long / double)" {
  width: 320
  height: 55
  style.fill: "#fff3e0"
}
ret: "ToInt / ToLong / ToDoubleFunction<T>\nint / long / double applyAs…" {
  width: 340
  height: 55
  style.fill: "#e3f2fd"
}
f -> arg: "specialize the argument"
f -> ret: "ToXxx specializes the return"
```

**Fig. 1.** `IntFunction` consumes a primitive. `ToIntFunction` produces one. Neither is a `Function` subtype. Stream `map` is the boxed `Function` ([[Which functional interface does Stream map use]], [[What is functional interface]]). Return-primitive types: [[How would you explain ToDoubleFunction ToIntFunction and ToLongFunction]].

Package naming: prefix `ToXxx` when the **result** is primitive (`ToIntFunction`). Otherwise specialize arguments left-to-right (`IntFunction`, `DoubleFunction`). Two-arg cousins are `BiFunction` / `ToIntBiFunction`, not these four.

Call sites: `Stream.map(Function)` yields `Stream<R>`. `Stream.mapToInt(ToIntFunction)` yields `IntStream`. `IntStream.mapToObj(IntFunction)` is the reverse bridge back to `Stream`. `IntStream.flatMap` also takes `IntFunction` (to an `IntStream`).

```java
import java.util.function.Function;
import java.util.function.IntFunction;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        Function<String, String> twice = s -> s + s;
        Function<String, Integer> len = String::length;
        Function<String, Integer> lenOfTwice = len.compose(twice);
        int n = lenOfTwice.apply("ab"); // 4
        Function<Integer, Integer> id = Function.identity();
        Stream.of("ab").map(len);
        // Function.identity().compose(null); // NPE
    }

    static void primitiveArg() {
        IntFunction<String> hex = Integer::toHexString;
        String s = hex.apply(255); // "ff"
        IntStream.of(10, 255).mapToObj(hex);
        // Function<Integer, String> no = hex; // does not compile
        // hex.andThen(String::toUpperCase);  // IntFunction has no andThen
    }
}
```

**Listing 1.** `compose` exists only on `Function`. `Integer::toHexString` is `int` → `String`, so it is an `IntFunction<String>` and a legal `mapToObj` mapper. Same shape for `LongFunction` / `DoubleFunction` with `apply(long)` / `apply(double)`.

> [!warning] `IntFunction` is not `Function<Integer,R>`
> No subtype, no `compose` / `andThen` / `identity`. Pipe a second function yourself, or stay on `Function<Integer,R>` and pay boxing. `Stream<Integer>.map` wants `Function`; `IntStream.mapToObj` wants `IntFunction`. Passing `i -> …` works in both only because target typing picks the SAM.

> [!warning] `IntFunction` versus `ToIntFunction`
> `IntFunction<R>`: primitive **in**, reference **out** (`apply(int)`). `ToIntFunction<T>`: reference **in**, primitive **out** (`applyAsInt(T)`). Mixing them is a compile-time error. `IntToDoubleFunction` is yet another type (primitive in and out), not `IntFunction<Double>`.

> [!tip] Interview answer
> **`Function<T,R>` is `R apply(T)` with `compose`, `andThen`, and `identity`.** `Int`/`Long`/`DoubleFunction<R>` take a primitive and return `R` via `apply(int)` and friends — they are not `Function` subtypes and have no combinators. `ToIntFunction` is the opposite specialization (object in, `int` out); `map` vs `mapToObj` vs `mapToInt` follow that split.
