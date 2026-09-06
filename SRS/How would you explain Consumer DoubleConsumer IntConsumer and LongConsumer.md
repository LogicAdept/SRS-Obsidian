<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer?

> [!abstract] Short answer
> **One value in, void out, meant for side effects.** `Consumer<T>`’s SAM is `void accept(T)`. `IntConsumer` / `LongConsumer` / `DoubleConsumer` are the **primitive** specializations (`accept(int)` / `accept(long)` / `accept(double)`). They do **not** extend `Consumer`. All four are Java 8 `@FunctionalInterface` types with `andThen`. `Iterable.forEach` / `Stream.forEach` / `Optional.ifPresent` take `Consumer`; `IntStream.forEach` takes `IntConsumer`.

## Side effects, then primitive `accept`

`Consumer<T>` “represents an operation that accepts a single input argument and returns no result.” Unlike most `java.util.function` types, it is **expected to operate via side-effects**. The body prints, collects, or mutates; it does not produce a value for the caller ([[What is functional interface]], [[How does Supplier differ from Consumer in Java]]).

`andThen(after)` returns a composed consumer: this `accept`, then `after.accept`. If this operation throws, `after` is **not** run. `andThen(null)` throws `NullPointerException` at composition time. `accept` declares no checked exceptions ([[Can a lambda throw a checked exception]]).

```d2
direction: down
c: "Consumer<T>\nvoid accept(T)" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
p: "Int / Long / DoubleConsumer\naccept(int / long / double)" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
use: "forEach / ifPresent\nandThen chains" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
c -> p: "docs: specialization\nnot a subtype"
c -> use
p -> use
```

**Fig. 1.** Boxed and primitive consumers share the side-effect contract and `andThen`. They are different types. Two arguments is a different interface: [[How would you explain the BiConsumer functional interface]]. Object-plus-primitive: [[How would you explain ObjDoubleConsumer ObjIntConsumer and ObjLongConsumer]].

`IntConsumer` is “the primitive type specialization of `Consumer` for `int`”: SAM `accept(int)`, same side-effect expectation, `andThen` returning `IntConsumer`. `LongConsumer` / `DoubleConsumer` match that for `long` / `double`. They list **no** superinterface `Consumer`: you cannot assign an `IntConsumer` to `Consumer<Integer>`. `IntStream.Builder` is an `IntConsumer`; `IntSummaryStatistics` implements it.

Call sites follow the type. `Iterable.forEach(Consumer)` is an enhanced-`for` that calls `action.accept(t)` ([[Which functional interface does Iterable forEach use]]). `Stream.forEach` / `forEachOrdered` take `Consumer`. `Optional.ifPresent` runs a `Consumer` only when a value is present (`NullPointerException` if present **and** the action is null). `IntStream.forEach(IntConsumer)` is the primitive pipeline; parallel `forEach` does not promise encounter order, and shared-state actions must synchronize.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.IntConsumer;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        List<String> log = new ArrayList<String>();
        Consumer<String> first = log::add;
        Consumer<String> then = s -> log.add(s.toUpperCase());
        first.andThen(then).accept("hi"); // [hi, HI]
        Stream.of("a").forEach(log::add);
        Optional.of("x").ifPresent(log::add);
        // first.andThen(null); // NPE now
    }

    static void primitive() {
        List<Integer> log = new ArrayList<Integer>();
        IntConsumer first = i -> log.add(i);
        IntConsumer then = i -> log.add(i * 2);
        first.andThen(then).accept(3); // [3, 6]
        IntStream.of(1, 2).forEach(i -> log.add(i));
        // Consumer<Integer> no = first; // does not compile
    }
}
```

**Listing 1.** `andThen` sequences side effects. `forEach` / `ifPresent` take `Consumer`; `IntStream.forEach` takes `IntConsumer`. The primitive value is `int`, not `Integer`.

> [!warning] Primitive consumers are not `Consumer` subtypes
> `IntConsumer` cannot be passed to `Iterable<Integer>.forEach` or `Stream<Integer>.forEach`. Those want `Consumer<? super Integer>` and will box. `IntStream.forEach` wants `IntConsumer`. A `Consumer<Integer>` in a hot primitive loop is a different type with `Integer` arguments.

> [!warning] `andThen(null)` fails before `accept`; `forEach` is not `andThen`
> Composition throws `NullPointerException` if `after` is null. If this consumer throws during `accept`, the `after` consumer is skipped. `Iterable.forEach` calls `accept` once per element — it does not compose with `andThen` for you. Modifying the iterable from the action has unspecified behavior unless the collection documents a concurrent-modification policy. Parallel `Stream.forEach` / `IntStream.forEach` may run the action on any thread, in any order.

> [!tip] Interview answer
> **`Consumer<T>` is `void accept(T)` — one in, nothing out, used for side effects, with `andThen` to chain.** `Int`/`Long`/`DoubleConsumer` are primitive specializations with `accept(int)` and friends; they do not extend `Consumer`. `forEach` and `ifPresent` take the boxed type; primitive streams take the primitive consumer.
