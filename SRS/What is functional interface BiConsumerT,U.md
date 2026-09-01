<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# What is functional interface BiConsumerT,U

> [!abstract] Short answer
> **`BiConsumer<T,U>` is Java 8’s two-in, void-out side-effect operator.** The SAM is `void accept(T, U)`. It is the two-arity specialization of `Consumer`, not a subtype. Expected to work by side-effects. `Map.forEach` takes `BiConsumer<? super K, ? super V>`.

## Two arguments, no result

`BiConsumer<T,U>` (`@since 1.8`) is a `@FunctionalInterface` for an operation that accepts two arguments and returns **no result**. Unlike most `java.util.function` types, it is **expected to operate via side-effects**. The SAM is `accept` ([[What is functional interface]], [[How would you explain the BiConsumer functional interface]], [[How would you explain for what needed functional interface ConsumerT DoubleConsumer IntConsumer and LongConsum]]).

`andThen(after)` returns a composed consumer: this `accept`, then `after.accept` on the **same** pair. If this throws, `after` is skipped. A `null` `after` throws `NullPointerException`.

It does **not** extend `Consumer`. One object is `Consumer<T>`. Object plus primitive is `ObjIntConsumer` / `ObjLongConsumer` / `ObjDoubleConsumer` — those are `(reference, primitive)` specializations of `BiConsumer`, not subtypes ([[How would you explain for what needed functional interface ObjDoubleConsumerT ObjIntConsumerT and ObjLongConsu]]).

`Map.forEach` (`@since 1.8` default) runs the action for each entry: `action.accept(key, value)`, in entry-set order unless the map says otherwise. `Iterable.forEach` is still `Consumer` — one element, not a pair ([[Which functional interface does Iterable forEach use]]).

```d2
direction: down
c: "Consumer<T>\naccept(T) → void" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
bi: "BiConsumer<T,U>\naccept(T, U) → void" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
obj: "ObjInt/Long/DoubleConsumer\naccept(T, primitive)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}

c -> bi: "two-arity specialization, not a subtype"
bi -> obj: "unbox the second arg"
```

**Fig. 1.** Same “do something, return nothing” shape. `Map.forEach` is the usual two-argument sink.

```java
import java.util.Map;
import java.util.function.BiConsumer;

class Demo {
    static void entries(Map<String, Integer> map) {
        BiConsumer<String, Integer> print = (k, v) -> System.out.println(k + "=" + v);
        print.andThen((k, v) -> {}).accept("a", 1);
        map.forEach(print);
    }
}
```

**Listing 1.** `accept` takes two references. `map.forEach` is `BiConsumer` of key and value. `andThen(null)` throws.

> [!warning] Not `Consumer` with a pair type
> `BiConsumer<T,U>` is not `Consumer<Map.Entry<T,U>>` and not a subtype of `Consumer`. You cannot pass it to `Iterable.forEach`. `ObjIntConsumer` is not `BiConsumer<T,Integer>` — the second argument is `int`.

> [!warning] `andThen` is sequential and fail-fast
> If the first consumer throws, the second never runs. That is not `Predicate.and`. Side effects in `Map.forEach` see each mapping once; concurrent mutation is the map’s problem (`ConcurrentModificationException` on many implementations).

> [!tip] Interview answer
> **`BiConsumer<T,U>` is `void accept(T, U)` — two values in, side effect, no result.** Two-arity `Consumer`. You need it for `Map.forEach`. `andThen` chains two consumers; `ObjIntConsumer` is the mixed primitive twin.
