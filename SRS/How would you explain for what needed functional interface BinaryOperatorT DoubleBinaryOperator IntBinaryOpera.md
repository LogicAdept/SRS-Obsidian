<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface BinaryOperatorT DoubleBinaryOperator IntBinaryOpera

> [!abstract] Short answer
> **They are Java 8 same-type two-in, one-out operators.** `BinaryOperator<T>` extends `BiFunction<T,T,T>`: `apply(T, T)` → `T`. `IntBinaryOperator` / `LongBinaryOperator` / `DoubleBinaryOperator` are the **primitive** specializations (`applyAsInt` / `applyAsLong` / `applyAsDouble`) — they take `int`/`long`/`double`, not `Integer`/`Long`/`Double`. Streams use them as associative reducers (`reduce`, `sum` as `reduce(0, Integer::sum)`).

## Same type both sides, then a result of that type

`BinaryOperator<T>` (`@since 1.8`) is a `@FunctionalInterface` for an operation on two operands of type `T` that produces a `T`. It is `BiFunction` specialized so both arguments and the result share one type. The SAM is inherited `apply`. `Integer::sum` and `(a, b) -> a + b` are typical bodies; `operator.apply(1, 2)` is `3` after boxing ([[How would you explain the BiFunction functional interface]], [[What is functional interface]], [[How would you explain for what needed functional interface UnaryOperatorT DoubleUnaryOperator IntUnaryOperator]]).

`minBy(comparator)` / `maxBy(comparator)` are static factories: they return a `BinaryOperator` that picks the lesser/greater operand. A `null` comparator throws `NullPointerException`.

The primitive trio does **not** extend `BinaryOperator`. Each is its own functional interface:

| Type | SAM | Operands / result |
| --- | --- | --- |
| `IntBinaryOperator` | `applyAsInt` | `int`, `int` → `int` |
| `LongBinaryOperator` | `applyAsLong` | `long`, `long` → `long` |
| `DoubleBinaryOperator` | `applyAsDouble` | `double`, `double` → `double` |

That is why `IntStream.reduce` takes `IntBinaryOperator`, while `Stream<Integer>.reduce` takes `BinaryOperator<Integer>` ([[How do you sum numbers in a stream]], [[How would you explain BinaryOperator DoubleBinaryOperator IntBinaryOperator and LongBinaryOperator]]).

```d2
direction: down
bi: "BiFunction<T,U,R>\napply(T, U) → R" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
bin: "BinaryOperator<T>\nT, T → T" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
prim: "Int/Long/DoubleBinaryOperator\napplyAsX primitives" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}

bi -> bin: "same type both sides"
bin -> prim: "specialization, not a subtype"
```

**Fig. 1.** `BinaryOperator` is a `BiFunction` shape. The primitive operators are siblings, not `BinaryOperator<Integer>` in disguise.

```java
import java.util.function.BinaryOperator;
import java.util.function.IntBinaryOperator;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static int boxed() {
        BinaryOperator<Integer> add = (a, b) -> a + b;
        return Stream.of(1, 2, 3).reduce(0, add);
    }

    static int primitive() {
        IntBinaryOperator add = Integer::sum;
        return IntStream.of(1, 2, 3).reduce(0, add);
    }
}
```

**Listing 1.** `boxed()` and `primitive()` are both `6`. The identity `0` must satisfy `add.apply(0, t) == t`. The accumulator must be associative for parallel `reduce`.

> [!warning] Primitive operators are not `BinaryOperator<Integer>`
> Dump text that says `IntBinaryOperator` “takes `Integer`” is wrong: the SAM is `int`. You cannot pass an `IntBinaryOperator` where `BinaryOperator<Integer>` is required. `apply` vs `applyAsInt` is the tell.

> [!warning] `reduce` needs identity and associativity, not any lambda
> `(a, b) -> a - b` is a legal `IntBinaryOperator` and a bad parallel reduction. `sum` / `Integer::max` / `Integer::min` match the documented `IntStream` reductions. `minBy` / `maxBy` still throw if the `Comparator` is `null`.

> [!tip] Interview answer
> **`BinaryOperator<T>` is `BiFunction<T,T,T>` — two values of one type in, one of the same type out, SAM `apply`.** `IntBinaryOperator`, `LongBinaryOperator`, and `DoubleBinaryOperator` are the unboxed twins (`applyAsInt` and friends). You need them for `reduce` / `sum` / `max` so the combiner is a typed operator, not a vague two-arg function.
