<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# How would you explain what method `filter` in stream?

> [!abstract] Short answer
> **`filter(Predicate)` is a lazy intermediate op that keeps elements for which the predicate is true.** It returns a **new** stream of matches; it does not walk the source when you call it. The predicate must be non-interfering and stateless. Primitive streams take `IntPredicate` / `LongPredicate` / `DoublePredicate`.

## Keep matching elements, still a stream

`Stream.filter(Predicate<? super T> predicate)` returns a stream consisting of the elements of this stream that match the given predicate. It is an **intermediate** operation: it produces another `Stream`, and intermediate ops are **always lazy**. Calling `filter` does not filter yet. The source is traversed only when a **terminal** op runs (`count`, `collect`, `forEach`, …) ([[What intermediate stream operations do you know in Java]], [[When does a Java stream pipeline actually start executing]]).

The package doc classifies `filter` as **stateless**: each element is included or dropped on its own, with no memory of earlier elements (unlike `distinct` / `sorted`). The predicate is a functional-interface instance, usually a lambda or method reference (`String::isEmpty`, `x -> x > 0`) ([[Which functional interface represents a filter or predicate in the Stream API]], [[What is the Java Stream API]]).

`filter` does **not** change the element type. Dropped elements are gone from the downstream pipeline; kept elements pass through unchanged. Chain as many `filter`s as you need — each is another lazy stage, still one fused pass at the terminal.

`IntStream` / `LongStream` / `DoubleStream` have the same shape with primitive predicates. `Optional.filter` is a different method: 0-or-1 value, not a stream pipeline ([[What does Optional.filter do]], [[How do you count empty strings using filter]]).

```d2
direction: right
in: "source elements" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
pred: "predicate.test" {
  width: 180
  height: 50
  style.fill: "#fff8e1"
}
out: "matching Stream" {
  width: 170
  height: 50
  style.fill: "#e8f5e9"
}
in -> pred
pred -> out
```

**Fig. 1.** `filter` keeps elements for which the predicate is true; the result is still a stream.

```java
import java.util.List;

class Demo {
    static long nonemptyCount(List<String> words) {
        return words.stream()
            .filter(s -> !s.isEmpty())
            .count();
    }
}
```

**Listing 1.** `filter` then `count`: empty strings never reach the terminal. Until `count()`, no predicate has run.

> [!warning] The predicate must not mutate the source, and `filter` is not a loop
> A stateful predicate (`seen.add(e)`) makes results nondeterministic, especially in parallel. Mutating the backing collection inside `filter` is interference. `filter` also does **no** work by itself: `list.stream().filter(...)` with no terminal leaves the list untouched and runs zero tests.

> [!tip] Interview answer
> **`filter` is the lazy `WHERE` of the Stream API: `Predicate` in, same-type stream of matches out.** Nothing is selected until a terminal op. Use it to drop elements; use `map` when you need to **change** them.
