<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Versions/8 #SRS

# What is the `collect` terminal operation in Java streams?

> [!abstract] Short answer
> **`collect` is an eager terminal: it starts the pipeline, folds elements into a mutable container, and consumes the stream.** Two overloads: `collect(Collector)` (`Collectors.toList`, `groupingBy`, `joining`, …) or `collect(supplier, accumulator, combiner)`. A `Collector<T,A,R>` packages **supplier** / **accumulator** / **combiner** / **finisher**. Parallel fills **isolated** containers and merges them — no extra lock on an `ArrayList`. Prefer this over `forEach` + `list.add`. Contrast with `reduce` (immutable fold) and `Stream.toList()` (Java 16, unmodifiable).

## Mutable reduction, then the `Collector` protocol

A pipeline does not walk the source until a **terminal** runs. `collect` is that terminal: it produces a result (a `List`, `Map`, `String`, summary, …) and afterward the pipeline is **consumed** ([[What terminal stream operations do you know in Java]], [[When does a Java stream pipeline actually start executing]]). Intermediates before it (`filter`, `map`, `sorted`) stay lazy until this call.

Package doc: `collect` is **mutable reduction** — update a container in place, unlike `reduce` which replaces the result (`String::concat` is O(n²) for a big join). Three functions: **supplier** (new box), **accumulator** (fold one element in), **combiner** (merge two boxes for parallel). The three-arg form is:

```text
stream.collect(ArrayList::new, ArrayList::add, ArrayList::addAll)
```

`Collector<T,A,R>` packages those plus a **finisher** (`A` → `R`).

| Function | Role |
| --- | --- |
| `supplier()` | New empty `A` |
| `accumulator()` | Fold one `T` into `A` |
| `combiner()` | Merge two partial `A`s (parallel splits) — `BinaryOperator<A>`, **must return** a container |
| `finisher()` | `A` → `R` after accumulation |

If `IDENTITY_FINISH` is set, the finisher is treated as an unchecked cast `A` → `R`. `Collector.of(supplier, accumulator, combiner, characteristics...)` **sets** `IDENTITY_FINISH`. Sequential: one container, then finisher. Parallel: one container per partition, combiner, then finisher. Identity: `combiner.apply(a, supplier.get())` must be equivalent to `a`.

`Stream.collect(Collector)` JavaDoc: if the stream is parallel, the collector is `CONCURRENT`, and the stream or collector is unordered, a **concurrent** reduction may share one container. Otherwise partial results stay isolated, so a non-thread-safe `ArrayList` still needs no extra synchronization. Combining maps (`groupingBy` on a large parallel ordered stream) can be expensive; `groupingByConcurrent` drops encounter order.

`Stream.toList()` (Java 16) is a different terminal: unmodifiable list. `Collectors.toList()` does **not** promise mutability or concrete type — use `toCollection(Supplier)` or `toUnmodifiableList()` when you care.

`Collectors` factories worth reciting: `toList` / `toSet` / `toCollection`; `toMap` / `toConcurrentMap` (two-arg `toMap` throws `IllegalStateException` on duplicate keys — pass a merge function); `groupingBy` / `groupingByConcurrent`; `partitioningBy(Predicate)` → `Map<Boolean, List<T>>` that **always** has both `true` and `false` keys; `joining`; `mapping(mapper, downstream)`; `summing*` / `averaging*` / `summarizing*`. Empty `averagingInt` is `0.0`, not an `Optional`. Empty `summing*` is `0`.

```d2
direction: down
pipe: "lazy intermediates" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
col: "collect (terminal, eager)" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
done: "pipeline consumed" {
  width: 180
  height: 40
  style.fill: "#fce4ec"
}
pipe -> col
col -> done
```

**Fig. 1.** `collect` is what actually runs the stream and then retires it. Parallel paths use combiner; `IDENTITY_FINISH` skips a real finisher.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collector;
import java.util.stream.Collectors;

class Demo {
    static Map<Integer, List<String>> byLength(List<String> words) {
        return words.stream()
            .filter(s -> !s.isEmpty())
            .collect(Collectors.groupingBy(String::length));
    }

    static Collector<String, List<String>, List<String>> toArrayList() {
        return Collector.of(
            ArrayList::new,
            List::add,
            (left, right) -> {
                left.addAll(right);
                return left;
            }
        );
    }
}
```

**Listing 1.** `filter` does nothing until `collect`. `groupingBy` is a `Collector`; the result is a `Map`. Three-arg `Collector.of` has `IDENTITY_FINISH`; the combiner **returns** `left`. A second terminal on the same stream is illegal.

> [!warning] One terminal per pipeline — and `forEach` is not `collect`
> `stream.filter(...).map(...)` with no `collect` (or other terminal) does **zero** work. Adding to a shared `ArrayList` from `forEach` is a data race when parallel and unnecessary when sequential. `Collectors.toList()` may return a mutable list of unspecified class; `Stream.toList()` is unmodifiable. Empty `Collectors.averagingInt` is `0`, not an `Optional`. Two-arg `toMap` throws `IllegalStateException` on duplicate keys.

> [!tip] Interview answer
> **`collect` is the eager terminal for mutable reduction: `Collector` in, collection or summary out, stream consumed.** Name `Collectors.toList` / `groupingBy` / `joining`, supplier–accumulator–combiner–finisher, and “don’t `forEach`-add.” Custom collectors: `Collector.of`, combiner **returns** the merged box. Contrast with `reduce` (immutable fold) and `Stream.toList()` (Java 16, unmodifiable).
