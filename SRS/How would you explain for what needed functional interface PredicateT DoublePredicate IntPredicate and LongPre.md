<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface PredicateT DoublePredicate IntPredicate and LongPre

> [!abstract] Short answer
> **They are Java 8 one-in, `boolean`-out tests.** `Predicate<T>`’s SAM is `boolean test(T)`. `IntPredicate` / `LongPredicate` / `DoublePredicate` are the **primitive** specializations (`test(int)` / `test(long)` / `test(double)`), not `Integer` / `Long` / `Double`. `Stream.filter` takes `Predicate`; primitive streams take the matching `*Predicate`. `and` / `or` / `negate` compose conditions.

## Boolean test, then combinators

`Predicate<T>` (`@since 1.8`) is a `@FunctionalInterface` for a predicate — a boolean-valued function of one argument. The SAM is `test`. Defaults `and`, `or`, and `negate` build compound conditions. The dump is legal: `s -> s.length() > 0` yields `true` for `"foo"` and `false` after `negate()` ([[What is functional interface]], [[How would you explain Predicate DoublePredicate IntPredicate and LongPredicate]], [[Which functional interface represents a filter or predicate in the Stream API]]).

`and(other)` is short-circuit **AND**: if this is `false`, `other` is skipped. `or(other)` is short-circuit **OR**: if this is `true`, `other` is skipped. A throw from this skips `other`. A `null` `other` throws `NullPointerException`. `BiPredicate` is the two-argument cousin ([[How would you explain the BiPredicate functional interface]]).

The primitive trio does **not** extend `Predicate`:

| Type | SAM | Argument |
| --- | --- | --- |
| `IntPredicate` | `test(int)` | `int` |
| `LongPredicate` | `test(long)` | `long` |
| `DoublePredicate` | `test(double)` | `double` |

Each is the primitive-consuming specialization of `Predicate` and has the same `and` / `or` / `negate` shape (same-type `other`). `Stream.filter` takes `Predicate`; `IntStream.filter` takes `IntPredicate` ([[How do you count empty strings using filter]]).

```d2
direction: down
p: "Predicate<T>\ntest(T) → boolean" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
prim: "Int/Long/DoublePredicate\ntest(primitive) → boolean" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
use: "filter / anyMatch" {
  width: 220
  height: 50
  style.fill: "#fff8e1"
}

p -> prim: "specialization, not a subtype"
p -> use
prim -> use
```

**Fig. 1.** Same “ask a yes/no question” shape. Primitive predicates avoid boxing on `IntStream` / `LongStream` / `DoubleStream`.

```java
import java.util.function.IntPredicate;
import java.util.function.Predicate;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        Predicate<String> nonempty = s -> s.length() > 0;
        nonempty.test("foo");            // true
        nonempty.negate().test("foo");   // false
        Stream.of("", "x").filter(String::isEmpty);
    }

    static void primitive() {
        IntPredicate positive = n -> n > 0;
        IntStream.of(-1, 2, 3).filter(positive);
    }
}
```

**Listing 1.** Dump `test` / `negate` on `"foo"`. `and` / `or` short-circuit; `and(null)` throws. `IntPredicate` is not a `Predicate<Integer>`.

> [!warning] Primitive predicates are not `Predicate<Integer>`
> Dump text that says `IntPredicate` “takes `Integer`” is wrong: the SAM is `test(int)`. You cannot pass an `IntPredicate` where `Predicate<Integer>` is required. `filter` on an `IntStream` wants `IntPredicate`.

> [!warning] `and` / `or` short-circuit
> If the left predicate already decides the result, the right one never runs — and never throws. That is not `Consumer.andThen`, which always tries the first action and then the second. `negate` is a new predicate; it does not mutate this one.

> [!tip] Interview answer
> **`Predicate<T>` is `boolean test(T)` — one value in, true or false out.** `IntPredicate`, `LongPredicate`, and `DoublePredicate` are the unboxed twins. You need them for `filter` / `anyMatch` / `allMatch`. `and` / `or` / `negate` compose; `BiPredicate` is two arguments.
