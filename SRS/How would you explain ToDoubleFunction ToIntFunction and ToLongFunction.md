<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain ToDoubleFunction ToIntFunction and ToLongFunction?

> [!abstract] Short answer
> **One object in, a primitive number out.** `ToIntFunction<T>` is `int applyAsInt(T)` — the **`int`-producing** primitive specialization of `Function`. `ToLongFunction` / `ToDoubleFunction` are `applyAsLong` / `applyAsDouble`. They do **not** extend `Function` and have **no** `compose` / `andThen` / `identity`. Java 8. `Stream.mapToInt` / `mapToLong` / `mapToDouble` take these types; `Stream.map` takes `Function`.

## `ToXxx` specializes the result

Package naming: prefix `ToXxx` when the **return** is primitive. That is the opposite of `IntFunction<R>`, which **consumes** an `int` and returns `R` ([[How would you explain core functional interfaces in java.util.function]], [[How would you explain Function DoubleFunction IntFunction and LongFunction variants]]).

`ToIntFunction<T>` “represents a function that produces an int-valued result.” SAM `applyAsInt(Object)` — in source, `int applyAsInt(T value)`. `ToLongFunction` / `ToDoubleFunction` match that with `long applyAsLong(T)` / `double applyAsDouble(T)`. Method summary is **only** that SAM.

They list **no** superinterface `Function`. You cannot assign a `ToIntFunction<String>` to `Function<String,Integer>`. `Function.andThen` / `compose` / `identity` do not exist here.

```d2
direction: down
f: "Function<T,R>\nR apply(T)\nandThen / compose / identity" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
to: "ToIntFunction<T>\nint applyAsInt(T)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
from: "IntFunction<R>\nR apply(int)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
f -> to: "ToXxx = primitive result\nnot a subtype"
f -> from: "IntXxx = primitive argument"
```

**Fig. 1.** `ToInt*` produces `int`; `Int*` consumes `int`. Two-arg primitive-result: [[How would you explain ToDoubleBiFunction ToIntBiFunction and ToLongBiFunction]]. Boxed `map`: [[Which functional interface does Stream map use]].

Call sites: `Stream.mapToInt(ToIntFunction)` yields `IntStream`; `mapToLong` / `mapToDouble` take `ToLongFunction` / `ToDoubleFunction`. `Stream.map(Function)` stays on `Stream<R>` and boxes if you return `Integer`. `IntStream.mapToObj(IntFunction)` is the reverse bridge.

| Type | In | Out | SAM |
| --- | --- | --- | --- |
| `Function<T,R>` | `T` | `R` | `apply` |
| `ToIntFunction<T>` | `T` | `int` | `applyAsInt` |
| `IntFunction<R>` | `int` | `R` | `apply(int)` |
| `ToIntBiFunction<T,U>` | `T`,`U` | `int` | `applyAsInt(T,U)` |

```java
import java.util.function.Function;
import java.util.function.IntFunction;
import java.util.function.ToIntFunction;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void objectInIntOut() {
        ToIntFunction<String> len = String::length;
        int n = len.applyAsInt("ab"); // 2
        IntStream ints = Stream.of("a", "bb").mapToInt(len);
        Function<String, Integer> boxed = String::length;
        IntFunction<String> hex = Integer::toHexString;
        Stream.of("a").mapToLong(s -> s.length());
        Stream.of("a").mapToDouble(s -> s.length());
        // Function<String, Integer> no = len; // does not compile
        // len.andThen(i -> i); // ToIntFunction has no andThen
    }
}
```

**Listing 1.** `String::length` is a `ToIntFunction<String>` for `mapToInt`. `mapToLong` / `mapToDouble` widen the `int` in the lambda body. `Integer::toHexString` is the opposite shape (`IntFunction`).

> [!warning] `ToIntFunction` is not `Function<T,Integer>`
> No subtype, no combinators. `Stream.map` wants `Function` and yields `Stream<Integer>` if you box. `mapToInt` wants `ToIntFunction` and yields `IntStream` with primitive `int`s. Target typing lets `String::length` fill either SAM; the **declared** type decides boxing.

> [!warning] `ToInt` versus `Int` versus `ToIntBi`
> `IntConsumer` / `IntPredicate` / `IntFunction` take an `int`. These types take an object and **return** a primitive. `ToIntBiFunction` takes **two** objects. `IntToDoubleFunction` is primitive-to-primitive, not `ToDoubleFunction<Integer>`.

> [!tip] Interview answer
> **`ToIntFunction<T>` is `int applyAsInt(T)` — object in, primitive `int` out, the `ToInt` form of `Function`.** `ToLong` / `ToDouble` are `applyAsLong` / `applyAsDouble`. They are not `Function` subtypes and have no `andThen`. Use them with `mapToInt` / `mapToLong` / `mapToDouble`; `IntFunction` is the opposite direction.
