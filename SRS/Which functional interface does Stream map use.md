<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# Which functional interface does Stream `map` use?

> [!abstract] Short answer
> **`Function<T,R>` — SAM `apply(T)` → `R`.** `Stream.map` takes `Function<? super T, ? extends R>`: one argument in, one result out, new stream of `R`. Java 8 `@FunctionalInterface` in `java.util.function`. Primitive cousins: `mapToInt` → `ToIntFunction`, `mapToLong` → `ToLongFunction`, `mapToDouble` → `ToDoubleFunction`. `filter` is `Predicate`, not `Function`. The mapper must be non-interfering and stateless.

## `Function.apply`, one-to-one

`Stream.map(Function mapper)` “returns a stream consisting of the results of applying the given function to the elements of this stream.” Intermediate, always lazy. Parameters: a non-interfering, stateless **function** per element ([[What are map and mapToInt for in Java streams]], [[What intermediate stream operations do you know in Java]]).

`java.util.function.Function<T,R>` (Java 8): “a function that accepts one argument and produces a result.” Functional method: `R apply(T t)`. Lambdas (`s -> s.toUpperCase()`) and method references (`String::toUpperCase`, `Widget::weight`) are assignment-compatible. Defaults: `compose`, `andThen`; static `identity()`. `UnaryOperator<T>` extends `Function<T,T>` — a same-type `map` may be a `UnaryOperator`, still a `Function`.

That is **one-to-one**. A function that returns a `Stream` or `List` still yields `Stream<Stream<…>>` / `Stream<List<…>>` until `flatMap` (which also takes a `Function`, but to a stream of values) ([[What is the difference between Stream map and flatMap]], [[What is the Java Stream API]]).

`filter` uses `Predicate` (`test` → `boolean`) ([[Which functional interface represents a filter or predicate in the Stream API]]). `forEach` uses `Consumer`. Do not answer “`Function`” for those.

```d2
direction: right
t: "T" {
  width: 70
  height: 40
  style.fill: "#e3f2fd"
}
fn: "Function.apply" {
  width: 160
  height: 40
  style.fill: "#fff8e1"
}
r: "R" {
  width: 70
  height: 40
  style.fill: "#e8f5e9"
}
t -> fn
fn -> r
```

**Fig. 1.** `map`’s mapper is `Function`: one in, one out.

```java
import java.util.List;
import java.util.function.Function;
import java.util.stream.Stream;

class Demo {
    static Stream<Integer> lengths(List<String> words) {
        Function<String, Integer> len = String::length;
        return words.stream().map(len);
    }
}
```

**Listing 1.** `String::length` is a `Function<String,Integer>`. `mapToInt(String::length)` would be `ToIntFunction` and an `IntStream` instead.

> [!warning] `Function` is not `Predicate`, and a stateful `apply` is broken
> `s -> s.isEmpty()` is a `Predicate` — that is `filter`. Returning `Optional` from `map` yields `Stream<Optional<T>>`, not a flatten. Parallel `map` with a mapper that mutates shared state is a data race; JavaDoc requires a **stateless** function.

> [!tip] Interview answer
> **`Stream.map` uses `Function<T,R>` (`apply`).** Primitive maps use `ToIntFunction` / `ToLongFunction` / `ToDoubleFunction`. `filter` → `Predicate`. `flatMap` → `Function` that **returns a `Stream`**.
