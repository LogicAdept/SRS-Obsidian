<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Career/Interview/Exercises #Java/Versions/8 #SRS

# How do you print 10 random numbers using `forEach`?

> [!abstract] Short answer
> **`new Random().ints(10).forEach(System.out::println)`.** `Random.ints(10)` (Java 8) is ten pseudorandom `int`s; `forEach` is the terminal print. Same pipeline: `ints().limit(10).forEach(...)`. That is **not** sorted — add `sorted()` only if the question asks for ascending order.

## Ten ints, then a terminal print

`Random.ints(long streamSize)` produces that many values, each as if `nextInt()` (full `int` range, including negatives). `ints()` with no size is **effectively unlimited**. Origin/bound overloads use origin inclusive, bound exclusive. `streamSize < 0` throws `IllegalArgumentException` ([[How do you print 10 random numbers in ascending order with streams]]).

`limit(10)` is a short-circuiting stateful intermediate: it truncates an unlimited `ints()` to ten elements. Negative `maxSize` throws `IllegalArgumentException` ([[What is the Stream limit method for]]). `ints(10)` sizes the source so you do not need `limit`.

`forEach(IntConsumer)` is **terminal**. The pipeline is lazy until that call ([[When does a Java stream pipeline actually start executing]]). Sequential `forEach` follows encounter order (the generator’s order — not numeric order). Parallel `forEach` does **not** promise encounter order; `forEachOrdered` does ([[What is the difference between forEach and forEachOrdered on a stream]]).

`System.out::println` is a valid `IntConsumer`. Nothing is printed until `forEach` runs.

```d2
direction: down
src: "Random.ints(10)\nor ints().limit(10)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
prn: "forEach(System.out::println)\nterminal" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
src -> prn
```

**Fig. 1.** Bound the random `IntStream`, then `forEach`. No `sorted()` unless the cue asks for ascending order.

```java
import java.util.Random;
import java.util.stream.IntStream;

class Demo {
    static void printTen() {
        new Random().ints(10)
            .forEach(System.out::println);
    }

    static void printTenLimited() {
        new Random().ints()
            .limit(10)
            .forEach(System.out::println);
    }

    static IntStream tenInRange() {
        return new Random().ints(10, 0, 100);
    }
}
```

**Listing 1.** `printTen` sizes the source. `printTenLimited` truncates an unlimited stream. `tenInRange` is ten values in `[0, 100)` — still needs a terminal op to print.

> [!warning] `forEach` does not sort
> Encounter order is generation order. `3, 1, 2` prints as `3, 1, 2`. For ascending print, insert `sorted()` **after** the size/`limit` and **before** `forEach` ([[How do you print 10 random numbers in ascending order with streams]]). Parallel `forEach` can scramble even that; use `forEachOrdered` or stay sequential.

> [!warning] Unlimited `ints().forEach` never stops
> `ints()` is effectively `ints(Long.MAX_VALUE)`. Without `limit` or `ints(n)`, `forEach(println)` prints until you kill the process. `limit` after an unbounded `sorted()` is a different hang ([[How do you print 10 random numbers in ascending order with streams]]).

> [!tip] Interview answer
> **`new Random().ints(10).forEach(System.out::println)` — or `ints().limit(10)` then `forEach`.** That prints ten pseudorandom ints, not sorted. Bound the stream or `forEach` never returns; add `sorted()` only when the question wants ascending order.
