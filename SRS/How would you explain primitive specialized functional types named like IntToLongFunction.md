<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain primitive specialized functional types named like `IntToLongFunction`?

> [!abstract] Short answer
> **They are `Function` specializations that take and return primitives, so the lambda does not box.** `IntToLongFunction` is the `int`-to-`long` form: `long applyAsLong(int value)`. The name is **arg type**, then **`To` + result type**, then `Function`.

## Read the name left to right

`Function<T,R>` is objects in, objects out (`R apply(T t)`). Generics cannot be `int` or `long` ([[Why does type erasure prevent a List of int in Java]]), so `Function<Integer,Long>` would box and unbox ([[What are autoboxing and unboxing in Java]]).

`java.util.function` therefore ships primitive specializations. Three shapes, all `@FunctionalInterface` since 1.8:

| Name | Meaning | Method |
| --- | --- | --- |
| `IntToLongFunction` | `int` in, `long` out | `applyAsLong(int)` |
| `IntFunction<R>` | `int` in, object out | `apply(int)` |
| `ToLongFunction<T>` | object in, `long` out | `applyAsLong(T)` |

`Int…` on the left means the **argument** is `int` (`int`-consuming). `ToLong` means the **result** is `long` (`long`-producing). Put together: `IntToLongFunction`. The same `To` pattern is used for the other primitive pairs (`int`/`long`/`double`). When the result is still a reference type, there is no `To` (`IntFunction<R>`).

The SAM is not `apply` when the result is `long`: it is `applyAsLong`. A lambda `i -> (long) i` targets `IntToLongFunction` ([[What is functional interface]]). `IntToLongFunction` does **not** copy `Function`’s `compose` / `andThen` / `identity` defaults — only `applyAsLong`. Same primitive in and out is **`IntUnaryOperator`**, not `IntToIntFunction`.

Six types cover every pair among `int` / `long` / `double`:

| Type | SAM |
| --- | --- |
| `IntToLongFunction` | `applyAsLong(int)` |
| `IntToDoubleFunction` | `applyAsDouble(int)` |
| `LongToIntFunction` | `applyAsInt(long)` |
| `LongToDoubleFunction` | `applyAsDouble(long)` |
| `DoubleToIntFunction` | `applyAsInt(double)` |
| `DoubleToLongFunction` | `applyAsLong(double)` |

`IntStream.mapToLong` takes `IntToLongFunction`. Narrowing (`LongToIntFunction`) is a Java cast: overflow does not throw.

```d2
direction: down
f: "Function<T,R>\napply(T) → R" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
both: "IntToLongFunction\napplyAsLong(int) → long" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
arg: "IntFunction<R>\napply(int) → R" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ret: "ToLongFunction<T>\napplyAsLong(T) → long" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}

f -> both: "both ends primitive"
f -> arg: "int-consuming"
f -> ret: "long-producing"
```

**Fig. 1.** `IntToLongFunction` is both specializations at once: primitive argument and primitive result.

```java
import java.util.function.IntFunction;
import java.util.function.IntToLongFunction;
import java.util.function.ToLongFunction;

public final class IntToLongNaming {
    public static void main(String[] args) {
        IntToLongFunction widening = i -> (long) i * 1_000_000_000L;
        ToLongFunction<String> asLong = s -> Long.parseLong(s);
        IntFunction<String> label = i -> "n=" + i;

        System.out.println(widening.applyAsLong(3));
        System.out.println(asLong.applyAsLong("42"));
        System.out.println(label.apply(3));

        // Function<Integer, Long> boxed = i -> (long) i; // boxes Integer/Long
        // widening.apply(3);                             // compile error: applyAsLong
    }
}
```

**Listing 1.** `applyAsLong` on primitive-to-primitive and object-to-`long`. `IntFunction` still uses `apply` because the result is an object.

> [!warning] `Function<Integer,Long>` is not the same type, and `apply` will not compile
> A lambda can be compatible with more than one SAM if you ignore types, but `IntToLongFunction` is not a subtype of `Function`. Passing it where `Function<Integer,Long>` is required does not work without an adapter, and that adapter boxes. `applyAsLong` vs `apply` is a compile error, not a runtime surprise. Prefer the specialized type in hot `int`/`long` pipelines ([[Why prefer primitives over wrappers in hot loops in Java]]).

> [!tip] Interview answer
> **`IntToLongFunction` is `Function` with `int` in and `long` out — `applyAsLong(int)` — so nothing is boxed.** Six types cover `int`/`long`/`double` pairs. Names: left primitive is the argument, `ToX` is the result. `IntFunction` consumes `int` and returns an object; `ToLongFunction` returns `long` from an object. Same primitive both sides is a unary operator, not `IntToIntFunction`.
