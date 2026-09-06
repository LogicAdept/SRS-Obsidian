<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Language/Primitives #Java/Versions/8 #SRS

# How would you explain ObjDoubleConsumer ObjIntConsumer and ObjLongConsumer?

> [!abstract] Short answer
> **Two arguments, void result, side effects: a reference plus one primitive.** `ObjIntConsumer<T>` is `void accept(T t, int value)` — the `(reference, int)` specialization of `BiConsumer`. `ObjLongConsumer` / `ObjDoubleConsumer` match that for `long` / `double`. They do **not** extend `BiConsumer` or `Consumer`, and they have **no** `andThen`. Java 8. Primitive streams use them as `collect` accumulators: fold an `int` into a mutable container.

## `Obj` then a primitive, not two objects

`ObjIntConsumer<T>` “represents an operation that accepts an object-valued and a `int`-valued argument, and returns no result.” Like other consumers, it is **expected to operate via side-effects**. The SAM is `accept(Object, int)` — in source, `accept(T t, int value)`. Same text for `ObjLongConsumer` (`accept(T, long)`) and `ObjDoubleConsumer` (`accept(T, double)`).

The `Obj` prefix is the package naming rule: leave the **first** type parameter as a reference and specialize the **next** one. Because both arguments already have a prefix (`Obj` + `Int`), the arity prefix `Bi` is omitted. These are **not** `BiConsumer<T, Integer>` and **not** `IntConsumer` ([[How would you explain core functional interfaces in java.util.function]], [[How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer]], [[How would you explain the BiConsumer functional interface]]).

```d2
direction: down
bi: "BiConsumer<T,U>\naccept(T, U)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
obj: "ObjIntConsumer<T>\naccept(T, int)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
use: "IntStream.collect\naccumulator.accept(container, element)" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
bi -> obj: "docs: (reference, int)\nspecialization, not a subtype"
obj -> use
```

**Fig. 1.** Second argument is a primitive, first is the object you mutate. `IntStream.collect` calls `accumulator.accept(result, element)` ([[What is functional interface]]).

Method summary is **only** `accept` — no default `andThen` (unlike `Consumer` / `IntConsumer`). No superinterfaces: you cannot assign an `ObjIntConsumer<List<Integer>>` to `BiConsumer<List<Integer>, Integer>`.

Call site: `IntStream.collect(Supplier, ObjIntConsumer, BiConsumer)` is a mutable reduction. Equivalent sequential loop: `R result = supplier.get(); for (int element : stream) accumulator.accept(result, element);`. The accumulator must **fold** the `int` into the container (side effect on `result`). For parallel use the supplier must return a **fresh** container each call; the combiner merges two containers. `ObjLongConsumer` / `ObjDoubleConsumer` are the same two-arg side-effect shape for `long` / `double`.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.ObjIntConsumer;
import java.util.stream.IntStream;

class Demo {
    static void foldIntoList() {
        ObjIntConsumer<List<Integer>> acc = (list, i) -> list.add(i);
        List<Integer> box = new ArrayList<Integer>();
        acc.accept(box, 3);

        List<Integer> collected = IntStream.of(1, 2, 3)
                .collect(ArrayList::new, (list, i) -> list.add(i), ArrayList::addAll);
        // BiConsumer<List<Integer>, Integer> no = acc; // does not compile
        // acc.andThen(acc); // ObjIntConsumer has no andThen
    }
}
```

**Listing 1.** `accept` mutates the list. `collect` is the documented loop: supplier, then `accept(result, element)` per `int`, then combiner. There is no `IntObjConsumer` (primitive first, object second) in this trio.

> [!warning] Specialization is documentation, not subtyping
> `ObjIntConsumer<T>` is not a `BiConsumer<T, Integer>` and not an `IntConsumer`. `Stream<Integer>.collect` does not take `ObjIntConsumer`; `IntStream.collect` does. Boxing the second argument into `BiConsumer<T, Integer>` is a different SAM (`accept(T, Integer)`), with `Integer` not `int`.

> [!warning] The accumulator must mutate the container
> `collect` is not `reduce`: you update `result`, you do not return a new `R` from `accept` (`accept` is `void`). A supplier that returns the same instance on every call breaks parallel collect (the spec requires a fresh value each time). There is no `andThen` to chain two object-plus-primitive consumers — compose by calling `accept` twice yourself.

> [!tip] Interview answer
> **`ObjIntConsumer<T>` is `void accept(T, int)` — object plus primitive, side effects, no `andThen`.** `ObjLong` / `ObjDouble` are the `long` / `double` twins. `Obj` means “do not specialize the first parameter”; they are named as `BiConsumer` specializations but are separate types. Primitive `collect` uses them to fold each element into a mutable container.
