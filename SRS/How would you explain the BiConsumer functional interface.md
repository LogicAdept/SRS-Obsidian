<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain the BiConsumer functional interface?

> [!abstract] Short answer
> **`BiConsumer<T,U>` is two values in, void out, meant for side effects.** SAM `void accept(T t, U u)`. It is the **two-arity** specialization of `Consumer`, not a subtype of `Consumer`. Java 8. `andThen` runs this `accept`, then `after.accept`; a `null` `after` throws `NullPointerException` at composition. `Map.forEach` and `Stream.collect`’s accumulator/combiner take `BiConsumer`.

## Two arguments, no result

`BiConsumer<T,U>` “represents an operation that accepts two input arguments and returns no result.” Like `Consumer`, it is **expected to operate via side-effects**. The functional method is `accept(Object, Object)` — in source, `accept(T, U)`. There is no return to chain as a value; composition is `andThen` only ([[How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer]], [[What is functional interface]]).

`andThen(after)` returns a composed `BiConsumer`: this operation, then `after`. If this `accept` throws, `after` is **not** run. `andThen(null)` throws `NullPointerException` immediately. `accept` declares no checked exceptions.

```d2
direction: down
c: "Consumer<T>\naccept(T)" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
bi: "BiConsumer<T,U>\naccept(T, U)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
obj: "ObjIntConsumer<T>\naccept(T, int)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
c -> bi: "arity prefix Bi\nnot a subtype"
bi -> obj: "(reference, int)\nspecialization, not a subtype"
```

**Fig. 1.** `Bi` raises arity. Primitive second argument is `ObjIntConsumer`, a different type ([[How would you explain ObjDoubleConsumer ObjIntConsumer and ObjLongConsumer]]). One-arg `Iterable.forEach` stays `Consumer` ([[Which functional interface does Iterable forEach use]]).

`Map.forEach(BiConsumer<? super K, ? super V>)` walks entries: default body is `action.accept(entry.getKey(), entry.getValue())`. A `null` action is `NullPointerException`. If an entry is removed during iteration, `ConcurrentModificationException`. Passing a one-arg `Consumer` does not compile.

`Stream.collect(Supplier, BiConsumer, BiConsumer)` is a mutable reduction: `accumulator.accept(result, element)` folds each element into the container; the combiner merges two containers. Documented method references: `ArrayList::new`, `ArrayList::add`, `ArrayList::addAll`. The supplier must return a **fresh** container on each parallel call.

Two-arity `Function` is `BiFunction` (`apply` returns a value), not this type.

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiConsumer;
import java.util.stream.Stream;

class Demo {
    static void mapAndCollect() {
        Map<String, Integer> m = new HashMap<String, Integer>();
        m.put("a", 1);
        List<String> log = new ArrayList<String>();
        BiConsumer<String, Integer> first = (k, v) -> log.add(k + v);
        BiConsumer<String, Integer> then = (k, v) -> log.add(k);
        m.forEach(first.andThen(then));
        List<String> asList = Stream.of("x", "y")
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
        // m.forEach(s -> { }); // Consumer — does not compile
        // first.andThen(null); // NPE now
    }
}
```

**Listing 1.** `Map.forEach` supplies key and value to `accept`. `andThen` sequences two side effects. `collect` uses `BiConsumer` to mutate the list (`add`) and to merge lists (`addAll`).

> [!warning] `Map.forEach` is not `Iterable.forEach`
> A `Map` is not an `Iterable` of entries in the `forEach(Consumer)` sense. You need `(k, v) -> …` or `entrySet().forEach(e -> …)` with a `Consumer<Map.Entry<…>>`. `andThen` is composition of two `BiConsumer`s; `Map.forEach` does not call `andThen` for you.

> [!warning] `andThen(null)` fails before `accept`; `ObjIntConsumer` is not a `BiConsumer`
> Composition throws `NullPointerException` if `after` is null. If this consumer throws, `after` is skipped. `ObjIntConsumer<T>` is `accept(T, int)` — not assignable to `BiConsumer<T, Integer>`. `collect`’s accumulator must **mutate** `result`; `accept` is `void` and does not return a new container.

> [!tip] Interview answer
> **`BiConsumer<T,U>` is `void accept(T, U)` — two in, nothing out, side effects, with `andThen` to chain.** It is the two-argument form of `Consumer`, not a subtype. `Map.forEach` and the accumulator/combiner of `Stream.collect` take it; one-arg `Iterable.forEach` does not.
