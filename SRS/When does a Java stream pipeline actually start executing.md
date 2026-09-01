<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations #Java/Versions/8 #SRS

# When does a Java stream pipeline actually start executing?

> [!abstract] Short answer
> **When a terminal operation is invoked — not when you call `filter` / `map` / `sorted`.** Intermediate ops are always lazy: they only return another stream. `list.stream().filter(…).map(…)` with no terminal does **no** filtering or mapping. Except the escape hatches `iterator()` / `spliterator()`, execution **starts** at that invoke and **ends** when the terminal returns. Laziness also lets the implementation skip work: short-circuit (`findFirst`, `limit`) and even skip whole stages (`count` from a sized source).

## Terminal = start; intermediates = recipe

A pipeline is source + zero or more intermediates + one terminal ([[What is the Java Stream API]], [[What kinds of stream operations exist in Java]], [[What is Stream]]). Calling `filter` “creates a new stream that, when traversed, contains the matching elements” ([[What intermediate stream operations do you know in Java]]). **Intermediate operations are always lazy.** Traversal of the source does not begin until the terminal operation executes.

Most terminals are **eager**: they finish walking (as far as they need) before they return (`collect`, `forEach`, `reduce`, `sum`, `findFirst`, …) ([[What terminal stream operations do you know in Java]], [[How do you count empty strings using filter]]). Short-circuiting terminals (`findFirst`, `anyMatch`, `limit` then `findFirst`) may stop early; they still **started** at the terminal call.

**Not eager:** `iterator()` and `spliterator()`. They are terminals (the pipeline is then consumed as a recipe for a cursor) but they do not drain the source up front. Pulling the iterator is when elements are produced ([[Does the Stream API use an Iterator internally]]).

Non-interference: except those escape hatches, execution begins at the terminal and ends when it completes. You may mutate a well-behaved collection **before** the terminal; those changes are visible. Mutating it **during** the terminal is interference. `Files.lines` populates **lazily as consumed** — opening the stream is not a full read ([[What ways exist to create a Java stream]]). Stateful intermediates (`sorted`, `distinct`) still have to see the whole (remaining) stream once the terminal starts — laziness does not make `ints().sorted()` finite ([[What is the Stream sorted method for]], [[What is the Stream limit method for]]).

`count()` may compute size from the source and **elide** intermediates (`peek` on a `List` may print nothing) ([[What is the peek method on stacks queues or streams in Java]]). That is still “the terminal started” — it just proved it did not need to walk. Mapper errors are deferred the same way: `stream.map(Integer::parseInt)` on `"oops"` does not throw until a terminal pulls that element.

```d2
direction: right
build: "stream().filter().map()\n(no walk yet)" {
  width: 240
  height: 55
  style.fill: "#fff8e1"
}
term: "collect / count / forEach\n(walk starts)" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
build -> term
```

**Fig. 1.** Building the chain is free. The terminal is the start gun — unless the implementation can skip that walk.

```java
import java.util.List;

class Demo {
    static List<String> builtNotRun(List<String> names) {
        names.stream()
            .filter(s -> s.length() > 3)
            .map(String::toUpperCase);
        return names;
    }

    static long nonempty(List<String> words) {
        var pipeline = words.stream()
            .filter(s -> !s.isEmpty()); // still no reads
        return pipeline.count();        // walk starts here
    }

    static long sizedCount(List<String> names) {
        return names.stream()
            .peek(System.out::println)
            .count();
    }
}
```

**Listing 1.** `builtNotRun` never filters or maps (no terminal). Assigning the `Stream` in `nonempty` does not execute `filter`; `count()` does. `sizedCount` may not print: `count` can use the list size. A second terminal on `pipeline` is illegal.

> [!warning] `peek` is not a debugger you can trust, and `iterator()` is a terminal
> Side effects in `map`/`filter`/`peek` may never run if the terminal can skip them (`count` on a sized source). `forEach` / `forEachOrdered` are specified to run their actions. Calling `iterator()` “starts” the pipeline in the API sense even if you have not yet called `next()`. Infinite `generate` without a short-circuit terminal never returns. Forgetting `collect` / `forEach` looks like a “broken filter.”

> [!warning] Lazy is not “free to mutate during the run”
> You may change a well-behaved `List` **before** the terminal starts. During execution, interfering with a non-concurrent source is undefined.

> [!tip] Interview answer
> **Nothing runs until a terminal op.** Intermediates are lazy plumbing. That is why a pipeline without `collect`/`forEach`/`count` does nothing, why `findFirst` need not scan everything, and why `count` can skip `peek` on a sized list. Name the exception: `iterator`/`spliterator` hand back a cursor instead of draining immediately.
