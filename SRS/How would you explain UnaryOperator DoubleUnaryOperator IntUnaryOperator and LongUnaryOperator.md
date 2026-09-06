<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain UnaryOperator DoubleUnaryOperator IntUnaryOperator and LongUnaryOperator?

> [!abstract] Short answer
> **Same type in, same type out.** `UnaryOperator<T>` extends `Function<T,T>`; the SAM is still `apply(T)` → `T`. `IntUnaryOperator` / `LongUnaryOperator` / `DoubleUnaryOperator` are the primitive specializations (`applyAsInt` / `applyAsLong` / `applyAsDouble`). They do **not** extend `UnaryOperator`. All four have `compose`, `andThen`, and static `identity()`. Java 8. `List.replaceAll` and `Stream.iterate` take `UnaryOperator`; `IntStream.map` takes `IntUnaryOperator`.

## `Function<T,T>` with an `identity()` factory

`UnaryOperator<T>` “represents an operation on a single operand that produces a result of the same type as its operand.” It **is** a `Function<T,T>`: you may assign it wherever `Function<T,T>` is required. Extra static `identity()` returns a `UnaryOperator` that yields its argument. `compose` / `andThen` are **inherited from `Function`**, so `andThen` returns a `Function`, not a `UnaryOperator` ([[How would you explain Function DoubleFunction IntFunction and LongFunction variants]], [[How would you explain core functional interfaces in java.util.function]]).

`IntUnaryOperator` is “the primitive type specialization of `UnaryOperator` for `int`”: SAM `int applyAsInt(int)`. It declares its **own** `compose` / `andThen` (both take and return `IntUnaryOperator`) plus static `identity()`. `LongUnaryOperator` / `DoubleUnaryOperator` match that for `long` / `double`. They list **no** superinterface `UnaryOperator`. `null` `before` / `after` on `compose` / `andThen` is `NullPointerException`.

```d2
direction: down
f: "Function<T,R>\napply(T) → R" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
u: "UnaryOperator<T>\nextends Function<T,T>\nidentity()" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
p: "IntUnaryOperator\napplyAsInt(int) → int\ncompose / andThen / identity" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
f -> u: "same type both sides"
u -> p: "docs: specialization\nnot a subtype"
```

**Fig. 1.** Boxed operator is a `Function` subtype. Primitive operators keep combinators but are different types. Two operands: [[How would you explain BinaryOperator DoubleBinaryOperator IntBinaryOperator and LongBinaryOperator]].

Call sites: `List.replaceAll(UnaryOperator)` does `li.set(operator.apply(li.next()))`. A `null` operator is `NullPointerException`; a `null` result is NPE if the list forbids nulls; the list must support `set`. `Stream.map` can take a `UnaryOperator` because it **is** a `Function`. `Stream.iterate(seed, UnaryOperator)` is infinite `seed`, `f(seed)`, `f(f(seed))`, … (Java 9 adds `iterate(seed, Predicate, UnaryOperator)` with a stop test). `IntStream.map(IntUnaryOperator)` stays on `IntStream`. There is no `IntToIntFunction` — same-primitive maps are this type.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.IntUnaryOperator;
import java.util.function.UnaryOperator;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class Demo {
    static void sameTypeInOut() {
        UnaryOperator<String> upper = String::toUpperCase;
        List<String> names = new ArrayList<String>();
        names.add("ab");
        names.replaceAll(upper); // ["AB"]
        UnaryOperator<String> id = UnaryOperator.identity();
        Stream.iterate("a", s -> s + "a").limit(3);

        IntUnaryOperator times2 = i -> i * 2;
        IntUnaryOperator plus1 = i -> i + 1;
        IntStream.of(1, 2).map(times2.andThen(plus1)); // 3, 5
        // UnaryOperator<Integer> no = times2; // does not compile
        // times2.andThen(null); // NPE
    }
}
```

**Listing 1.** `replaceAll` applies a boxed `UnaryOperator`. Primitive `andThen` stays an `IntUnaryOperator` for `IntStream.map`.

> [!warning] Inherited `andThen` is a `Function`, not a `UnaryOperator`
> `UnaryOperator.andThen(f)` is `Function.andThen`: the result is `Function<T,V>`. If `V` is not `T`, you no longer have a `UnaryOperator`. `IntUnaryOperator.andThen` keeps `IntUnaryOperator` because it is redeclared. Do not assign `IntUnaryOperator` to `UnaryOperator<Integer>`.

> [!warning] `replaceAll` needs `set`; `iterate(seed, f)` does not stop
> Unmodifiable lists throw `UnsupportedOperationException`. `List.of` cannot `set`. Infinite `Stream.iterate(seed, f)` needs `limit` / `findFirst` / the Java 9 `hasNext` overload. `identity()` is “return the same value,” not “skip the call.”

> [!tip] Interview answer
> **`UnaryOperator<T>` is `Function<T,T>` — one value in, same type out, SAM `apply`, plus static `identity()`.** `Int`/`Long`/`DoubleUnaryOperator` use `applyAsInt` and friends and are not subtypes, but they do keep `compose`/`andThen`/`identity`. Use them for `List.replaceAll`, `Stream.iterate`, and `IntStream.map`.
