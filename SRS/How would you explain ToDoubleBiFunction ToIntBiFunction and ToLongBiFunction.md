<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain ToDoubleBiFunction ToIntBiFunction and ToLongBiFunction?

> [!abstract] Short answer
> **Two arguments in, a primitive number out.** `ToIntBiFunction<T,U>` is `int applyAsInt(T t, U u)` — the **`int`-producing** primitive specialization of `BiFunction`. `ToLongBiFunction` / `ToDoubleBiFunction` are `applyAsLong` / `applyAsDouble`. They do **not** extend `BiFunction` and have **no** `andThen`. Java 8. `ToXxx` names the **result**; `Bi` names the arity.

## `ToXxx` is the return, `Bi` is two arguments

Package naming: prefix `ToXxx` when the **result** is primitive (`ToIntFunction`, `ToIntBiFunction`). The `Bi` prefix means two arguments, as on `BiFunction`. Combining them yields this trio: two reference (or boxed) arguments, primitive result ([[How would you explain core functional interfaces in java.util.function]], [[How would you explain the BiFunction functional interface]]).

`ToIntBiFunction<T,U>` “represents a function that accepts two arguments and produces an int-valued result.” SAM `applyAsInt(Object, Object)` — in source, `applyAsInt(T, U)`. `ToLongBiFunction` / `ToDoubleBiFunction` match that with `applyAsLong` / `applyAsDouble`. Method summary is **only** that SAM: no `compose`, no `andThen`, no `identity`.

They list **no** superinterface `BiFunction`. You cannot assign a `ToIntBiFunction<String,String>` to `BiFunction<String,String,Integer>`. `BiFunction.andThen` is a boxed-`Function` pipeline; it does not exist here.

```d2
direction: down
bi: "BiFunction<T,U,R>\napply(T, U) → R\nandThen" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
tobi: "ToIntBiFunction<T,U>\napplyAsInt(T, U) → int" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
to: "ToIntFunction<T>\napplyAsInt(T) → int" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
bi -> tobi: "ToXxx specializes return\nnot a subtype"
bi -> to: "one argument, same ToInt idea"
```

**Fig. 1.** `ToInt*` produces `int`. One-arg form is `ToIntFunction` ([[How would you explain ToDoubleFunction ToIntFunction and ToLongFunction]]). Consuming an `int` instead is `IntFunction` ([[How would you explain Function DoubleFunction IntFunction and LongFunction variants]]). Same-type boxed two-arg is `BinaryOperator` ([[How would you explain BinaryOperator DoubleBinaryOperator IntBinaryOperator and LongBinaryOperator]]).

Contrast the other `ToInt` / `Int` / `Bi` mixes:

| Type | Arguments | Result | SAM |
| --- | --- | --- | --- |
| `BiFunction<T,U,R>` | two refs | `R` | `apply` |
| `ToIntBiFunction<T,U>` | two refs | `int` | `applyAsInt` |
| `ToIntFunction<T>` | one ref | `int` | `applyAsInt` |
| `IntFunction<R>` | one `int` | `R` | `apply(int)` |

There is no `andThen` to turn the `int` into an object on this type — box yourself or use `BiFunction<T,U,Integer>`.

```java
import java.util.function.BiFunction;
import java.util.function.ToIntBiFunction;
import java.util.function.ToIntFunction;

class Demo {
    static void twoArgsIntOut() {
        ToIntBiFunction<String, String> total = (a, b) -> a.length() + b.length();
        int n = total.applyAsInt("a", "bb"); // 3
        ToIntFunction<String> one = String::length;
        BiFunction<String, String, Integer> boxed = (a, b) -> a.length() + b.length();
        Integer boxedN = boxed.apply("a", "bb");
        // BiFunction<String, String, Integer> no = total; // does not compile
        // total.andThen(i -> i); // ToIntBiFunction has no andThen
    }
}
```

**Listing 1.** `applyAsInt` returns `int`, not `Integer`. The boxed twin is `BiFunction<…, Integer>` with `apply`. One-arg primitive-result is `ToIntFunction`.

> [!warning] Specialization is not subtyping
> `ToIntBiFunction<T,U>` is not a `BiFunction<T,U,Integer>`. Map `compute` / `merge` / `replaceAll` and three-arg `reduce` want `BiFunction` (or `BinaryOperator`), not `ToIntBiFunction`. Passing `(a, b) -> a.length() + b.length()` works for both only because target typing picks `apply` vs `applyAsInt`.

> [!warning] No `andThen` — and `ToInt` is not `Int`
> You cannot `toIntBi.andThen(f)` the way `BiFunction` can. `IntFunction` / `IntConsumer` **consume** an `int`; these types **produce** one. Mixing `ToIntBiFunction` with `IntBinaryOperator` (`applyAsInt(int, int)`) is a different SAM: two primitives in, not two objects.

> [!tip] Interview answer
> **`ToIntBiFunction<T,U>` is `int applyAsInt(T, U)` — two arguments, primitive `int` out, the `ToInt` form of `BiFunction`.** `ToLong` / `ToDouble` are `applyAsLong` / `applyAsDouble`. They are not `BiFunction` subtypes and have no combinators. `ToXxx` is the result; `Bi` is arity; one-arg cousins are `ToIntFunction`, not these.
