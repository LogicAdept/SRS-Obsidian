<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# What intermediate stream operations do you know in Java?

> [!abstract] Short answer
> **They return another stream and are always lazy.** On `Stream` (Java 8): `filter`, `map` / `mapToInt` / `mapToLong` / `mapToDouble`, `flatMap` / `flatMapTo*`, `distinct`, `sorted`, `peek`, `limit`, `skip`. Java 9 adds `takeWhile` / `dropWhile`; Java 16 adds `mapMulti` / `mapMultiTo*`. Stateless vs stateful vs short-circuiting is how the package doc splits them. Nothing walks the source until a **terminal** op.

## Stream-producing stages, not a second collection

A pipeline is source + zero or more intermediate ops + one terminal. Intermediate ops **return a new stream**. Calling `filter` does not filter yet; traversal starts at the terminal ([[How would you explain intermediate operations on Java streams]], [[When does a Java stream pipeline actually start executing]], [[What kinds of stream operations exist in Java]]).

Package-summary split:

- **Stateless** — `filter`, `map` (and the `mapTo*` / `flatMap*` family): no memory of earlier elements.
- **Stateful** — `distinct`, `sorted`, `skip`, `limit`: may buffer or need the whole input (`sorted` cannot emit until it has seen everything).
- **Short-circuiting intermediate** — `limit`, `takeWhile`: may turn infinite input into a finite stream. Necessary but not sufficient for an infinite pipeline to finish.

`Stream` methods labeled intermediate in Java SE 21:

| Kind | Methods |
| --- | --- |
| Keep / drop | `filter` ([[How would you explain what method filter in stream]]) |
| One-to-one | `map`, `mapToInt`, `mapToLong`, `mapToDouble` ([[What are map and mapToInt for in Java streams]]) |
| One-to-many | `flatMap`, `flatMapToInt`, `flatMapToLong`, `flatMapToDouble` ([[What are flatMap and flatMapToInt for in Java streams]]); `mapMulti*` (16) |
| Dedup / order | `distinct`, `sorted()`, `sorted(Comparator)` ([[What is the Stream sorted method for]]) |
| Debug | `peek` — not a substitute for `forEach`; may be skipped ([[What is the peek method on stacks queues or streams in Java]]) |
| Size / prefix | `limit`, `skip` ([[What is the Stream limit method for]]); `takeWhile`, `dropWhile` (9) |

`BaseStream.unordered()` / `sequential()` / `parallel()` change mode or encounter-order constraints; they are not the `filter`/`map` family but they do return a stream.

Primitive streams add `boxed`, `mapToObj`, `asLongStream`, `asDoubleStream`. Behavioral parameters must be non-interfering and, in most cases, stateless. After any **terminal**, the pipeline is consumed ([[What terminal stream operations do you know in Java]]).

```d2
direction: down
src: "source" {
  width: 120
  height: 40
  style.fill: "#e3f2fd"
}
mid: "intermediate (lazy)\nfilter map flatMap distinct\nsorted peek limit skip …" {
  width: 280
  height: 80
  style.fill: "#fff8e1"
}
term: "terminal (starts the walk)" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
src -> mid
mid -> term
```

**Fig. 1.** Intermediate ops stack; only the terminal starts traversal.

```java
import java.util.List;
import java.util.stream.Collectors;

class Demo {
    static List<String> firstThreeLong(List<String> words) {
        return words.stream()
            .filter(s -> s.length() > 3)
            .map(String::toUpperCase)
            .sorted()
            .limit(3)
            .collect(Collectors.toList());
    }
}
```

**Listing 1.** Typical chain: stateless `filter`/`map`, stateful `sorted`, short-circuiting `limit`, then a terminal `collect`. Until `collect`, none of those stages have run.

> [!warning] Lazy means “not yet,” and stateful stages can wreck parallel speedup
> `list.stream().filter(...).map(...)` with no terminal does **zero** work. `peek` may not run when `count()` can take the size from the source. Ordered `limit` / `distinct` / `sorted` on a **parallel** pipeline may buffer heavily — `unordered()` or `sequential()` can be cheaper if order does not matter. `sorted()` on non-`Comparable` elements throws `ClassCastException` at the **terminal**, not at `sorted()`.

> [!tip] Interview answer
> **Name the lazy `Stream`-producing ops: `filter`, `map`/`mapToInt`, `flatMap`/`flatMapToInt`, `distinct`, `sorted`, `peek`, `limit`, `skip`, plus `takeWhile`/`dropWhile` (9).** They never start the pipeline; `collect`/`forEach`/`count` do. Split them as stateless vs stateful vs short-circuiting if the interviewer wants depth.
