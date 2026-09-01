<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface To Function

> [!abstract] Short answer
> **They are Java 8 one-primitive-in, other-primitive-out transformers.** Six types cover every pair among `int` / `long` / `double`. The name is the contract: left token is the argument, `ToX` is the result. The SAM is `applyAsX`, never `apply`. They are primitive-to-primitive specializations of `Function`, not `Function<Integer,Long>` and not subtypes of `Function`.

## Left primitive in, `ToX` out

Each of these types (`@since 1.8`) is a `@FunctionalInterface` that accepts one primitive and produces a **different** primitive. They do **not** extend `Function`. There is no `andThen` / `compose`. The dump’s `Integer` / `Long` / `Double` wording is wrong on **both** sides ([[What is functional interface]], [[How would you explain primitive specialized functional types named like IntToLongFunction]], [[How would you explain for what needed functional interface FunctionT,R DoubleFunctionR IntFunctionR and LongFu]]).

| Type | SAM | In | Out |
| --- | --- | --- | --- |
| `IntToLongFunction` | `applyAsLong(int)` | `int` | `long` |
| `IntToDoubleFunction` | `applyAsDouble(int)` | `int` | `double` |
| `LongToIntFunction` | `applyAsInt(long)` | `long` | `int` |
| `LongToDoubleFunction` | `applyAsDouble(long)` | `long` | `double` |
| `DoubleToIntFunction` | `applyAsInt(double)` | `double` | `int` |
| `DoubleToLongFunction` | `applyAsLong(double)` | `double` | `long` |

Same primitive in and out is **not** this family (`IntUnaryOperator`, not `IntToIntFunction`). Object in, primitive out is `ToIntFunction` / `ToLongFunction` / `ToDoubleFunction`. Primitive in, object out is `IntFunction` / `LongFunction` / `DoubleFunction` ([[How would you explain for what needed functional interface ToDoubleFunctionT ToIntFunctionT and ToLongFunction]]).

`IntStream.mapToLong` takes `IntToLongFunction`; `mapToDouble` takes `IntToDoubleFunction`. Boxed `Stream.map` still wants `Function`.

```d2
direction: down
name: "IntToLongFunction" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
arg: "int in\n(left token)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
out: "long out\n(ToLong / applyAsLong)" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}

name -> arg
name -> out
```

**Fig. 1.** Read the type name left to right. `ToIntFunction<T>` is a different axis (object in, `int` out) — no `Int` on the left.

```java
import java.util.function.IntToLongFunction;
import java.util.function.LongToIntFunction;
import java.util.stream.IntStream;

class Demo {
    static void convert() {
        IntToLongFunction widen = i -> (long) i;
        LongToIntFunction narrow = l -> (int) l;
        widen.applyAsLong(3);  // 3L
        narrow.applyAsInt(3L); // 3
        IntStream.of(1, 2).mapToLong(widen);
    }
}
```

**Listing 1.** `applyAsLong` / `applyAsInt`, not `apply`. `mapToLong` wants `IntToLongFunction`. Narrowing `long` → `int` truncates; it does not throw.

> [!warning] Wrappers and `apply` are both wrong
> Dump text that says `IntToLongFunction` takes `Integer` and returns `Long` is wrong on both ends. There is no `apply(Integer)`. You cannot pass these types where `Function<Integer,Long>` is required. `ToLongFunction<T>` is object → `long`; `IntFunction<R>` is `int` → object.

> [!warning] Narrowing is silent
> `LongToIntFunction` / `DoubleToIntFunction` use a Java cast. Overflow and `double` truncation do not throw. Same-type maps (`IntStream.map`) use unary operators, not a `*To*Function`.

> [!tip] Interview answer
> **`IntToLongFunction` is `long applyAsLong(int)` — primitive in, other primitive out, no boxing.** Six types cover `int`/`long`/`double` pairs. Left name = argument, `ToX` = result and `applyAsX`. `ToIntFunction` and `IntFunction` are the mixed object/primitive cousins, not this set.
