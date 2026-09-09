<!--
reps: 0
priority: 0
-->
#Java/Generics/TypeBounds #SRS

# How would you explain the PECS rule for generic method signatures

> [!abstract] Short answer
> PECS — Producer Extends, Consumer Super — is the API-design rule for wildcard parameters: if a parameter produces `T` values your code reads, declare it `? extends T`; if it consumes `T` values your code writes, declare it `? super T`. It maximizes the set of argument types callers may pass without breaking type safety.

The rule answers a design question, not a correctness question: a signature with exact types compiles too, but rejects callers it could accept. `Collections.copy` would be useless as `copy(List<T>, List<T>)`; the actual signature `copy(List<? super T> dest, List<? extends T> src)` lets you copy from a `List<Integer>` into a `List<Number>`.

## Reading JDK signatures through PECS

Producers sit behind `extends`: `Collections.max(Collection<? extends T>)` only reads elements out. Consumers sit behind `super`: `Collections.addAll(Collection<? super T> c, T... elements)` only writes elements in. Two-sided APIs split the roles between parameters — `copy` names its sides `dest` and `src` exactly because each gets its own variance. The stream API applies the same template everywhere: `map(Function<? super T, ? extends R>)` consumes `T` from the pipeline and produces `R`, the same shape that [[What is the difference between Stream map and flatMap]] and [[What is the collect terminal operation in Java streams]] hide behind their parameter types.

```d2
direction: right
src: "src: List<? extends T>\nProducer" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
body: "Method body\nreads T from src\nwrites T to dst" {
  width: 280
  height: 110
  style.fill: "#e3f2fd"
}
dst: "dst: List<? super T>\nConsumer" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
caller: "Caller freedom:\nsrc = List<Integer>\ndst = List<Number> or List<Object>" {
  width: 340
  height: 110
  style.fill: "#ffebee"
}
src -> body: T flows out
body -> dst: T flows in
caller -> src
caller <- dst: accepts any supertype
```

**Fig. 1.** `T` flows from the `extends` parameter through the body into the `super` parameter; both directions stay safe for every caller.

## Applying the rule to your own API

Write the mechanics once with wildcards in the signature; callers then mix concrete types freely:

```java
import java.util.ArrayList;
import java.util.List;

public class PecsDemo {

    // Same shape as Collections.copy(List<? super T>, List<? extends T>):
    static <T> void copyAll(List<? super T> dst, List<? extends T> src) {
        for (T item : src) dst.add(item);
    }

    public static void main(String[] args) {
        List<Integer> ints = new ArrayList<>(List.of(1, 2, 3));
        List<Number> nums = new ArrayList<>();
        List<Object> objs = new ArrayList<>();

        copyAll(nums, ints); // src produces T=Integer, dst consumes it
        copyAll(objs, nums); // also valid: Object is a supertype of Number
        System.out.println(nums); // [1, 2, 3]

        // Reverse direction is rejected: producer and consumer swapped
        // copyAll(ints, nums); // compile-time error: List<Number> is not ? extends Integer

        // Real JDK signatures that follow PECS:
        // Collections.copy(List<? super T>, List<? extends T>)
        // Collections.addAll(Collection<? super T>, T... elements)
        // Collections.max(Collection<? extends T>) — source only, reads elements
    }
}
```

**Listing 1.** One PECS signature covers `Integer → Number`, `Number → Object`, and every other legal pairing.

## When no wildcard fits

A parameter used both ways — read and written, like a swap helper — cannot be a wildcard: inside the body the compiler knows nothing beyond "some unknown type", so neither direction is provable. Use the exact type `T` (or an unbounded `?` plus a private capture helper) there. Parameters of type `T` that feed a consumer chain keep narrowing toward `super` as they descend the API, which is why recursive bound forms such as `Comparable<? super T>` appear in [[What is the purpose of type bounds in Java generics]].

> [!warning] PECS is about signatures, not performance or element types
> The rule does not make code faster and does not choose the element type of your collections — it widens parameter types so more caller combinations compile. Writing `? extends T` on a parameter you also modify is the misuse it exists to prevent: the body then fails to compile on its own writes, and the fix is to split the parameter by role, not to sprinkle casts.

> [!tip] Interview answer
> PECS tells you which wildcard a parameter needs: a producer you read from takes `? extends T`, a consumer you write into takes `? super T`. The JDK follows it everywhere — `Collections.copy(List<? super T>, List<? extends T>)`, `max(Collection<? extends T>)`, `Function<? super T, ? extends R>` in streams. A parameter both read and written stays a plain `T`. It is a flexibility rule for API design: exact types compile, but wildcards let more callers pass their collections unchanged.

