<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface UnaryOperatorT DoubleUnaryOperator IntUnaryOperator

> [!abstract] Short answer
> **They are Java 8 same-type-in, same-type-out transformers.** `UnaryOperator<T>` **extends** `Function<T,T>`; the SAM is still `apply`. `IntUnaryOperator` / `LongUnaryOperator` / `DoubleUnaryOperator` are the **primitive** specializations (`applyAsInt` / `applyAsLong` / `applyAsDouble`), not `Integer` / `Long` / `Double`. Same type on both ends — unlike `IntToLongFunction`. `IntStream.map` takes `IntUnaryOperator`.

## Same type in and out

`UnaryOperator<T>` (`@since 1.8`) is a `@FunctionalInterface` for an operation on one operand that produces a result of the **same** type. It extends `Function<T,T>` — this is a real subtype, so a `UnaryOperator<T>` is a `Function<T,T>`. The SAM is `Function.apply`. `identity()` returns an operator that always returns its argument. `andThen` / `compose` come from `Function` ([[What is functional interface]], [[How would you explain UnaryOperator DoubleUnaryOperator IntUnaryOperator and LongUnaryOperator]], [[How would you explain for what needed functional interface FunctionT,R DoubleFunctionR IntFunctionR and LongFu]]).

The dump is legal: `UnaryOperator<Integer> operator = x -> x * x` then `apply(5)` is `25` (boxed `Integer`).

The primitive trio does **not** extend `UnaryOperator`:

| Type | SAM | In / out |
| --- | --- | --- |
| `IntUnaryOperator` | `applyAsInt(int)` | `int` |
| `LongUnaryOperator` | `applyAsLong(long)` | `long` |
| `DoubleUnaryOperator` | `applyAsDouble(double)` | `double` |

Each is the primitive specialization of `UnaryOperator` and has its own `compose` / `andThen` (NPE if `before` / `after` is null) plus `identity()`. Different primitives in vs out is `IntToLongFunction`, not a unary operator ([[How would you explain for what needed functional interface To Function]]). Two same-type operands is `BinaryOperator` ([[How would you explain for what needed functional interface BinaryOperatorT DoubleBinaryOperator IntBinaryOpera]]). `IntStream.map` takes `IntUnaryOperator`; boxed `Stream.map` takes `Function` (a `UnaryOperator` is allowed because it **is** a `Function`).

```d2
direction: down
f: "Function<T,R>\nT in, R out" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
u: "UnaryOperator<T>\nextends Function<T,T>" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
prim: "Int/Long/DoubleUnaryOperator\napplyAsX(primitive) → same" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}

f -> u: "T equals R"
u -> prim: "specialization, not a subtype"
```

**Fig. 1.** Boxed `UnaryOperator` **is** a `Function`. Primitive unary operators are not `UnaryOperator<Integer>`.

```java
import java.util.function.IntUnaryOperator;
import java.util.function.UnaryOperator;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        UnaryOperator<Integer> square = x -> x * x;
        square.apply(5); // 25
        Stream.of(2, 3).map(square);
    }

    static void primitive() {
        IntUnaryOperator square = x -> x * x;
        square.applyAsInt(5); // 25
        IntStream.of(2, 3).map(square);
    }
}
```

**Listing 1.** Dump `apply(5)` is `25`. Primitive SAM is `applyAsInt`, not `apply`. `IntStream.map` wants `IntUnaryOperator`; `Stream.map` can take the boxed `UnaryOperator` because it extends `Function`.

> [!warning] Primitive unary operators are not `UnaryOperator<Integer>`
> Dump text that says `IntUnaryOperator` “takes `Integer`” is wrong: the SAM is `applyAsInt(int)`. You cannot pass an `IntUnaryOperator` where `UnaryOperator<Integer>` (or `Function<Integer,Integer>`) is required. There is no `IntToIntFunction` — same-primitive maps are this type.

> [!warning] `UnaryOperator` boxes; `IntUnaryOperator` does not
> `UnaryOperator<Integer>` with `x -> x * x` unboxes, multiplies, and reboxes on every call. Prefer `IntUnaryOperator` on `IntStream`. `identity()` returns the operand unchanged — it does not clone.

> [!tip] Interview answer
> **`UnaryOperator<T>` is `Function<T,T>` — `apply` with the same type in and out.** `IntUnaryOperator`, `LongUnaryOperator`, and `DoubleUnaryOperator` are the unboxed twins (`applyAsInt` / `applyAsLong` / `applyAsDouble`). You need them for same-type `map`. Two arguments is `BinaryOperator`; different primitives is `IntToLongFunction`.
