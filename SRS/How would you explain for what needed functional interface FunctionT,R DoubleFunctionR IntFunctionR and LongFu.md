<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface FunctionT,R DoubleFunctionR IntFunctionR and LongFu

> [!abstract] Short answer
> **They are Java 8 one-in, one-out transformers.** `Function<T,R>`’s SAM is `R apply(T)`. `IntFunction<R>` / `LongFunction<R>` / `DoubleFunction<R>` are the **primitive-argument** specializations (`apply(int)` / `apply(long)` / `apply(double)`), not `Integer` / `Long` / `Double`. `Stream.map` takes `Function`; primitive streams use `mapToObj` with the matching `*Function`.

## One argument in, a result out

`Function<T,R>` (`@since 1.8`) is a `@FunctionalInterface` for a function that accepts one argument and produces a result. The SAM is `apply`. `UnaryOperator<T>` is a known subinterface (`T` in and `T` out) ([[What is functional interface]], [[How would you explain Function DoubleFunction IntFunction and LongFunction variants]], [[Which functional interface does Stream map use]]).

Defaults chain two functions. `andThen(after)` applies **this first**, then `after`. `compose(before)` applies **`before` first**, then this. Either path relays a thrown exception. A `null` `before` / `after` throws `NullPointerException`. `identity()` returns a function that always returns its argument.

The dump chain is legal: `Integer::valueOf` is a `Function<String,Integer>`; `andThen(String::valueOf)` yields a `Function<String,String>`; `apply("123")` is `"123"`.

The primitive trio does **not** extend `Function` and has **no** `andThen` / `compose` / `identity`:

| Type | SAM | Argument | Result |
| --- | --- | --- | --- |
| `IntFunction<R>` | `apply(int)` | `int` | `R` |
| `LongFunction<R>` | `apply(long)` | `long` | `R` |
| `DoubleFunction<R>` | `apply(double)` | `double` | `R` |

Each is the primitive-consuming specialization of `Function`. The opposite direction — object in, primitive out — is `ToIntFunction` / `ToLongFunction` / `ToDoubleFunction`, not these types ([[How would you explain for what needed functional interface ToDoubleFunctionT ToIntFunctionT and ToLongFunction]], [[How would you explain primitive specialized functional types named like IntToLongFunction]]). `Stream.map` takes `Function`; `IntStream.mapToObj` takes `IntFunction`.

```d2
direction: down
f: "Function<T,R>\napply(T) → R" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
prim: "Int/Long/DoubleFunction<R>\napply(primitive) → R" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
use: "map / mapToObj" {
  width: 220
  height: 50
  style.fill: "#fff8e1"
}

f -> prim: "specialization, not a subtype"
f -> use
prim -> use
```

**Fig. 1.** Same “transform, return a value” shape. Primitive `*Function` avoids boxing the **argument**. `ToIntFunction` is the other axis (object in, `int` out).

```java
import java.util.function.Function;
import java.util.function.IntFunction;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        Function<String, Integer> toInteger = Integer::valueOf;
        Function<String, String> backToString = toInteger.andThen(String::valueOf);
        backToString.apply("123"); // "123"
        Stream.of("ab", "c").map(String::length);
    }

    static void primitive() {
        IntFunction<String> label = i -> "n=" + i;
        IntStream.of(1, 2).mapToObj(label);
    }
}
```

**Listing 1.** Dump `andThen` round-trip is `"123"`. `compose` would run the other function **first**. `IntFunction` has only `apply(int)` — chain on `Function`, not on the primitive types.

> [!warning] Primitive functions are not `Function<Integer,R>`
> Dump text that says `IntFunction` “takes `Integer`” is wrong: the SAM is `apply(int)`. You cannot pass an `IntFunction` where `Function<Integer,R>` is required. `ToIntFunction<T>` is the reverse (`T` in, `int` out) and is what `Stream.mapToInt` wants.

> [!warning] `andThen` is not `compose`
> `f.andThen(g)` is `g(f(x))`. `f.compose(g)` is `f(g(x))`. Both throw `NullPointerException` if the other function is `null`. `IntFunction` / `LongFunction` / `DoubleFunction` have neither default.

> [!tip] Interview answer
> **`Function<T,R>` is `R apply(T)` — one value in, a result out.** `IntFunction`, `LongFunction`, and `DoubleFunction` are the unboxed-argument twins. You need them for `map` / `mapToObj`. `andThen` / `compose` chain two `Function`s; `identity()` returns the argument unchanged.
