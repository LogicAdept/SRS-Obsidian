<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Versions/8 #SRS

# What terminal stream operations do you know in Java?

> [!abstract] Short answer
> **Terminals start the pipeline, produce a result or a side-effect, and consume the stream.** On `Stream`: `forEach` / `forEachOrdered`, `toArray`, `reduce`, `collect` / `toList()` (Java 16), `min` / `max` / `count`, short-circuiting `anyMatch` / `allMatch` / `noneMatch` / `findFirst` / `findAny`. Escape hatches (not eager): `iterator()`, `spliterator()`. Primitive streams add `sum`, `average`, `summaryStatistics`. One terminal per pipeline.

## The ops that actually run the stream

A pipeline is source + lazy intermediates + **one** terminal. Traversal starts here; afterward get a **new** stream from the source ([[What kinds of stream operations exist in Java]], [[When does a Java stream pipeline actually start executing]]). Almost all terminals are **eager**; only `iterator()` and `spliterator()` are not.

`Stream` terminals (Java 8 unless noted), as labeled in Java SE 21:

| Role | Methods |
| --- | --- |
| Per-element side-effect | `forEach`, `forEachOrdered` — parallel `forEach` ignores encounter order ([[What is the difference between forEach and forEachOrdered on a stream]]) |
| Materialize | `toArray`, `toArray(generator)`, `collect`, `toList()` (16, unmodifiable) ([[What is the collect terminal operation in Java streams]]) |
| Reduce | `reduce` (identity / `Optional` / 3-arg), `min`, `max`, `count` |
| Short-circuit | `anyMatch`, `allMatch`, `noneMatch`, `findFirst`, `findAny` |
| Escape hatch | `iterator()`, `spliterator()` — not eager ([[Does the Stream API use an Iterator internally]]) |

Empty-stream notes worth reciting: `allMatch` / `noneMatch` → `true`; `anyMatch` → `false`; `findFirst` / `findAny` / `min` / `max` → empty `Optional`; `count` → `0`; `reduce` without identity → empty `Optional`. `count()` may skip `peek` if it can take the size from the source.

`IntStream` / `LongStream` / `DoubleStream`: `sum()` (empty → `0`), `average()` (`OptionalDouble`), `summaryStatistics()`, primitive `min`/`max` ([[How do you sum numbers in a stream]], [[How do you get the average of numbers in a stream]], [[How do you find the maximum number in a stream]]).

```d2
direction: down
t: "terminal" {
  width: 140
  height: 35
  style.fill: "#e3f2fd"
}
e: "eager\nforEach collect reduce count\nmin max toArray toList" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
s: "short-circuit\n*Match find*" {
  width: 220
  height: 55
  style.fill: "#fff8e1"
}
x: "not eager\niterator spliterator" {
  width: 240
  height: 55
  style.fill: "#fce4ec"
}
t -> e
t -> s
t -> x
```

**Fig. 1.** Interview split: eager vs short-circuit vs escape hatch.

```java
import java.util.List;
import java.util.Optional;

class Demo {
    static Optional<String> firstLong(List<String> words) {
        return words.stream()
            .filter(s -> s.length() > 3)
            .findFirst();
    }
}
```

**Listing 1.** `findFirst` is a short-circuiting terminal: it may stop before the end of `words`. `filter` has not run until this call.

> [!warning] Name them, then name the traps
> Two terminals on one stream may throw `IllegalStateException`. `forEach` + `list.add` is not a reduction — use `collect`. Parallel `forEach` is unordered. `toList()` (16) is unmodifiable; `Collectors.toList()` is not specified that way. Empty `averagingInt` is `0`, not missing.

> [!tip] Interview answer
> Recite: **`forEach`/`forEachOrdered`, `collect`/`toList`, `reduce`, `count`/`min`/`max`, `toArray`, `findFirst`/`findAny`, `anyMatch`/`allMatch`/`noneMatch`.** Add primitive `sum`/`average`. Add “`iterator`/`spliterator` are terminals but not eager.” One terminal; then a new stream.
