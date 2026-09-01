<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface ToDoubleFunctionT ToIntFunctionT and ToLongFunction

> [!abstract] Short answer
> **They are Java 8 one-object-in, primitive-out transformers.** `ToIntFunction<T>` / `ToLongFunction<T>` / `ToDoubleFunction<T>` take a reference `T` and return `int` / `long` / `double` — not `Integer` / `Long` / `Double`. The SAM is `applyAsInt` / `applyAsLong` / `applyAsDouble`. `Stream.mapToInt` / `mapToLong` / `mapToDouble` take them so you can `sum` without boxing.

## Object in, an unboxed number out

Each of these types (`@since 1.8`) is a `@FunctionalInterface` that produces a primitive numeric result from one object. They are the primitive-producing specializations of `Function`, not subtypes. There is no `andThen` / `compose`. The dump’s wrapper return types are wrong ([[What is functional interface]], [[How would you explain ToDoubleFunction ToIntFunction and ToLongFunction]], [[What are map and mapToInt for in Java streams]]).

| Type | SAM | Result |
| --- | --- | --- |
| `ToIntFunction<T>` | `applyAsInt(T)` | `int` |
| `ToLongFunction<T>` | `applyAsLong(T)` | `long` |
| `ToDoubleFunction<T>` | `applyAsDouble(T)` | `double` |

`To` names the **result**. The argument stays a reference. The opposite mixed axis — primitive in, object out — is `IntFunction` / `LongFunction` / `DoubleFunction` (`apply`, not `applyAsInt`) ([[How would you explain for what needed functional interface FunctionT,R DoubleFunctionR IntFunctionR and LongFu]]). Two objects in, primitive out is `ToIntBiFunction` ([[How would you explain for what needed functional interface ToDoubleBiFunctionT,U ToIntBiFunctionT,U and ToLong]]). Primitive-to-primitive is `IntToLongFunction` ([[How would you explain for what needed functional interface To Function]]).

`Stream.map` takes `Function` and stays boxed. `mapToInt(ToIntFunction)` yields an `IntStream` so `sum` / `average` exist ([[Which functional interface does Stream map use]], [[How do you get all numbers in set]]).

```d2
direction: down
f: "Function<T,R>\napply(T) → R" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
to: "ToInt/Long/DoubleFunction<T>\napplyAsX(T) → primitive" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
use: "mapToInt / mapToLong / mapToDouble" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}

f -> to: "specialization, not a subtype"
to -> use
```

**Fig. 1.** `ToX` is the result. `IntFunction<R>` is the other mixed type (`int` in, object out). `ToIntBiFunction` adds a second object argument.

```java
import java.util.function.ToDoubleFunction;
import java.util.function.ToIntFunction;
import java.util.stream.Stream;

class Demo {
    static void unbox() {
        ToIntFunction<String> chars = String::length;
        ToLongFunction<String> bits = s -> (long) s.length() * Integer.SIZE;
        ToDoubleFunction<String> percents = s -> s.length() / 100.0;
        chars.applyAsInt("ab"); // 2
        Stream.of("a", "bb").mapToInt(chars).sum(); // 3
    }
}
```

**Listing 1.** `String::length` is a `ToIntFunction<String>`. `map` would yield `Stream<Integer>` with no `sum()`. Call `applyAsInt`, not `apply`.

> [!warning] The result is not a wrapper
> Dump text that says `ToIntFunction` “returns `Integer`” is wrong: the SAM is `applyAsInt(T)` → `int`. You cannot pass a `ToIntFunction` where `Function<T,Integer>` is required. `IntFunction<R>` is `int` → object — the arrows are reversed.

> [!warning] `map` is not `mapToInt`
> `Stream.map(String::length)` is `Function` → `Stream<Integer>`. Primitive terminals live on `IntStream`, which you get from `mapToInt`. Forgetting that is why `stream.sum()` does not compile on a boxed stream.

> [!tip] Interview answer
> **`ToIntFunction<T>` is `int applyAsInt(T)` — one object in, `int` out.** `ToLongFunction` and `ToDoubleFunction` match `long` and `double`. You need them for `mapToInt` / `mapToLong` / `mapToDouble`. `IntFunction` is the reverse mix; `ToIntBiFunction` is two objects in.
