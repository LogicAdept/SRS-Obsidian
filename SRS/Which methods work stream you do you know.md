<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations #Java/Versions/8 #SRS

# Which methods work stream you do you know?

> [!abstract] Short answer
> **Two families: lazy intermediates (return a stream) and terminals (start the walk, consume it).** Intermediates you should name: `filter`, `map` / `mapToInt`, `flatMap` / `flatMapToInt`, `distinct`, `sorted`, `peek`, `limit`, `skip` (`takeWhile`/`dropWhile` since 9; `mapMulti` since 16). Terminals: `forEach` / `forEachOrdered`, `collect` / `toList` (16), `toArray`, `reduce`, `count`, `min` / `max`, `findFirst` / `findAny`, `anyMatch` / `allMatch` / `noneMatch`. Numeric: `sum`, `average` (`OptionalDouble`), `mapToObj`. Nothing runs until a terminal.

## Intermediate vs terminal catalogs

Dump asked both. Package split: intermediates always lazy; terminals consume ([[What kinds of stream operations exist in Java]], [[What intermediate stream operations do you know in Java]], [[What terminal stream operations do you know in Java]], [[What is the Java Stream API]]).

**Intermediates (Java 8 unless noted)**

| Method | Role |
| --- | --- |
| `filter(Predicate)` | Keep matches ([[How would you explain what method filter in stream]]) |
| `map` / `mapToInt` / `mapToLong` / `mapToDouble` | One-to-one; primitives skip boxing |
| `flatMap` / `flatMapTo*` | One-to-many, flatten ([[What is the difference between Stream map and flatMap]]) |
| `distinct` | Unique per `equals`; stable if ordered |
| `sorted` / `sorted(Comparator)` | Stateful sort; source collection unchanged ([[What is the Stream sorted method for]]) |
| `peek` | Debug side-effect as elements are consumed — **may be skipped** ([[What is the peek method on stacks queues or streams in Java]]) |
| `limit(n)` / `skip(n)` | Prefix cap (short-circuiting) / drop prefix ([[What is the Stream limit method for]]) |
| `mapToObj` on `IntStream` | Primitive → `Stream<U>` (still intermediate) |

**Terminals**

| Method | Role |
| --- | --- |
| `findFirst` / `findAny` | `Optional`; `findAny` may differ on parallel repeats |
| `collect` | Mutable reduction ([[What is the collect terminal operation in Java streams]]) |
| `count` | `long`; may skip `peek` on a sized source |
| `anyMatch` / `allMatch` / `noneMatch` | Empty: `false` / `true` / `true` |
| `min` / `max` | `Optional` + `Comparator` on `Stream`; primitives have no-arg forms |
| `forEach` / `forEachOrdered` | Parallel `forEach` ignores encounter order ([[What is the difference between forEach and forEachOrdered on a stream]]) |
| `toArray` / `reduce` | Array; fold to one value (`Optional` without identity) |
| `IntStream.sum` / `average` | `sum` empty → `0`; `average` → `OptionalDouble` ([[How do you get the average of numbers in a stream]]) |

Also: `iterator()` / `spliterator()` (not eager). `toList()` (16).

```d2
direction: down
m: "stream methods" {
  width: 180
  height: 35
  style.fill: "#e3f2fd"
}
i: "intermediate (lazy)" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
t: "terminal (runs, consumes)" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
m -> i
m -> t
```

**Fig. 1.** Recite two lists, not one undifferentiated pile.

```java
import java.util.List;
import java.util.stream.Collectors;

class Demo {
    static List<Integer> demo(List<String> words) {
        return words.stream()
            .filter(s -> !s.isEmpty())
            .map(String::length)
            .distinct()
            .sorted()
            .limit(5)
            .collect(Collectors.toList());
    }
}
```

**Listing 1.** Several intermediates, one terminal. Until `collect`, `filter`/`map`/`distinct`/`sorted`/`limit` have not run.

> [!warning] Dump traps: `peek` always runs, `average` is a `double`, `mapToObj` is terminal
> `peek` can be elided (`count` on a `List`). `average()` is `OptionalDouble` — empty is not `0` (unlike `Collectors.averagingInt`). `mapToObj` is **intermediate**. `allMatch` on an empty stream is `true`. `peek` does not “return the same stream object” in any API you should rely on — it returns a stream of the same elements plus an action.

> [!tip] Interview answer
> Split the answer: **intermediates** (`filter`, `map`/`flatMap`, `distinct`, `sorted`, `limit`/`skip`, `peek`) then **terminals** (`collect`, `reduce`, `count`, `forEach`/`forEachOrdered`, `find*`, `*Match`, `min`/`max`, `toArray`; numeric `sum`/`average`). End with: lazy until the terminal; one terminal per pipeline.
