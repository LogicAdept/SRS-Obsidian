<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #SRS

# How does Supplier differ from Consumer in Java?

> [!abstract] Short answer
> **Opposite arrows.** `Supplier<T>` is `T get()` — no input, a result. `Consumer<T>` is `void accept(T)` — one input, no result, and it is **expected to operate via side-effects**. They are both Java 8 `@FunctionalInterface` types; a lambda that matches one does not match the other. `Function<T,R>` sits between them: one argument in, a result out.

## Produce versus consume

`Supplier` “represents a supplier of results.” The platform states there is **no** requirement that each `get()` return a new or distinct object: a supplier may cache, share, or recompute. `Consumer` “represents an operation that accepts a single input argument and returns no result.” Unlike most `java.util.function` types, a consumer is expected to work by mutating, printing, collecting, or otherwise affecting state.

```d2
direction: right
sup: "Supplier<T>\nT get()" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
val: "value T" {
  width: 140
  height: 55
  style.fill: "#e3f2fd"
}
con: "Consumer<T>\nvoid accept(T)" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
sup -> val: "produces"
val -> con: "consumed"
```

**Fig. 1.** `get()` yields a `T`. `accept` takes that `T` and returns nothing. See [[What is functional interface]] and [[How would you explain for what needed functional interface SupplierT BooleanSupplier DoubleSupplier IntSupplie]].

`Consumer` has a default `andThen(after)`: run this `accept`, then `after.accept`, in that order. If this operation throws, `after` is **not** run. `andThen(null)` throws `NullPointerException` at composition time. `Supplier` has no `andThen` / `compose`. `Function.apply` is the type that both takes an argument and produces a result (`andThen` / `compose` / `identity` live there).

Typical call sites follow the shapes. `Iterable.forEach` and `Stream.forEach` take a `Consumer` and call `accept` per element ([[Which functional interface does Iterable forEach use]]). `Optional.ifPresent` takes a `Consumer` and runs it only when a value is present. `Stream.generate` takes a `Supplier` and yields an **infinite** sequential unordered stream. `Optional.orElseGet` / `orElseThrow` take a `Supplier` and invoke it on the empty path only — a present value does not require a non-null supplier (`NullPointerException` is specified only when no value is present **and** the supplier is null). `orElse(T)` takes a ready value, not a supplier.

Neither `get()` nor `accept(T)` declares a checked exception, so a lambda body targeting them cannot throw `IOException` unless it is caught inside or wrapped ([[Can a lambda throw a checked exception]]).

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Supplier;
import java.util.stream.Stream;

class Demo {
    static final String SHARED = "same";

    static void shapes() {
        Supplier<String> supply = () -> SHARED;
        Consumer<String> consume = s -> { };
        String v = supply.get();
        consume.accept(v);
        // Consumer<String> no = supply; // does not compile — different SAM
    }

    static void andThenThenGenerate() {
        List<String> log = new ArrayList<String>();
        Consumer<String> first = log::add;
        Consumer<String> then = s -> log.add(s.toUpperCase());
        first.andThen(then).accept("hi");
        // log is [hi, HI]; first.andThen(null) throws now, not at accept

        Stream.generate(() -> "x").limit(2).forEach(log::add);
        // generate is infinite; limit (or another short-circuit) is required
    }

    static String fallback() {
        return "computed";
    }

    static void optionalPaths() {
        Optional<String> present = Optional.of("a");
        String ready = present.orElse(fallback());
        String delayed = present.orElseGet(() -> fallback());
        present.orElseGet(null); // present: no NPE; empty + null supplier: NPE
    }
}
```

**Listing 1.** `SHARED` is a legal `Supplier` result — `get()` need not allocate. `andThen` sequences side effects. `orElse` takes a `T`; `orElseGet` takes a `Supplier`. Primitive-result / primitive-argument specializations are separate types: [[How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer]].

> [!warning] `get()` is not a factory contract
> “New object every call” is not part of `Supplier`. A constant, a cached instance, or `() -> SHARED` is valid. Treat `get()` as “produce a `T`,” then document uniqueness yourself if you need it. `Stream.generate` is infinite and unordered; without `limit`, `findFirst`, or another short-circuit it does not terminate.

> [!warning] `andThen(null)` fails before `accept`
> Composition throws `NullPointerException` if `after` is null. If this consumer throws during `accept`, the `after` consumer is skipped. `Iterable.forEach` does not call `andThen` for you, and modifying the source from the action has unspecified behavior unless the collection documents a concurrent-modification policy.

> [!tip] Interview answer
> **`Supplier` is `T get()` — zero in, a value out. `Consumer` is `void accept(T)` — one in, void out, meant for side effects.** They are not interchangeable lambdas. `andThen` exists on `Consumer` only; `get()` need not return a fresh object; `orElseGet` / `Stream.generate` take a `Supplier`, `forEach` / `ifPresent` take a `Consumer`.
