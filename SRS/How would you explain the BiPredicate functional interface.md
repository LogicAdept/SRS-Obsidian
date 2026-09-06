<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain the BiPredicate functional interface?

> [!abstract] Short answer
> **`BiPredicate<T,U>` is a boolean-valued function of two arguments.** SAM `boolean test(T t, U u)`. It is the **two-arity** specialization of `Predicate`, not a subtype of `Predicate`. Java 8. Combinators are the same idea as `Predicate`: short-circuit `and` / `or`, plus `negate`. There is **no** `isEqual` and **no** `BiPredicate.not`. `Stream.filter` still wants a one-arg `Predicate`.

## `test(T, U)`, then `and` / `or` / `negate`

`BiPredicate<T,U>` “represents a predicate (boolean-valued function) of two arguments.” `test` returns `true` if the pair matches. That is the `Bi` arity prefix on `Predicate`, not a `Predicate` that you pass two values to ([[How would you explain Predicate DoublePredicate IntPredicate and LongPredicate]], [[What is functional interface]]).

`and(other)` / `or(other)` compose two `BiPredicate`s. Evaluation is **short-circuit**: `and` skips `other` when this is `false`; `or` skips `other` when this is `true`. If this `test` throws, `other` is not evaluated. A `null` `other` throws `NullPointerException` at composition. `negate()` flips the boolean. Combinators return `BiPredicate<T,U>`.

Boxed `Predicate` also has static `isEqual` and `Predicate.not` (Java 11). **`BiPredicate` does not.** Comparing two live arguments is a lambda you write (`(a, b) -> …`); `Predicate.isEqual` captures **one** target and tests **one** argument.

```d2
direction: down
p: "Predicate<T>\ntest(T)\nand / or / negate / isEqual / not" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
bi: "BiPredicate<T,U>\ntest(T, U)\nand / or / negate only" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
no: "Stream.filter\nstill Predicate" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
p -> bi: "arity prefix Bi\nnot a subtype"
bi -> no: "does not replace filter"
```

**Fig. 1.** Two-arg `test`. Same short-circuit combinators as `Predicate`, minus the static helpers. Filter is still one-arg ([[Which functional interface represents a filter or predicate in the Stream API]]). Two-arg `apply` / `accept` are different shapes: [[How would you explain the BiFunction functional interface]], [[How would you explain the BiConsumer functional interface]].

`IntPredicate` is one primitive, not a two-arg `BiPredicate`. `BiPredicate`’s type parameters are the two arguments to `test`.

```java
import java.util.function.BiPredicate;

class Demo {
    static void twoArgs() {
        BiPredicate<String, Integer> longEnough = (s, n) -> s.length() >= n;
        BiPredicate<String, Integer> nonempty = (s, n) -> !s.isEmpty();
        boolean ok = longEnough.and(nonempty).test("ab", 2); // true
        BiPredicate<String, Integer> tooShort = longEnough.negate();
        // Predicate<String> no = longEnough; // does not compile
        // longEnough.and(null); // NPE now
    }
}
```

**Listing 1.** `and` is another `BiPredicate`; both arguments are supplied together at `test`.

> [!warning] `BiPredicate` is not a `Predicate` and not `filter`
> `Stream.filter` / `Optional.filter` take `Predicate`. You cannot pass `(k, v) -> …` there. Bind one argument in a closure (`v -> pred.test(k, v)`) or `filter` a stream of pairs. `IntPredicate` is one `int`, not a two-arg `BiPredicate`.

> [!warning] `and` / `or` short-circuit and NPE on null `other`
> `p.and(q)` never calls `q.test` if `p` is false; `p.or(q)` never calls `q` if `p` is true. If `p.test` throws, `q` is skipped. `and(null)` / `or(null)` throw at **composition**, before any `test`. There is no `BiPredicate.not(p)` factory — use `p.negate()`.

> [!tip] Interview answer
> **`BiPredicate<T,U>` is `boolean test(T, U)` — two-argument `Predicate`, not a subtype.** It has short-circuit `and`/`or` and `negate`, but not `isEqual` or `Predicate.not`. `Stream.filter` still wants a one-arg `Predicate`; use `BiPredicate` when the test naturally takes a pair (key and value, two operands).
