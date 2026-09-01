<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# What is functional interface BiFunctionT,U,R

> [!abstract] Short answer
> **`BiFunction<T,U,R>` is Java 8’s two-in, one-out transformer.** The SAM is `R apply(T, U)`. It is the two-arity specialization of `Function`, not a subtype. `BinaryOperator<T>` **is** a subinterface (`T` in, `T` in, `T` out). `Map.replaceAll` / `merge` take a `BiFunction`. `andThen` chains a **`Function`** on the result — there is no `compose`.

## Two arguments in, a result out

`BiFunction<T,U,R>` (`@since 1.8`) is a `@FunctionalInterface` that accepts two arguments and produces a result. The SAM is `apply` ([[What is functional interface]], [[How would you explain the BiFunction functional interface]], [[How would you explain for what needed functional interface FunctionT,R DoubleFunctionR IntFunctionR and LongFu]]).

`andThen(after)` applies **this first** (`T,U` → `R`), then `after` (`R` → `V`). `after` is a `Function`, not another `BiFunction`. A throw from either is relayed. A `null` `after` throws `NullPointerException`. There is no `compose` (nothing to run “before” two arguments in one `Function`).

`BinaryOperator<T>` extends `BiFunction<T,T,T>` ([[How would you explain for what needed functional interface BinaryOperatorT DoubleBinaryOperator IntBinaryOpera]]). Primitive **result** twins are `ToIntBiFunction` / `ToLongBiFunction` / `ToDoubleBiFunction` (`applyAsInt`, not `apply`) — they do not extend `BiFunction` ([[How would you explain for what needed functional interface ToDoubleBiFunctionT,U ToIntBiFunctionT,U and ToLong]]). Two-in void is `BiConsumer` ([[What is functional interface BiConsumerT,U]]).

`Map.replaceAll` takes `BiFunction<? super K, ? super V, ? extends V>` and replaces each value. `Map.merge` remaps two values with a `BiFunction<? super V, ? super V, ? extends V>`.

```d2
direction: down
f: "Function<T,R>\napply(T) → R" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
bi: "BiFunction<T,U,R>\napply(T, U) → R" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
bin: "BinaryOperator<T>\nextends BiFunction<T,T,T>" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}

f -> bi: "two-arity specialization, not a subtype"
bi -> bin: "same type in/out"
```

**Fig. 1.** `andThen` is `Function` on the result. `ToIntBiFunction` is a different type (`int` out), not a subtype.

```java
import java.util.Map;
import java.util.function.BiFunction;

class Demo {
    static void twoIn(Map<String, Integer> map) {
        BiFunction<String, String, Integer> chars = (a, b) -> a.length() + b.length();
        chars.andThen(Object::toString).apply("ab", "c"); // "3"
        map.replaceAll((k, v) -> v + 1);
    }
}
```

**Listing 1.** `apply` takes two references. `andThen` wants a `Function` of `R`. `replaceAll` is `BiFunction<K,V,V>`. `andThen(null)` throws.

> [!warning] `andThen` is not another `BiFunction`
> Dump text that stops at “two args in, `R` out” is true but incomplete: `Function.compose` does not exist here. You cannot `andThen` a two-argument function. `BiFunction<T,U,R>` is not `Function<Pair<T,U>,R>` and not a subtype of `Function`.

> [!warning] Primitive-result cousins are not `BiFunction<T,U,Integer>`
> `ToIntBiFunction.applyAsInt(T, U)` returns `int`. You cannot pass it where `BiFunction<T,U,Integer>` is required. `BinaryOperator` is the same-type special case, not a different arity.

> [!tip] Interview answer
> **`BiFunction<T,U,R>` is `R apply(T, U)` — two values in, a result out.** Two-arity `Function`. `andThen` maps the result with a `Function`. `BinaryOperator<T>` is `BiFunction<T,T,T>`. You meet it on `Map.replaceAll` / `merge`. Void two-arg is `BiConsumer`.
