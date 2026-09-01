<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# What is the Stream `sorted` method for?

> [!abstract] Short answer
> **To give the pipeline a sorted encounter order without mutating the source.** `sorted()` uses natural order (`Comparable`); `sorted(Comparator)` uses that comparator. Both are lazy **stateful intermediate** ops: they buffer **all** input and only compare when a **terminal** runs. On an ordered stream the sort is **stable**. The original `List`/`Set` is untouched — `filter`/`sorted` produce a new stream, not an in-place `Collections.sort`.

## Sort the stream, not the collection

`Stream.sorted()` returns a stream of this stream’s elements sorted by natural order. Non-`Comparable` elements may throw `ClassCastException` **when the terminal executes**. `sorted(Comparator)` takes a non-interfering, stateless comparator. Both are **stateful intermediate** operations ([[How would you explain intermediate operations on Java streams]]). Primitive streams have `sorted()` in natural numeric order (no `Comparator` overload).

Dump’s “sorted representation” is that new stream: the source collection’s iteration order does **not** change. Package doc: stream ops are functional and do not modify the source. Nothing is ordered in memory until a terminal materializes it (`collect`, `toArray`, `forEachOrdered`) ([[What is the difference between Collection and Stream in Java]], [[When does a Java stream pipeline actually start executing]]).

`sorted()` also **imposes encounter order** on an unordered source (`HashSet`). Downstream `limit(n)` then means “smallest *n* in sort order” (full sort). `limit` then `sorted` sorts only the prefix ([[What is the Stream limit method for]], [[How do you print 10 random numbers in ascending order with streams]]).

Stability: equal elements keep relative encounter order **if** the stream was ordered. Parallel `sorted` still has to produce a globally ordered result and may buffer heavily ([[How would you explain parallel streams in Java]]).

Primitive streams: `IntStream.sorted()` (natural numeric order; no `Comparator` overload).

```d2
direction: right
src: "source collection\n(unchanged)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
st: "sorted() stage\n(lazy, buffers at terminal)" {
  width: 240
  height: 55
  style.fill: "#fff8e1"
}
out: "ordered encounter" {
  width: 170
  height: 50
  style.fill: "#e8f5e9"
}
src -> st
st -> out
```

**Fig. 1.** `sorted` is a stream stage. The collection you called `stream()` on is not `Collections.sort`’d.

```java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Demo {
    static List<String> copySorted(List<String> words) {
        return words.stream()
            .sorted(Comparator.naturalOrder())
            .toList();
    }
}
```

**Listing 1.** `words` stays in original order. The returned list is a new sequence. `toList()` is Java 16; `collect(Collectors.toList())` is Java 8. `sorted()` with no comparator is equivalent here because `String` is `Comparable`.

> [!warning] The sort runs at the terminal — and it sees every element
> `list.stream().sorted()` with no terminal does no comparisons and does not copy. `ClassCastException` for a non-`Comparable` shows up then. A stateful comparator is broken, especially in parallel. `forEach` after `sorted` on a **parallel** stream still may ignore encounter order — use `forEachOrdered` to print sort order.

> [!tip] Interview answer
> **`sorted` is the lazy stateful sort of the stream: natural order or a `Comparator`, source collection left alone.** It cannot emit until the whole input is seen. Contrast with `Collections.sort` / `List.sort`, which mutate the list.
