<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain BinaryOperator DoubleBinaryOperator IntBinaryOperator and LongBinaryOperator?

> [!abstract] Short answer
> **`BinaryOperator<T>` is a same-type two-in, one-out operator:** it extends `BiFunction<T,T,T>` and its SAM is `apply(T, T)` → `T`. `IntBinaryOperator` / `LongBinaryOperator` / `DoubleBinaryOperator` are the **primitive** specializations (`applyAsInt` / `applyAsLong` / `applyAsDouble`). They do **not** extend `BinaryOperator`. Java 8. Streams take them as **associative** reducers (`reduce`, `Integer::sum`).

## Same three types, then primitives

`BinaryOperator<T>` “represents an operation upon two operands of the same type, producing a result of the same type as the operands.” It is the `BiFunction` case where both arguments and the result are `T`. You still call `apply` — there is no `applyAsT` on the boxed type. `andThen` is inherited from `BiFunction` and returns a `BiFunction`, not a `BinaryOperator` ([[How would you explain the BiFunction functional interface]], [[What is functional interface]]).

The only methods `BinaryOperator` adds are static factories: `minBy(comparator)` / `maxBy(comparator)` return the lesser / greater operand per that `Comparator`. A `null` comparator throws `NullPointerException` at the factory, before any `apply`.

```d2
direction: down
bi: "BiFunction<T,U,R>\napply(T, U) → R" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
bin: "BinaryOperator<T>\nextends BiFunction<T,T,T>" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
prim: "Int / Long / DoubleBinaryOperator\napplyAsInt / AsLong / AsDouble" {
  width: 320
  height: 55
  style.fill: "#fff3e0"
}
bi -> bin: "T = U = R"
bin -> prim: "docs: specialization\nnot a subtype"
```

**Fig. 1.** Boxed operator is a `BiFunction` subtype. Primitive operators are separate types with different SAM names. The unary cousins: [[How would you explain UnaryOperator DoubleUnaryOperator IntUnaryOperator and LongUnaryOperator]].

`IntBinaryOperator` is “the primitive type specialization of `BinaryOperator` for `int`”: two `int`s in, `int` out, SAM `applyAsInt(int left, int right)`. `LongBinaryOperator` / `DoubleBinaryOperator` match that shape for `long` / `double`. They list **no** superinterfaces: an `IntBinaryOperator` is not a `BinaryOperator<Integer>`. They have no `minBy` / `maxBy`. There is no `andThen` on them.

`Stream.reduce(identity, accumulator)` takes a `BinaryOperator`. The identity must satisfy `accumulator.apply(identity, t)` equals `t` for all `t`; the operator must be **associative**, non-interfering, and stateless. `reduce(accumulator)` without identity returns `Optional`. The three-arg form uses a `BiFunction` accumulator plus a `BinaryOperator` combiner. Documented sum: `integers.reduce(0, (a, b) -> a+b)` or `Integer::sum`. `IntStream.reduce(int, IntBinaryOperator)` is the same contract with `applyAsInt`.

```java
import java.util.Comparator;
import java.util.Optional;
import java.util.function.BinaryOperator;
import java.util.function.IntBinaryOperator;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        BinaryOperator<Integer> add = Integer::sum;
        int six = add.apply(1, 5);
        BinaryOperator<String> longer =
                BinaryOperator.maxBy(Comparator.comparingInt(String::length));
        String pick = longer.apply("aa", "bbb"); // "bbb"
        // BinaryOperator.minBy(null); // NPE now
    }

    static void primitiveAndReduce() {
        IntBinaryOperator add = Integer::sum;
        int six = add.applyAsInt(1, 5);
        // BinaryOperator<Integer> no = add; // does not compile

        Integer sum = Stream.of(1, 2, 3).reduce(0, Integer::sum);
        Optional<Integer> max = Stream.of(1, 2, 3).reduce(Integer::max);
        int ip = IntStream.of(1, 2, 3).reduce(0, Integer::sum);
    }
}
```

**Listing 1.** `Integer::sum` matches both `BinaryOperator<Integer>` (`apply`) and `IntBinaryOperator` (`applyAsInt`). `maxBy` picks by `Comparator`. `reduce(0, Integer::sum)` is the documented identity-plus-operator sum. Subtraction is a `BinaryOperator` but **not** a legal `reduce` accumulator (not associative).

> [!warning] Primitive operators are not `BinaryOperator` subtypes
> `IntBinaryOperator` cannot be assigned to `BinaryOperator<Integer>`. `Stream<Integer>.reduce` wants `BinaryOperator`; `IntStream.reduce` wants `IntBinaryOperator`. Boxing `BinaryOperator<Integer>` in a hot loop is a different type, with `Integer` operands, not `int`.

> [!warning] `reduce` needs an associative operator and a true identity
> The type system only checks `T apply(T, T)`. Parallel `reduce` may split the stream and combine partial results; a non-associative body (`(a, b) -> a - b`) can disagree with a sequential loop. `0` is the identity for sum, not for `Integer::min`. `minBy` / `maxBy` throw on a `null` `Comparator`; they do not define null-element order — that is the comparator’s job.

> [!tip] Interview answer
> **`BinaryOperator<T>` extends `BiFunction<T,T,T>` — same type in, same type in, same type out, SAM `apply`.** `Int`/`Long`/`DoubleBinaryOperator` are primitive specializations with `applyAsInt` and friends; they do not extend `BinaryOperator`. Use them as associative stream reducers; `minBy`/`maxBy` are the static helpers on the boxed type only.
