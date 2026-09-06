<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain the BiFunction functional interface?

> [!abstract] Short answer
> **`BiFunction<T,U,R>` is two values in, a result out:** SAM `R apply(T t, U u)`. It is the **two-arity** specialization of `Function`, not a subtype of `Function`. Java 8. `andThen(Function)` runs `apply` then the `Function`; there is **no** `compose`. `BinaryOperator<T>` extends `BiFunction<T,T,T>`. `Map.compute` / `merge` / `replaceAll` and the three-arg `Stream.reduce` take a `BiFunction`.

## Two arguments, one result

`BiFunction<T,U,R>` “represents a function that accepts two arguments and produces a result.” The functional method is `apply(Object, Object)` — in source, `apply(T, U)` returning `R`. That is the `Bi` arity prefix on `Function`, not a second `apply` on `Function` itself ([[How would you explain Function DoubleFunction IntFunction and LongFunction variants]], [[What is functional interface]]).

`andThen(after)` returns `BiFunction<T,U,V>`: this `apply`, then `after.apply` on that result. A `null` `after` throws `NullPointerException`. `after` is a **`Function`**, not a `BiFunction` — you cannot pipe a second two-arg function with `andThen`. There is no `compose` and no static `identity` on `BiFunction` (those live on `Function` / `UnaryOperator`).

```d2
direction: down
f: "Function<T,R>\napply(T) → R\ncompose / andThen / identity" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
bi: "BiFunction<T,U,R>\napply(T, U) → R\nandThen only" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
bin: "BinaryOperator<T>\nextends BiFunction<T,T,T>" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
f -> bi: "arity prefix Bi\nnot a subtype"
bi -> bin: "same three types"
```

**Fig. 1.** Two-arg `apply` plus `andThen`. Same-type case is `BinaryOperator` ([[How would you explain BinaryOperator DoubleBinaryOperator IntBinaryOperator and LongBinaryOperator]]). Void two-arg is `BiConsumer` ([[How would you explain the BiConsumer functional interface]]). Primitive-result cousins: [[How would you explain ToDoubleBiFunction ToIntBiFunction and ToLongBiFunction]].

`BinaryOperator<T>` **is** a `BiFunction<T,T,T>` (you may assign it where `BiFunction<T,T,T>` is required). `ToIntBiFunction<T,U>` is a **different** type (`applyAsInt`), not a `BiFunction<T,U,Integer>`.

Call sites: `Map.replaceAll` does `entry.setValue(function.apply(key, value))`. `compute` / `computeIfPresent` pass `(key, oldValue)` — returning `null` removes the mapping. `merge` takes a `BiFunction` to combine an incoming value with the existing one. `computeIfAbsent` is a **`Function`** (key only), not a `BiFunction`. Three-arg `Stream.reduce(identity, accumulator, combiner)` uses `BiFunction<U,? super T,U>` as the accumulator (`accumulator.apply(result, element)`) and a `BinaryOperator` combiner.

```java
import java.util.HashMap;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Stream;

class Demo {
    static void applyThenMap() {
        BiFunction<String, String, String> concat = String::concat;
        Function<String, Integer> len = String::length;
        BiFunction<String, String, Integer> both = concat.andThen(len);
        int n = both.apply("a", "bb"); // 3
        // concat.compose(len); // does not compile — no compose

        Map<String, String> m = new HashMap<String, String>();
        m.compute("k", (k, v) -> (v == null) ? "x" : v.concat("x"));
        Stream.of("a", "b").reduce("", String::concat, String::concat);
        // concat.andThen(null); // NPE
    }
}
```

**Listing 1.** `andThen` attaches a one-arg `Function` to the **result**. `Map.compute` is the documented `(k, v) -> v == null ? msg : v.concat(msg)` shape. Three-arg `reduce` uses a `BiFunction` accumulator plus a `BinaryOperator` combiner.

> [!warning] `andThen` is not a second `BiFunction`; there is no `compose`
> `after` must be `Function<? super R, ? extends V>`. Two two-arg functions do not compose with this API. `Function.identity()` is not a `BiFunction`. `andThen(null)` throws at composition, before any `apply`.

> [!warning] `computeIfAbsent` is not a `BiFunction`
> It takes `Function<? super K, ? extends V>` — only the key. `compute` / `computeIfPresent` / `merge` / `replaceAll` take `BiFunction`. Returning `null` from those remapping functions **removes** the entry (or leaves it absent). Do not mutate the map inside the remapping function. `ToIntBiFunction` is not assignable to `BiFunction<T,U,Integer>`.

> [!tip] Interview answer
> **`BiFunction<T,U,R>` is `R apply(T, U)` — two in, a result out, the two-argument `Function`.** It has `andThen` onto a `Function`, not `compose`. `BinaryOperator` is the same-type subtype. Maps use it for `compute`/`merge`/`replaceAll`; three-arg `reduce` uses it as the accumulator.
