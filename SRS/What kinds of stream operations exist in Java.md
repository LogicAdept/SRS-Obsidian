<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations #Java/Versions/8 #SRS

# What kinds of stream operations exist in Java?

> [!abstract] Short answer
> **Two kinds on the pipeline: intermediate and terminal.** Intermediates return a **new stream** and are **always lazy**. Terminals produce a value or a side-effect, start the walk, and **consume** the stream. Intermediates split further into **stateless** (`filter`, `map`) vs **stateful** (`distinct`, `sorted`). Either kind may be **short-circuiting** (`limit`, `findFirst`). Almost all terminals are eager; `iterator()` / `spliterator()` are the non-eager escape hatches. Sequential vs parallel is a **mode**, not a third kind of op.

## Intermediate vs terminal, then the subtypes

Package doc: operations combine into a **pipeline** — source, zero or more intermediates (`filter`, `map`, …), one terminal (`forEach`, `reduce`, …) ([[What is the Java Stream API]], [[When does a Java stream pipeline actually start executing]]).

**Intermediate** — return a stream; **always lazy**. Calling `filter` does not filter yet. Traversal starts only at the terminal ([[What intermediate stream operations do you know in Java]], [[When does a Java stream pipeline actually start executing]]).

- **Stateless** — `filter`, `map`: no memory of earlier elements.
- **Stateful** — `distinct`, `sorted`: may use previously seen elements. `sorted` cannot emit until it has seen everything; parallel pipelines may buffer or take extra passes ([[What is the Stream sorted method for]]).
- **Short-circuiting intermediate** — `limit`, `takeWhile`: may turn infinite input into a finite stream ([[What is the Stream limit method for]]).

**Terminal** — result or side-effect; pipeline then **consumed**. Almost all are **eager**. Exceptions: `iterator()` and `spliterator()` ([[What terminal stream operations do you know in Java]], [[Does the Stream API use an Iterator internally]]).

- **Short-circuiting terminal** — `findFirst`, `findAny`, `anyMatch` / `allMatch` / `noneMatch`: may finish without visiting every element.

A short-circuiting op in the pipeline is **necessary but not sufficient** for an infinite source to terminate.

`peek` is still intermediate (debug side effects; may be elided). `forEach` is terminal (side effects specified to run). Sequential vs parallel is `stream()` / `parallelStream()` / `.parallel()` — the same op kinds, different execution.

```d2
direction: down
ops: "stream operations" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
mid: "intermediate (lazy Stream)" {
  width: 260
  height: 45
  style.fill: "#fff8e1"
}
term: "terminal (consumes)" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
ops -> mid
ops -> term
```

**Fig. 1.** The package’s primary split. Stateless / stateful / short-circuiting cut across it.

```java
import java.util.List;
import java.util.stream.Collectors;

class Demo {
    static List<String> sample(List<String> words) {
        return words.stream()          // source
            .filter(s -> !s.isEmpty()) // stateless intermediate
            .sorted()                  // stateful intermediate
            .limit(3)                  // short-circuiting intermediate
            .collect(Collectors.toList()); // terminal
    }
}
```

**Listing 1.** One of each: stateless, stateful, short-circuiting intermediate, then an eager terminal. Until `collect`, none of the intermediates have run.

> [!warning] Without a terminal, “kinds” do not run
> A chain of only intermediates is a recipe, not work. Two terminals on one stream are illegal. `count()` may skip `peek` even though `peek` is an intermediate. Infinite `generate` without a short-circuit **and** a terminal that can stop will not halt.

> [!tip] Interview answer
> **Intermediate (lazy, return `Stream`) vs terminal (eager except `iterator`/`spliterator`, consume).** Then: stateless vs stateful, and short-circuiting on either side. Sequential/parallel is how they run, not a third column of methods.
