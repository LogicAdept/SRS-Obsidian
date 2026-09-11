<!--
reps: 0
priority: 0
-->
#Java/Versions/24 #SRS

# What are stream gatherers

> [!abstract] Short answer
> **Stream gatherers (JEP 485, final in Java 24; previewed in 22/23 as 461/473) are the general API for custom intermediate operations: `stream.gather(Gatherer)` sits between `map`/`filter` one-to-one and `flatMap` one-to-many, supporting one-to-many, many-to-one, and many-to-many shapes, with optional state and a finisher. The library ships built-ins: `Gatherers.windowFixed`, `windowSliding`, `mapConcurrent`, `scan`, and `fold`.**

## Why map and collect were not enough

Before gatherers, a stateful intermediate op — sliding windows, running differences, rate limiting, batching — had to be smuggled through `collect` (which is terminal) or a custom `Spliterator`. `Gatherer<T, A, R>` fixes that with four parts: an initializer for state, an integrator that receives each element and may emit downstream, a combiner for parallel runs, and a finisher for end-of-stream emission. `Gatherers.windowFixed(n)` chunks into consecutive groups; `windowSliding(n)` keeps overlapping windows; `mapConcurrent(n)` runs a mapper across virtual threads with bounded concurrency — the Loom tie-in ([[How would you explain Virtual Threads]]); `scan` is a stateful running transform; `fold` reduces while streaming.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collector;
import java.util.stream.Stream;

public class V44_Gatherers {
    // Emulates Gatherers.windowFixed(3) - final in JDK 24 (JEP 485) - on JDK 21.
    // JDK 24 form: Stream.of(...).gather(Gatherers.windowFixed(3)).toList();
    static <T> Collector<T, List<List<T>>, List<List<T>>> windowFixed(int size) {
        return Collector.of(ArrayList::new,
                (acc, item) -> {
                    if (acc.isEmpty() || acc.get(acc.size() - 1).size() == size) {
                        acc.add(new ArrayList<>());
                    }
                    acc.get(acc.size() - 1).add(item);
                },
                (a, b) -> a, List::copyOf);
    }

    public static void main(String[] args) {
        System.out.println(Stream.of(1, 2, 3, 4, 5, 6, 7).collect(windowFixed(3)));
    }
}
```

**Listing 1.** Verified on JDK 21 (V44_Gatherers in empirics): `[[1, 2, 3], [4, 5, 6], [7]]` (out/V44_Gatherers.txt) — the collector emulation works but is terminal; the 24 `gather` form expresses the same shape as a true intermediate op.

```d2
direction: right
src: "source\nT..." { width: 120; height: 70 }
g: "gather(Gatherer<T,A,R>)\nstate + integrator +\ncombiner + finisher" { style.fill: "#e3f2fd"; width: 300; height: 100 }
sink: "downstream\nR..." { width: 130; height: 70 }
src -> g -> sink: ""
```

**Fig. 1.** `gather` as the general intermediate stage: elements flow in with shared state, transformed results flow out, and a finisher runs at the end of the stream.

> [!warning] The API does not exist on JDK 21
> `Stream.gather` and `java.util.stream.Gatherers` are Java 24 — on 21 the code does not compile, preview flag or not (461 previewed on 22, not 21). Interview claims like "we used gatherers on our Java 17 service" are impossible; the honest 21-era equivalent is a custom `Collector` — which changes the stream shape, because `collect` is terminal ([[What Stream API methods arrived after Java 8]]).

> [!tip] Interview answer
> **Gatherers are the Java 24 API for custom intermediate stream operations — Stream.gather takes a Gatherer with state, integrator, combiner, and finisher, covering windowing, sliding, scanning, and concurrent mapping without abusing collect. Built-ins include windowFixed, windowSliding, mapConcurrent, scan, and fold; the API previewed in 22/23 and finalized in 24.**
