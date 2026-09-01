<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# Which functional interface represents a filter or predicate in the Stream API?

> [!abstract] Short answer
> **`Predicate<T>` — SAM `boolean test(T)`.** `Stream.filter(Predicate)` keeps elements for which `test` is true. Java 8 `@FunctionalInterface` in `java.util.function`: a boolean-valued function of one argument. Primitive streams use `IntPredicate` / `LongPredicate` / `DoublePredicate`. `map` uses `Function`, not `Predicate`. The predicate must be non-interfering and stateless.

## `Predicate.test`, keep or drop

`Stream.filter` “returns a stream consisting of the elements of this stream that match the given predicate.” Intermediate, always lazy. The parameter is a non-interfering, stateless **predicate** ([[How would you explain what method filter in stream]], [[What intermediate stream operations do you know in Java]], [[How do you count empty strings using filter]]).

`java.util.function.Predicate<T>` (Java 8): “a predicate (boolean-valued function) of one argument.” Functional method: `boolean test(T t)`. Lambdas (`s -> !s.isEmpty()`) and method references (`String::isBlank` is Java 11) are assignment-compatible.

Defaults: `and` / `or` (short-circuit; if the left side decides, the other is not evaluated), `negate()`. Statics: `isEqual(targetRef)` (`Objects.equals`), `not(Predicate)` (Java 11, delegates to `negate()`).

Other Stream methods that take a `Predicate`: `anyMatch`, `allMatch`, `noneMatch`, `takeWhile`, `dropWhile`. Those are still predicates, not `filter` itself.

`map` takes `Function` (`apply` → `R`) ([[Which functional interface does Stream map use]], [[What is the Java Stream API]], [[What is Stream]]). A `Predicate` is not a `Function<T,Boolean>` in the Stream signatures — `filter` wants `test`, not `apply`.

```d2
direction: right
el: "T" {
  width: 70
  height: 40
  style.fill: "#e3f2fd"
}
p: "Predicate.test" {
  width: 160
  height: 40
  style.fill: "#fff8e1"
}
out: "keep if true" {
  width: 130
  height: 40
  style.fill: "#e8f5e9"
}
el -> p
p -> out
```

**Fig. 1.** `filter`’s argument is `Predicate`: one element in, boolean out.

```java
import java.util.List;
import java.util.function.Predicate;

class Demo {
    static long nonempty(List<String> words) {
        Predicate<String> keep = s -> !s.isEmpty();
        return words.stream().filter(keep).count();
    }
}
```

**Listing 1.** `s -> !s.isEmpty()` is a `Predicate<String>`. `filter` does not run until `count()`. `map(s -> !s.isEmpty())` would be `Stream<Boolean>`, not a filtered `Stream<String>`.

> [!warning] `Predicate` is not `Function`, and a stateful `test` is broken
> Returning `boolean` from `map` does not filter. Parallel `filter` with a predicate that mutates shared state is a data race. `and`/`or` short-circuit — do not rely on the second predicate always running. `Optional.filter` is the same `Predicate` idea on 0-or-1, not a stream stage.

> [!tip] Interview answer
> **Filter in the Stream API is `Predicate<T>` (`test` → `boolean`).** Primitives: `IntPredicate` and twins. `map` → `Function`. Compose with `and`/`or`/`negate`, or `Predicate.not` (11).
