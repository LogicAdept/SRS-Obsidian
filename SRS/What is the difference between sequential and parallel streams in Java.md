<!--
reps: 0
priority: 0
-->
#Java/Streams/Parallel #Java/Parallelism #Java/Versions/8 #SRS

# What is the difference between sequential and parallel streams in Java?

> [!abstract] Short answer
> **Same pipeline, different execution mode.** JDK streams are **sequential unless you opt in** (`Collection.stream()` vs `parallelStream()`, or `.parallel()`). The **latest** `sequential()` / `parallel()` before the **terminal** applies to the **whole** pipeline. Results should match except for explicitly nondeterministic ops (`findAny`, `forEach`). Parallel splits a `Spliterator` onto fork-join workers (common pool by default). `parallelStream()` is only **possibly** parallel.

## Mode flag, not a second API

All stream operations can run serial or parallel. JDK factories create **serial** streams unless parallelism is requested. `Collection.stream()` is sequential; `parallelStream()` is the parallel twin (the contract still **allows** a sequential stream). `IntStream.range` is sequential until `.parallel()`. `isParallel()` queries the flag ([[How would you explain parallel streams in Java]], [[What is Stream]]).

Package doc: the serial vs parallel widgets example differs **only** in `stream()` vs `parallelStream()`. Execution mode is the mode of the stream **on which the terminal is invoked**. `sequential()` / `parallel()` may appear mid-pipeline; the **most recent** setting wins for the entire pipeline.

Except for ops identified as explicitly nondeterministic (`findAny()`; `forEach` on parallel pipelines), sequential vs parallel **should not change the result**. Encounter-order **results** (for example `map` then `toArray` on an ordered source) stay ordered; **when** the mapper runs, and **which thread**, is not ordered ([[What is the difference between forEach and forEachOrdered on a stream]]).

Under the hood, parallel means `trySplit` and fork-join tasks, not a faster `for` loop. Poor splits (iterator-backed lists) and ordered `limit` / `distinct` can erase the speedup. Lambdas must stay non-interfering and stateless — that rule applies to **both** modes, but races show up in parallel ([[What backs Java parallelStream under the hood]], [[Does the Java Stream API optimize for lists that implement RandomAccess]]).

```d2
direction: down
seq: "stream() / sequential()\none thread, encounter order easy" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
par: "parallelStream() / parallel()\nsplit Spliterator, common pool" {
  width: 320
  height: 55
  style.fill: "#fff8e1"
}
```

**Fig. 1.** Sequential vs parallel is a property of the stream at the terminal, not a different set of operators.

```java
import java.util.List;

class Demo {
    static int seq(List<Widget> widgets) {
        return widgets.stream()
            .filter(w -> w.color() == Color.RED)
            .mapToInt(Widget::weight)
            .sum();
    }

    static int par(List<Widget> widgets) {
        return widgets.parallelStream()
            .filter(w -> w.color() == Color.RED)
            .mapToInt(Widget::weight)
            .sum();
    }
}
```

**Listing 1.** Package-summary pair: identical pipeline; only the source mode changes. `sum` is associative, so both should agree.

> [!warning] Parallel is not “always faster,” and `forEach` is not ordered
> Tiny lists and ordered `limit` often lose to sequential. Blocking I/O in `map` contends for the **common pool**. `parallelStream()` may still be sequential. `forEach` on a parallel ordered `List` may print out of order — use `forEachOrdered` or `collect`. Shared `ArrayList.add` in a lambda is a data race.

> [!tip] Interview answer
> **Sequential is the default; parallel is the same lazy pipeline with a parallel flag at the terminal.** Results match except `findAny` / parallel `forEach`. Underneath: `Spliterator` + fork-join, not a magic faster loop. Opt in only when the work is CPU-heavy, associative, and the source splits well.
