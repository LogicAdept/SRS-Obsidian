<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# How would you explain for what needed functional interface ObjDoubleConsumerT ObjIntConsumerT and ObjLongConsu

> [!abstract] Short answer
> **They are Java 8 two-in, void-out side-effect operators with one primitive argument.** Each SAM is `void accept(T, primitive)`. `ObjIntConsumer` / `ObjLongConsumer` / `ObjDoubleConsumer` are the `(reference, int)` / `(reference, long)` / `(reference, double)` specializations of `BiConsumer`, not `Integer` / `Long` / `Double`. Use them when you have an object plus an unboxed number and you only want a side effect.

## Object plus primitive, no result

Each of these types (`@since 1.8`) is a `@FunctionalInterface` for an operation that accepts an object-valued argument and a primitive, and returns **no result**. Unlike most `java.util.function` types, they are **expected to operate via side-effects**. They do **not** extend `BiConsumer` or `Consumer`. The only method is `accept` — there is no `andThen` ([[What is functional interface]], [[How would you explain ObjDoubleConsumer ObjIntConsumer and ObjLongConsumer]], [[How would you explain the BiConsumer functional interface]]).

| Type | SAM | Second argument |
| --- | --- | --- |
| `ObjIntConsumer<T>` | `accept(T, int)` | `int` |
| `ObjLongConsumer<T>` | `accept(T, long)` | `long` |
| `ObjDoubleConsumer<T>` | `accept(T, double)` | `double` |

`Consumer<T>` is one object and no result. `BiConsumer<T,U>` is two objects. These three sit in the gap: keep `T` as a reference, keep the number unboxed ([[How would you explain for what needed functional interface ConsumerT DoubleConsumer IntConsumer and LongConsum]]). `IntConsumer` is the one-argument primitive cousin (`accept(int)` only).

```d2
direction: down
bi: "BiConsumer<T,U>\naccept(T, U) → void" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
obj: "ObjInt/Long/DoubleConsumer<T>\naccept(T, primitive) → void" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
cons: "Consumer / IntConsumer\none argument" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}

bi -> obj: "specialization, not a subtype"
bi -> cons: "one vs two arguments"
```

**Fig. 1.** Same “do something, return nothing” shape. The `Obj*` types unbox only the **second** argument.

```java
import java.util.function.ObjDoubleConsumer;
import java.util.function.ObjIntConsumer;
import java.util.function.ObjLongConsumer;

class Demo {
    static void mixed() {
        ObjIntConsumer<String> ints = (label, n) -> System.out.println(label + "=" + n);
        ObjLongConsumer<String> longs = (label, n) -> System.out.println(label + "=" + n);
        ObjDoubleConsumer<String> doubles = (label, n) -> System.out.println(label + "=" + n);
        ints.accept("count", 3);
        longs.accept("nanos", 1L);
        doubles.accept("ratio", 0.5);
    }
}
```

**Listing 1.** `accept` takes `T` then a primitive. A `BiConsumer<String,Integer>` would box the number. None of these interfaces chain with `andThen`.

> [!warning] The second argument is not a wrapper
> Dump text that says `ObjIntConsumer` “takes `Integer`” is wrong: the SAM is `accept(T, int)`. You cannot pass an `ObjIntConsumer` where `BiConsumer<T,Integer>` is required. There is no `andThen` on these types — `Consumer` and `BiConsumer` are the ones that compose.

> [!tip] Interview answer
> **`ObjIntConsumer<T>` is `void accept(T, int)` — object plus `int`, side effect, no result.** `ObjLongConsumer` and `ObjDoubleConsumer` match `long` and `double`. They exist so you do not box the primitive into `BiConsumer<T,Integer>`. One argument only is `Consumer` / `IntConsumer`.
