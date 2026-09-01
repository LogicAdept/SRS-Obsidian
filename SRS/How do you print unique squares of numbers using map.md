<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Career/Interview/Exercises #Java/Versions/8 #SRS

# How do you print unique squares of numbers using `map`?

> [!abstract] Short answer
> **`map` (or `mapToInt`) to square, then `distinct()`, then `forEach` to print.** Example: `numbers.stream().map(n -> n * n).distinct().forEach(System.out::println)`. `distinct` uses `equals` (or `int` value on `IntStream`). Square **before** you unique — otherwise `-3` and `3` both survive and both print `9`.

## Map squares, then drop duplicate results

`Stream.map(Function)` is an intermediate op: each element becomes the function result. The mapper must be non-interfering and stateless ([[What are map and mapToInt for in Java streams]], [[Which functional interface does Stream map use]], [[What is the difference between Stream map and flatMap]]). `n -> n * n` on `Stream<Integer>` unboxes, multiplies, and boxes the square.

`distinct()` is a **stateful intermediate** op. On `Stream`, distinct means `Object.equals`. For ordered streams it is **stable** (first encounter of a duplicate wins). On `IntStream`, `map(IntUnaryOperator)` then `distinct()` compares the `int` values ([[What are map and mapToInt for in Java streams]]).

Print with terminal `forEach` ([[How do you print 10 random numbers using forEach]]). Nothing runs until that terminal starts.

Order of intermediates is the whole point: `map` then `distinct` uniques **squares**. `distinct` then `map` uniques **inputs**, so `3` and `-3` both stay and both square to `9`.

```d2
direction: down
src: "numbers\n3, -3, 3, 2" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
map: "map(n -> n * n)\n9, 9, 9, 4" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
uniq: "distinct()\n9, 4" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
prn: "forEach(println)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
src -> map
map -> uniq
uniq -> prn
```

**Fig. 1.** Square first, then `distinct`. Unique inputs would still produce two nines from `3` and `-3`.

```java
import java.util.List;
import java.util.stream.IntStream;

class Demo {
    static void printUniqueSquares(List<Integer> numbers) {
        numbers.stream()
            .map(n -> n * n)
            .distinct()
            .forEach(System.out::println);
    }

    static void printUniqueSquares(int[] numbers) {
        IntStream.of(numbers)
            .map(n -> n * n)
            .distinct()
            .forEach(System.out::println);
    }

    static void demo() {
        printUniqueSquares(List.of(3, -3, 3, 2)); // 9 then 4
    }
}
```

**Listing 1.** Boxed `map` vs `IntStream.map`. `List.of(3, -3, 3, 2)` prints `9` and `4` (stable: first `9` kept). Distinct-then-map on the same list would print `9`, `9`, `4`.

> [!warning] `distinct()` before `map` does not unique squares
> Unique **sources** are not unique **squares**. `-3` and `3` are distinct integers; both square to `9`. Put `map` first when the cue is unique squares. `equals` on boxed `Integer` after `map` is value equality for typical range; `IntStream.distinct` compares `int`s and skips boxing. `map` itself does not print — `forEach` is the terminal.

> [!warning] Parallel `distinct` is a full barrier
> Stability on an ordered parallel `distinct` is expensive (buffering). If encounter order of first-wins does not matter, `unordered()` can be cheaper. Parallel `forEach` can also print the unique squares out of encounter order — use `forEachOrdered` or stay sequential.

> [!tip] Interview answer
> **`stream.map(n -> n * n).distinct().forEach(System.out::println)` — or `mapToInt` / `IntStream.map` then `distinct`.** You square first so `-3` and `3` collapse to one `9`. `distinct` then `map` is a different question: unique numbers, not unique squares.
