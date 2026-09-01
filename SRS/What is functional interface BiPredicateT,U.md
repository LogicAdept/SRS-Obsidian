<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# What is functional interface BiPredicateT,U

> [!abstract] Short answer
> **`BiPredicate<T,U>` is Java 8’s two-in, `boolean`-out test.** The SAM is `boolean test(T, U)`. It is the two-arity specialization of `Predicate`, not a subtype. `and` / `or` / `negate` compose conditions. `Stream.filter` still wants a one-arg `Predicate` — this type is for two values at once.

## Two arguments, true or false

`BiPredicate<T,U>` (`@since 1.8`) is a `@FunctionalInterface` for a predicate of two arguments. The SAM is `test` ([[What is functional interface]], [[How would you explain the BiPredicate functional interface]], [[How would you explain for what needed functional interface PredicateT DoublePredicate IntPredicate and LongPre]]).

`and(other)` is short-circuit **AND**: if this is `false`, `other` is skipped. `or(other)` is short-circuit **OR**: if this is `true`, `other` is skipped. A throw from this skips `other`. A `null` `other` throws `NullPointerException`. `negate()` is a new predicate; it does not mutate this one.

It does **not** extend `Predicate`. There is no `isEqual` (that static is on `Predicate`). Two-in with a non-boolean result is `BiFunction`; two-in void is `BiConsumer` ([[What is functional interface BiFunctionT,U,R]], [[What is functional interface BiConsumerT,U]]).

`Stream.filter` takes `Predicate` ([[Which functional interface represents a filter or predicate in the Stream API]]). A `BiPredicate` is what you pass when the API already has two values (key and value, left and right, and so on).

```d2
direction: down
p: "Predicate<T>\ntest(T) → boolean" {
  width: 250
  height: 50
  style.fill: "#fff8e1"
}
bi: "BiPredicate<T,U>\ntest(T, U) → boolean" {
  width: 270
  height: 55
  style.fill: "#e8f5e9"
}
ops: "and / or / negate" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}

p -> bi: "two-arity specialization, not a subtype"
bi -> ops
```

**Fig. 1.** Same “yes/no question” shape. Combinators take another `BiPredicate`, not a `Predicate`.

```java
import java.util.function.BiPredicate;

class Demo {
    static void twoArgs() {
        BiPredicate<String, String> longer = (a, b) -> a.length() > b.length();
        longer.test("ab", "c");              // true
        longer.negate().test("ab", "c");     // false
        longer.and((a, b) -> b.length() > 0).test("ab", "c");
    }
}
```

**Listing 1.** `test` takes two references. `and` / `or` short-circuit; `and(null)` throws. `negate` returns a new predicate.

> [!warning] Not `Predicate` of a pair
> `BiPredicate<T,U>` is not `Predicate<Map.Entry<T,U>>` and not a subtype of `Predicate`. You cannot pass it to `Stream.filter`. Combinators need another `BiPredicate<? super T, ? super U>`, not a one-arg `Predicate`.

> [!warning] `and` / `or` short-circuit
> If the left predicate already decides the result, the right one never runs — and never throws. That is not `BiConsumer.andThen`, which always tries the first action. There is no `isEqual` helper on this type.

> [!tip] Interview answer
> **`BiPredicate<T,U>` is `boolean test(T, U)` — two values in, true or false out.** Two-arity `Predicate`. `and` / `or` / `negate` compose. `filter` still uses `Predicate`. Two arguments with a result object is `BiFunction`; void is `BiConsumer`.
