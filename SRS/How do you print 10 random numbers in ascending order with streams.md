<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Career/Interview/Exercises #Java/Versions/8 #SRS

# How do you print 10 random numbers in ascending order with streams?

> [!abstract] Short answer
> **`new Random().ints(10).sorted().forEach(System.out::println)`.** `Random.ints(10)` (Java 8) is a stream of ten pseudorandom `int`s; `sorted()` is a stateful intermediate sort; `forEach` prints. Equivalent: `ints().limit(10).sorted()…`. Limit **before** you sort — an unlimited `ints().sorted()` never finishes.

## Ten ints, then sort, then print

`Random.ints(long streamSize)` produces that many values, each as if `nextInt()`. `ints()` with no size is **effectively unlimited** (documented as `ints(Long.MAX_VALUE)`). Origin/bound overloads use origin inclusive, bound exclusive. `streamSize < 0` throws `IllegalArgumentException` ([[How do you print 10 random numbers using forEach]]).

`IntStream.sorted()` returns the elements in sorted numeric order. It is a **stateful intermediate** operation: it buffers, then emits in order ([[What is the Stream sorted method for]]). `limit(maxSize)` is a **short-circuiting** stateful intermediate; negative `maxSize` throws `IllegalArgumentException` ([[What is the Stream limit method for]]).

Nothing runs until a **terminal** op ([[When does a Java stream pipeline actually start executing]]). Sequential `forEach` prints in encounter order after `sorted()`. Parallel `forEach` does **not** promise encounter order — use `forEachOrdered` if the pipeline is parallel ([[What is the difference between forEach and forEachOrdered on a stream]]).

```d2
direction: down
src: "Random.ints(10)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
sort: "sorted()\nstateful" {
  width: 220
  height: 50
  style.fill: "#fff8e1"
}
prn: "forEach(println)\nterminal" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
bad: "ints().sorted()\nunlimited — never ends" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
src -> sort
sort -> prn
```

**Fig. 1.** Size (or `limit`) first, then `sorted`, then print. Sorting an unlimited `ints()` stream does not short-circuit.

```java
import java.util.Random;
import java.util.stream.IntStream;

class Demo {
    static void printTenAscending() {
        new Random().ints(10)
            .sorted()
            .forEach(System.out::println);
    }

    static void printTenAscendingLimited() {
        new Random().ints()
            .limit(10)
            .sorted()
            .forEach(System.out::println);
    }

    static IntStream tenInRange() {
        return new Random().ints(10, 0, 100).sorted();
    }
}
```

**Listing 1.** `ints(10)` sizes the source. `ints().limit(10)` truncates an unlimited stream, then sorts. `ints(10, 0, 100)` is ten values in `[0, 100)`.

> [!warning] `ints().sorted().limit(10)` does not mean “ten smallest random ints”
> `ints()` is unlimited. `sorted()` is stateful and waits for the whole stream. Putting `limit` **after** `sorted` on that source does not short-circuit the sort — it hangs or blows memory. Size with `ints(10)` or `limit(10)` **before** `sorted()`.

> [!warning] Parallel `forEach` can scramble the sort
> `sorted()` defines encounter order. Parallel `forEach` is allowed to ignore that order. Print with `forEachOrdered`, or keep the pipeline sequential. `limit` on an **ordered parallel** stream is also expensive: it must take the first `n` in encounter order.

> [!tip] Interview answer
> **`new Random().ints(10).sorted().forEach(System.out::println)` — or `ints().limit(10)` then `sorted`.** You must bound the stream before sorting, because unlimited `ints().sorted()` never completes. Use `forEachOrdered` if you go parallel, or you can print out of sorted order.
