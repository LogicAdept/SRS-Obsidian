<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface ToDoubleBiFunctionT,U ToIntBiFunctionT,U and ToLong

> [!abstract] Short answer
> **They are Java 8 two-in, primitive-out transformers.** `ToIntBiFunction<T,U>` / `ToLongBiFunction<T,U>` / `ToDoubleBiFunction<T,U>` take two reference arguments and return `int` / `long` / `double` — not `Integer` / `Long` / `Double`. The SAM is `applyAsInt` / `applyAsLong` / `applyAsDouble`. They are the primitive-result specializations of `BiFunction`, not subtypes.

## Two objects in, an unboxed number out

Each of these types (`@since 1.8`) is a `@FunctionalInterface` that accepts two arguments and produces a primitive numeric result. They do **not** extend `BiFunction`. There is no `andThen`. The dump’s wrapper return types are wrong ([[What is functional interface]], [[How would you explain ToDoubleBiFunction ToIntBiFunction and ToLongBiFunction]], [[How would you explain the BiFunction functional interface]]).

| Type | SAM | Result |
| --- | --- | --- |
| `ToIntBiFunction<T,U>` | `applyAsInt(T, U)` | `int` |
| `ToLongBiFunction<T,U>` | `applyAsLong(T, U)` | `long` |
| `ToDoubleBiFunction<T,U>` | `applyAsDouble(T, U)` | `double` |

`To` names the **result**. Both parameters stay objects (`T` and `U`). One object in, primitive out is `ToIntFunction` / `ToLongFunction` / `ToDoubleFunction` — a different family ([[How would you explain for what needed functional interface ToDoubleFunctionT ToIntFunctionT and ToLongFunction]]). Primitive-to-primitive maps (`IntToLongFunction`) have a primitive on the **left** of the name as well ([[How would you explain for what needed functional interface To Function]]).

```d2
direction: down
bi: "BiFunction<T,U,R>\ntwo objects → object" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
to: "ToInt/Long/DoubleBiFunction<T,U>\napplyAsX(T, U) → primitive" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
one: "ToIntFunction<T>\none object → int" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}

bi -> to: "specialization, not a subtype"
to -> one: "Bi = two arguments"
```

**Fig. 1.** `ToX` is the result. `Bi` means two reference arguments. Mixed primitive pairs like `IntToLongFunction` are not this set.

```java
import java.util.function.ToDoubleBiFunction;
import java.util.function.ToIntBiFunction;
import java.util.function.ToLongBiFunction;

class Demo {
    static void twoArgs() {
        ToIntBiFunction<String, String> chars = (a, b) -> a.length() + b.length();
        ToLongBiFunction<String, Integer> scaled = (s, n) -> (long) s.length() * n;
        ToDoubleBiFunction<Integer, Integer> ratio = (a, b) -> a / (double) b;
        chars.applyAsInt("ab", "c");   // 3
        scaled.applyAsLong("hi", 4);   // 8L
        ratio.applyAsDouble(1, 2);     // 0.5
    }
}
```

**Listing 1.** Call `applyAsInt`, not `apply`. A `BiFunction<String,String,Integer>` would box the sum. These interfaces do not chain with `andThen`.

> [!warning] The result is not a wrapper
> Dump text that says `ToIntBiFunction` “returns `Integer`” is wrong: the SAM is `applyAsInt(T, U)` → `int`. You cannot pass a `ToIntBiFunction` where `BiFunction<T,U,Integer>` is required. `ToIntFunction<T>` is the one-argument cousin.

> [!tip] Interview answer
> **`ToIntBiFunction<T,U>` is `int applyAsInt(T, U)` — two objects in, `int` out.** `ToLongBiFunction` and `ToDoubleBiFunction` match `long` and `double`. They exist so you do not box the result of a two-argument `BiFunction`. One argument is `ToIntFunction`; two primitives of different kinds is `IntToLongFunction`, not a `*BiFunction`.
