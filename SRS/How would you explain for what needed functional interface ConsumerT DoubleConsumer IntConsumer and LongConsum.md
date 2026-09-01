<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface ConsumerT DoubleConsumer IntConsumer and LongConsum

> [!abstract] Short answer
> **They are Java 8 one-in, void-out side-effect operators.** `Consumer<T>`’s SAM is `void accept(T)`. `IntConsumer` / `LongConsumer` / `DoubleConsumer` are the **primitive** specializations (`accept(int)` / `accept(long)` / `accept(double)`), not `Integer` / `Long` / `Double`. Streams and `Iterable.forEach` take them so `System.out::println` (and other mutators) can run per element.

## Side effects, not a return value

`Consumer<T>` (`@since 1.8`) is a `@FunctionalInterface` for an operation that accepts one argument and returns **no result**. Unlike most `java.util.function` types, it is **expected to operate via side-effects**. The SAM is `accept`. The dump lambda `hello.accept("world")` prints `Hello, world` ([[What is functional interface]], [[How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer]], [[How does Supplier differ from Consumer in Java]]).

`andThen(after)` returns a composed consumer: this `accept`, then `after.accept`. If this throws, `after` is skipped. A `null` `after` throws `NullPointerException`.

The primitive trio does **not** extend `Consumer`:

| Type | SAM | Argument |
| --- | --- | --- |
| `IntConsumer` | `accept(int)` | `int` |
| `LongConsumer` | `accept(long)` | `long` |
| `DoubleConsumer` | `accept(double)` | `double` |

Each also has `andThen` of the **same** primitive type. `Stream.forEach` / `Iterable.forEach` take `Consumer`; `IntStream.forEach` takes `IntConsumer` ([[Which functional interface does Iterable forEach use]], [[What is the difference between forEach and forEachOrdered on a stream]]). `BiConsumer` is two arguments — a different interface ([[How would you explain the BiConsumer functional interface]]).

```d2
direction: down
c: "Consumer<T>\naccept(T) → void" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
prim: "Int/Long/DoubleConsumer\naccept(primitive)" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
use: "forEach / peek" {
  width: 220
  height: 50
  style.fill: "#fff8e1"
}

c -> prim: "specialization, not a subtype"
c -> use
prim -> use
```

**Fig. 1.** Same “do something, return nothing” shape. Primitive consumers avoid boxing on `IntStream` / `LongStream` / `DoubleStream`.

```java
import java.util.function.Consumer;
import java.util.function.IntConsumer;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        Consumer<String> hello = name -> System.out.println("Hello, " + name);
        hello.andThen(s -> { }).accept("world");
        Stream.of("a", "b").forEach(System.out::println);
    }

    static void primitive() {
        IntConsumer print = System.out::println;
        IntStream.of(1, 2, 3).forEach(print);
    }
}
```

**Listing 1.** Dump `accept("world")` is legal. `System.out::println` is a `Consumer<String>` and an `IntConsumer` via overloads. `andThen(null)` throws.

> [!warning] Primitive consumers are not `Consumer<Integer>`
> Dump text that says `IntConsumer` “takes `Integer`” is wrong: the SAM is `accept(int)`. You cannot pass an `IntConsumer` where `Consumer<Integer>` is required. `peek` / `forEach` on an `IntStream` want `IntConsumer`.

> [!warning] `andThen` is sequential and fail-fast
> If the first consumer throws, the second never runs. That is not `and` on a `Predicate`. Side effects in `forEach` on a **parallel** stream may run on any thread, in any order — the action must synchronize shared state.

> [!tip] Interview answer
> **`Consumer<T>` is `void accept(T)` — one value in, side effect, no result.** `IntConsumer`, `LongConsumer`, and `DoubleConsumer` are the unboxed twins. You need them for `forEach` / `peek`. `andThen` chains two consumers; `BiConsumer` is the two-argument variant.
