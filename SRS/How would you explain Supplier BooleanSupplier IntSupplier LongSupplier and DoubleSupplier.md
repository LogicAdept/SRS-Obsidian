<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain Supplier BooleanSupplier IntSupplier LongSupplier and DoubleSupplier

> [!abstract] Short answer
> **They are Java 8 zero-in, one-out factories.** `Supplier<T>`’s SAM is `T get()`. `BooleanSupplier` / `IntSupplier` / `LongSupplier` / `DoubleSupplier` are the **primitive-result** specializations (`getAsBoolean` / `getAsInt` / `getAsLong` / `getAsDouble`), not `Boolean` / `Integer` / `Long` / `Double`. Nothing is passed in. `Stream.generate` takes `Supplier`; `IntStream.generate` takes `IntSupplier`.

## No argument, a result

`Supplier<T>` (`@since 1.8`) is a `@FunctionalInterface` that supplies results. The SAM is `get`. There is **no** requirement that each call return a new or distinct value — a supplier may cache, share, or recompute. The dump method reference `LocalDateTime::now` matches: no arguments, a `LocalDateTime` out, then `now.get()` ([[What is functional interface]], [[How does Supplier differ from Consumer in Java]]).

There are no `andThen` / `compose` defaults. `Consumer` is the opposite shape: one value in, void out ([[How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer]]).

The primitive four do **not** extend `Supplier`. Their SAMs are **not** named `get`:

| Type | SAM | Result |
| --- | --- | --- |
| `BooleanSupplier` | `getAsBoolean()` | `boolean` |
| `IntSupplier` | `getAsInt()` | `int` |
| `LongSupplier` | `getAsLong()` | `long` |
| `DoubleSupplier` | `getAsDouble()` | `double` |

Each is the primitive-producing specialization of `Supplier`. Same rule: a distinct result is not required on every call. `Stream.generate` takes `Supplier`; `IntStream.generate` takes `IntSupplier` — both sources are infinite unless you `limit` ([[How do you print 10 random numbers in ascending order with streams]]).

```d2
direction: down
s: "Supplier<T>\nget() → T" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}
prim: "Boolean/Int/Long/DoubleSupplier\ngetAsX() → primitive" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
use: "generate" {
  width: 180
  height: 50
  style.fill: "#fff8e1"
}

s -> prim: "specialization, not a subtype"
s -> use
prim -> use
```

**Fig. 1.** Same “produce a value, take nothing” shape. Primitive suppliers unbox the **result**. Call `getAsInt`, not `get`.

```java
import java.time.LocalDateTime;
import java.util.function.IntSupplier;
import java.util.function.Supplier;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void boxed() {
        Supplier<LocalDateTime> now = LocalDateTime::now;
        now.get();
        Stream.generate(now).limit(1);
    }

    static void primitive() {
        IntSupplier ones = () -> 1;
        ones.getAsInt();
        IntStream.generate(ones).limit(3);
    }
}
```

**Listing 1.** Dump `now.get()` is legal. `IntSupplier` uses `getAsInt`. `generate` without `limit` does not terminate.

> [!warning] Primitive suppliers are not `Supplier<Integer>`
> Dump text that says `IntSupplier` “returns `Integer`” is wrong: the SAM is `getAsInt()` → `int`. There is no `get()` on the primitive types. You cannot pass an `IntSupplier` where `Supplier<Integer>` is required.

> [!warning] Each `get` may return the same instance
> The contract does not demand a fresh object per call. A `Supplier` that always returns the same list is legal — mutating that list later surprises every caller. `generate` is infinite; forget `limit` and the terminal never finishes.

> [!tip] Interview answer
> **`Supplier<T>` is `T get()` — no input, a result out.** `BooleanSupplier`, `IntSupplier`, `LongSupplier`, and `DoubleSupplier` are the unboxed-result twins (`getAsBoolean` / `getAsInt` / `getAsLong` / `getAsDouble`). You need them for `generate` and other deferred factories. `Consumer` is the reverse (`accept`, void).
