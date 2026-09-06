<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain Predicate DoublePredicate IntPredicate and LongPredicate?

> [!abstract] Short answer
> **A predicate is a boolean-valued function of one argument.** `Predicate<T>`’s SAM is `boolean test(T)`. `IntPredicate` / `LongPredicate` / `DoublePredicate` are the **primitive** specializations (`test(int)` / `test(long)` / `test(double)`). They do **not** extend `Predicate`. All four have short-circuit `and` / `or` and `negate`. Only the boxed type adds `isEqual` and `Predicate.not` (Java 11). `Stream.filter` takes `Predicate`; `IntStream.filter` takes `IntPredicate`.

## `test`, then compose

`Predicate<T>` “represents a predicate (boolean-valued function) of one argument.” `test` returns `true` if the argument matches. Defaults: `and` / `or` are **short-circuit** (skip the other side on `false` / `true`; if this side throws, the other is not evaluated; `NullPointerException` if `other` is null). `negate` flips the result. Static `isEqual(targetRef)` uses `Objects.equals` (`targetRef` may be `null`). Static `Predicate.not` (**since 11**) is `target.negate()` and NPEs if `target` is null ([[What is functional interface]], [[How would you explain core functional interfaces in java.util.function]]).

`IntPredicate` is “the `int`-consuming primitive type specialization of `Predicate`”: SAM `test(int)`, plus `and` / `or` / `negate` returning `IntPredicate`. `LongPredicate` / `DoublePredicate` match that for `long` / `double`. They list **no** superinterface `Predicate`, and they have **no** `isEqual` / `not`.

```d2
direction: down
p: "Predicate<T>\nboolean test(T)\nand / or / negate / isEqual / not" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
prim: "Int / Long / DoublePredicate\ntest(int / long / double)\nand / or / negate only" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
use: "filter / anyMatch / allMatch / noneMatch" {
  width: 300
  height: 45
  style.fill: "#e3f2fd"
}
p -> prim: "docs: specialization\nnot a subtype"
p -> use
prim -> use
```

**Fig. 1.** Boxed `Predicate` has the static helpers. Primitive predicates keep combinators but are different types. Stream `filter` is the boxed SAM ([[Which functional interface represents a filter or predicate in the Stream API]]). Two arguments: [[How would you explain the BiPredicate functional interface]].

Call sites: `Stream.filter(Predicate)` (and `Optional.filter`). `IntStream.filter(IntPredicate)`; also `anyMatch` / `allMatch` / `noneMatch`, `takeWhile` / `dropWhile`, and `IntStream.iterate(seed, hasNext, next)` for the `hasNext` test. A statement expression that returns `boolean` (for example `list.add(s)`) can be a `Predicate` body ([[How would you explain lambda expressions in Java]]).

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.IntPredicate;
import java.util.function.Predicate;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        List<String> list = new ArrayList<String>();
        Predicate<String> nonempty = s -> !s.isEmpty();
        Predicate<String> stored = nonempty.and(list::add);
        Predicate<String> empty = Predicate.not(nonempty); // Java 11
        Predicate<String> isNull = Predicate.isEqual(null);
        Stream.of("a", "").filter(nonempty);
        stored.test("a"); // add runs only because nonempty is true
        // nonempty.and(null); // NPE
    }

    static void primitive() {
        IntPredicate even = i -> (i & 1) == 0;
        IntPredicate pos = i -> i > 0;
        IntStream.of(-2, 2, 3).filter(even.and(pos));
        // Predicate<Integer> no = even; // does not compile
    }
}
```

**Listing 1.** `and` skips `list::add` when `nonempty` is false. `Predicate.not` is Java 11 and boxed-only. `even.and(pos)` stays an `IntPredicate` for `IntStream.filter`.

> [!warning] `IntPredicate` is not `Predicate<Integer>`
> `Stream<Integer>.filter` wants `Predicate`; `IntStream.filter` wants `IntPredicate`. You cannot `Predicate.not(even)` or assign the primitive type to the boxed one. `test(Integer)` on `Predicate<Integer>` can unbox and NPE; `IntPredicate.test(int)` has no `null` `Integer`.

> [!warning] `and` / `or` short-circuit and NPE on null `other`
> `p.and(q)` never calls `q.test` if `p` is false; `p.or(q)` never calls `q` if `p` is true. If `p.test` throws, `q` is skipped. `and(null)` / `or(null)` throw `NullPointerException` at **composition**, before any `test`. Primitive predicates have the same combinator rules, minus `isEqual` / `not`.

> [!tip] Interview answer
> **`Predicate<T>` is `boolean test(T)`, with short-circuit `and`/`or`, `negate`, `isEqual`, and Java 11 `Predicate.not`.** `Int`/`Long`/`DoublePredicate` take a primitive `test` and the same combinators, but they are not `Predicate` subtypes and have no static `not`/`isEqual`. Use boxed `filter` on `Stream`, `IntPredicate` on `IntStream`.
