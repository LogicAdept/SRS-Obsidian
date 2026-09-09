<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #SRS

# What are the main functional interfaces in java.util.function

> [!abstract] Short answer
> **The four archetypes: `Function<T,R>` (T → R), `Predicate<T>` (T → boolean), `Consumer<T>` (T → void), `Supplier<T>` (() → T) — plus the operator pair, `UnaryOperator<T>` and `BinaryOperator<T>`, for same-type in/out, and `BiFunction` for two arguments.** Primitive specializations (`IntPredicate`, `ToIntFunction`, ...) exist to avoid boxing.

## The five you name first

| Interface | Signature | Typical use |
|---|---|---|
| `Function<T,R>` | `R apply(T)` | transform: `map`, field extraction |
| `Predicate<T>` | `boolean test(T)` | filter, condition |
| `Consumer<T>` | `void accept(T)` | side effect: forEach, logging |
| `Supplier<T>` | `T get()` | factory, lazy value |
| `UnaryOperator<T>` / `BinaryOperator<T>` | `T → T` / `(T,T) → T` | same-type math, `reduce` |

```d2
direction: right
in: "Input T" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
out: "Output" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
f: "Function<T,R>\nR apply(T)" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
p: "Predicate<T>\nboolean test(T)" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
c: "Consumer<T>\nvoid accept(T)\n(nothing out)" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
s: "Supplier<T>\nT get()\n(nothing in)" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
in -> f -> out
in -> p -> out
in -> c
s -> out
```

**Fig. 1.** Four shapes of in/out: transform, decide, consume, produce.

```java
Function<Integer, Integer> square = x -> x * x;
Predicate<Integer> even = x -> x % 2 == 0;
Supplier<String> greeting = () -> "hi";
UnaryOperator<String> shout = s -> s + "!";
System.out.println("square(7)=" + square.apply(7) + " even(7)=" + even.test(7)
        + " greeting=" + greeting.get() + " shout=" + shout.apply("go"));
```

**Listing 1.** Verified on JDK 21:

```java
square(7)=49 even(7)=false greeting=hi shout=go!
```

**Listing 2.** Each lambda's shape matches its interface: transform, test, produce, same-type transform.

## The siblings worth knowing

`BiFunction<T,U,R>` takes two arguments (its boolean-result cousin is `BiPredicate`; `BiConsumer` for two-argument side effects). `BinaryOperator<T>` is `BiFunction<T,T,T>` — the natural argument type of `Stream.reduce`. `UnaryOperator<T>` is `Function<T,T>` — `String::trim` shaped things. The primitive specializations (`IntFunction<R>`, `ToIntFunction<T>`, `IntPredicate`, `IntSupplier`, ...) remove boxing on hot paths: a `Function<Integer,Integer>` pays Integer boxing per call, `IntUnaryOperator` does not. Composition methods ride along: `Function.andThen`/`compose`, `Predicate.and`/`or`/`negate`. The SAM rule behind all of them is in [[How would you explain requirements for a Java functional interface]]; what existed before the package is in [[How would you explain classic functional style interfaces before java.util.function]].

> [!warning] Do not confuse the four by direction — and do not forget boxing
> The traps: using `Consumer` where `Function` is wanted (a consumer returns void — the stream `map` will not compile), mixing `Function<T,T>` with `UnaryOperator` (interchangeable as lambdas, but named operators document intent and appear in method signatures), and autoboxing blindness — `Function<Integer,Integer>` inside a hot loop generates allocations that `IntUnaryOperator` avoids entirely. Also, method-reference targeting is exact: `String::length` fits `Function<String,Integer>`, not `ToIntFunction<String>`... actually it fits both as a lambda shape, but the *generic* `Function` boxes the int — the specialization is what makes it cheap. Where these interfaces meet streams, the boxing story repeats per element; that is the level of detail a "name the java.util.function interfaces" question wants after the list.

> [!tip] Interview answer
> **Four basics: Function T to R, Predicate T to boolean, Consumer T to void, Supplier nothing-in T-out. Operators are same-type: UnaryOperator is Function T to T, BinaryOperator is BiFunction T,T,T for reduce. BiFunction covers two-argument transforms, and primitive variants like IntPredicate or ToIntFunction exist to skip boxing. Composability is built in: andThen, compose, and, or, negate.**

