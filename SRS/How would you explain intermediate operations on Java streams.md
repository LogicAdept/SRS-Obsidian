<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# How would you explain intermediate operations on Java streams?

> [!abstract] Short answer
> **They turn a stream into another stream and are always lazy.** `filter`, `map`, `sorted` and the rest do not touch the source when you call them; they build a pipeline. Traversal starts only when a **terminal** operation runs (`forEach`, `collect`, `count`, `reduce`, …). After that terminal, the pipeline is consumed.

## Lazy `Stream`-producing stages

A stream pipeline is a **source**, then zero or more **intermediate** operations, then one **terminal** operation ([[What is the Java Stream API]], [[What kinds of stream operations exist in Java]], [[When does a Java stream pipeline actually start executing]]). Intermediate ops **return a new stream**. Calling `filter` does not filter yet: it creates a stream that, when later traversed, holds matching elements. Source traversal does not begin until the terminal op executes.

They split further:

- **Stateless** (`filter`, `map`) — no memory of earlier elements; each element can be processed alone.
- **Stateful** (`distinct`, `sorted`) — may use previously seen elements. `sorted` cannot emit until it has seen the whole input, so parallel pipelines may buffer or take extra passes ([[What is the Stream sorted method for]], [[How do you print unique squares of numbers using map]]).
- **Short-circuiting intermediate** (`limit`, `takeWhile`) — may turn infinite input into a finite stream. That is necessary but not sufficient for an infinite pipeline to finish ([[What is the Stream limit method for]]).

Common intermediate methods: `filter`, `map` / `mapToInt`, `flatMap` / `flatMapToInt`, `distinct`, `sorted`, `peek`, `limit`, `skip`, `takeWhile`, `dropWhile`. Behavioral parameters must be non-interfering and, in most cases, stateless.

A stream may be operated on only once. Reuse **may** throw `IllegalStateException` if detected. Terminals are eager except the escape hatches `iterator()` and `spliterator()` ([[Does the Stream API use an Iterator internally]], [[What terminal stream operations do you know in Java]]).

```d2
direction: down
src: "source\nCollection / array / ints()" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
mid: "intermediate\nfilter, map, sorted…\nlazy, return Stream" {
  width: 300
  height: 80
  style.fill: "#fff8e1"
}
term: "terminal\ncollect, forEach, count\nstarts traversal" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
src -> mid
mid -> term
```

**Fig. 1.** Intermediate stages only describe the next stream. The terminal op is what walks the source.

```java
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

class Demo {
    static List<String> longUpper(List<String> names) {
        return names.stream()
            .filter(s -> s.length() > 3)
            .map(String::toUpperCase)
            .collect(Collectors.toList());
    }

    static Stream<String> notRunYet(List<String> names) {
        return names.stream()
            .filter(s -> s.length() > 3)
            .map(String::toUpperCase);
    }
}
```

**Listing 1.** `longUpper` runs when `collect` (terminal) executes. `notRunYet` has only intermediate ops — no filtering or mapping happens until a later terminal.

> [!warning] Intermediate does not mean “already computed”
> `peek` / `map` with side effects may **never run**. The implementation may elide stages if they cannot affect the result — `list.stream().peek(System.out::println).count()` need not print when `count` can use the source size. Do not put required logic in intermediate lambdas except documented terminals such as `forEach`.

> [!warning] Stateful intermediates plus infinite sources
> `sorted()` or `distinct()` on unlimited `Random.ints()` never completes: they wait for the whole stream. Put a short-circuit (`limit`) **before** those stages. After any terminal, you cannot reuse that stream object; get a new stream from the source.

> [!tip] Interview answer
> **Intermediate operations return a new `Stream` and are always lazy — `filter` and `map` do no work until a terminal op starts.** Stateless ones process elements independently; stateful ones such as `sorted` and `distinct` may need the whole input. The pipeline is one-shot after the terminal; `count` can even skip intermediates when the size is already known.
