<!--
reps: 0
priority: 0
-->
#Java/Versions/9 #SRS

# What Stream API methods arrived after Java 8

> [!abstract] Short answer
> **Java 9 added `takeWhile`, `dropWhile`, the three-argument `iterate` with a predicate, `ofNullable`, and `Collectors.flatMapping`/`filtering`; Java 16 added `Stream.toList()` and `mapMulti`; Java 24 added `Stream.gather` with the Gatherers library (461/473/485). Everything else on a stream today was already there in 8.**

## The gaps each release closed

Java 9's `takeWhile`/`dropWhile` give ordered-prefix semantics — on unordered sources the result is nondeterministic by design. Three-arg `iterate(seed, hasNext, next)` turns infinite generators into bounded ones without `.limit()`. `ofNullable(t)` flattens the null-or-value case into a zero-or-one stream. The collector additions (`flatMapping`, `filtering`) matter inside grouping: `groupingBy(f, flatMapping(...))` aggregates nested collections where 8 forced a collect-then-flatten round trip. Java 16's `toList()` is the terminal-op shortcut — unmodifiable, unlike `Collectors.toList()` — and `mapMulti` replaces flatMap when the downstream would allocate a stream per element: you push zero or more results into the consumer directly. Java 24's `gather` is the general intermediate-operation escape hatch ([[What are stream gatherers]]).

```java
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class V43_StreamAdditions {
    public static void main(String[] args) {
        System.out.println("takeWhile: " + Stream.of(2, 4, 5, 6).takeWhile(n -> n % 2 == 0).toList()); // 9
        System.out.println("dropWhile: " + Stream.of(2, 4, 5, 6).dropWhile(n -> n % 2 == 0).toList()); // 9
        System.out.println("iterate: " + Stream.iterate(1, n -> n < 20, n -> n * 3).toList());         // 9
        System.out.println("ofNullable: " + Stream.ofNullable(null).count());                          // 9
        System.out.println("mapMulti: " + Stream.of(1, 2)
                .<Integer>mapMulti((n, down) -> { down.accept(n); down.accept(n * 10); })
                .toList());                                                                            // 16
        System.out.println("toList: " + Stream.of("a").toList());                                      // 16
        System.out.println("filtering: " + Stream.of(1, 2, 3, 4).collect(Collectors.partitioningBy(
                n -> n % 2 == 0, Collectors.filtering(n -> n > 2, Collectors.toList()))));             // 9
    }
}
```

**Listing 1.** Verified on JDK 21 (V43_StreamAdditions in empirics): `takeWhile: [2, 4]`, `dropWhile: [5, 6]`, `iterate: [1, 3, 9]`, `ofNullable: 0`, `mapMulti: [1, 10, 2, 20]`, `toList: [a]`, `filtering: {false=[3], true=[4]}` (out/V43_StreamAdditions.txt).

```d2
direction: right
j9: "Java 9\ntakeWhile, dropWhile, iterate(3),\nofNullable, flatMapping/filtering" { style.fill: "#e8f5e9"; width: 320; height: 100 }
j16: "Java 16\ntoList(), mapMulti" { style.fill: "#e3f2fd"; width: 210; height: 100 }
j24: "Java 24\nStream.gather + Gatherers" { style.fill: "#fff3e0"; width: 250; height: 100 }
j9 -> j16 -> j24: ""
```

**Fig. 1.** Stream API growth: prefix ops and collector composition in 9, terminal and fan-out helpers in 16, the general gather API in 24.

> [!warning] `takeWhile`/`dropWhile` assume encounter order
> On an unordered stream (HashSet source, parallel stream) which elements are kept or dropped is not defined — using them for "filter with a boundary" semantics on unordered data is a correctness bug waiting for a data-shape change. And `toList()` (16) is unmodifiable: callers who sort or add will throw ([[What Stream API methods arrived after Java 8]] sibling fact: `Collectors.toList()` stays mutable).

> [!tip] Interview answer
> **Stream after 8 grew in three waves: Java 9 added takeWhile, dropWhile, bounded iterate, ofNullable, and the flatMapping/filtering collectors; 16 added the unmodifiable toList() and cheap mapMulti; 24 added Stream.gather as the general custom-intermediate-op API. I mention that takeWhile/dropWhile are order-dependent and toList is intentionally unmodifiable.**
