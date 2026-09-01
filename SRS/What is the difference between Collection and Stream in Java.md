<!--
reps: 0
priority: 0
-->
#Java/Collections #Java/Streams #Java/Versions/8 #SRS

# What is the difference between `Collection` and `Stream` in Java?

> [!abstract] Short answer
> **A `Collection` stores and gives access to a finite group of elements; a `Stream` (Java 8) is a lazy, one-shot pipeline over a source.** Package doc: streams have **no storage**, are **functional** (do not modify the source), **lazy**, possibly **unbounded**, and **consumable**. Collections are data structures (`List`, `Set` with uniqueness, …). Streams are a computation pipeline; `collect` is how you land back in a collection. `Collection.stream()` is the usual bridge. `Map` and `Iterator` are collection APIs too — streams do not replace them.

## Store-and-access vs describe-and-reduce

`Collection` is the root of the collections hierarchy: a **group of objects** (its elements). Some allow duplicates, some do not; some are ordered. The JDK implements `List` / `Set` / …, not `Collection` itself. A `Set` really is the set idea (no duplicate `equals`) ([[What is the Java Collections Framework]]). The Collections Framework also includes **`Map`** (not a `Collection`) with `keySet` / `values` / `entrySet` views, and **`Iterator`** / `ListIterator` for pull traversal ([[What is the Iterator interface and why do Java collections use it]]).

`Stream` does **not** provide a way to reach in and mutate “the element at i.” Stream JavaDoc: collections care about **efficient management and access**; streams care about **declaratively describing** a source and **aggregate** ops on it. Escape hatches: `iterator()` / `spliterator()` ([[What is Stream]], [[What is the Java Stream API]], [[Does the Stream API use an Iterator internally]]). The engine is a `Spliterator`, not an `Iterator` loop.

Package-summary contrast:

| | `Collection` (and collection APIs) | `Stream` |
| --- | --- | --- |
| Storage | Holds elements (except views that delegate) | Conveys them; not a data structure |
| Mutation | Mutators (`add`, …) or unmodifiable | Ops do not modify the source; `filter` yields a new stream |
| When work runs | Eager: the elements are already there | Lazy intermediates; terminal starts the walk |
| Size | Finite | May be infinite (`iterate`, `generate`); `limit` / `findFirst` can stop |
| Reuse | Iterate again | One walk; new stream from the source to revisit |
| Access | `get` / `contains` / `iterator` | No `get(i)`; `filter`/`map`/`reduce`/`collect` |

Dump’s “elements one-by-one vs as a whole” is that access-vs-aggregate split — not that you cannot `forEach` a stream. Dump’s “`Collection` is a data structure, `Stream` is a pipeline whose result is a structure or a search” matches **no storage** vs `collect` / `findFirst` ([[What is the Java Stream API]], [[What is the collect terminal operation in Java streams]]).

`Collection.stream()` / `parallelStream()` produce a stream over the collection as of the **terminal**. Do not mutate a non-concurrent collection while that terminal runs. `Map` is not a `Collection`; there is **no** `Map.stream()` — stream `entrySet()` / `keySet()` / `values()` ([[What ways exist to create a Java stream]]). A terminal `collect` lands back in a `List`/`Set`/`Map` — that is the collection API again. Neither API is `java.io`. An enhanced-for over a `List` is Collections + `Iterator`. `list.stream().map(...).collect(...)` is the same list, queried.

```d2
direction: down
coll: "Collection / Map / Iterator\n(store, access, finite)" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
st: "Stream pipeline\n(lazy, consumable)" {
  width: 260
  height: 55
  style.fill: "#fff8e1"
}
out: "collect / reduce / find\n(new structure or value)" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
coll -> st
st -> out
```

**Fig. 1.** Typical flow: collection APIs own the data, stream as query, collection or scalar as result.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

class Demo {
    static Set<String> nonempty(List<String> words) {
        return words.stream()
            .filter(s -> !s.isEmpty())
            .collect(Collectors.toSet());
    }

    static List<String> viaIterator(List<String> words) {
        List<String> out = new ArrayList<>();
        for (String w : words) {
            if (!w.isEmpty()) {
                out.add(w.toUpperCase());
            }
        }
        return out;
    }

    static List<String> viaStream(List<String> words) {
        return words.stream()
            .filter(s -> !s.isEmpty())
            .map(String::toUpperCase)
            .collect(Collectors.toList());
    }
}
```

**Listing 1.** `List` stores the data. `stream()` does not copy it until `collect`. `filter` does not `remove` from `words`. The loop mutates a new `ArrayList` with the collection API; the stream does not mutate `words`.

> [!warning] A stream is not a live view you can index, and it is not reusable
> There is no `stream.get(i)`. After `collect`/`count`/`forEach`, that stream is consumed. Holding a `Stream` field like a `List` is the wrong model. `forEach` on a stream is a terminal, not `Iterable.forEach`. Modifying `words` **during** `collect` is interference. Views (`subList`, `Map.keySet`) are still collections, not streams. Parallel streams do not make the `ArrayList` itself thread-safe.

> [!tip] Interview answer
> **`Collection` = stored finite group you can access and (usually) mutate. `Stream` = lazy one-pass pipeline that does not store and does not mutate the source.** Name the five package bullets: no storage, functional, lazy, possibly unbounded, consumable. `Set` uniqueness is a collection contract; `distinct()` is a stream stage. You still *have* a collection (or `Map`); you *query* it with `stream()` and often `collect` back.
