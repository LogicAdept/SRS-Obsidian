<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Intermediate #Java/Versions/8 #SRS

# What is the Stream `limit` method for?

> [!abstract] Short answer
> **To cap the pipeline at most `maxSize` elements — the first `maxSize` when the stream is ordered.** `limit` is a lazy, **short-circuiting stateful intermediate** op. That is how infinite sources (`iterate`, `generate`, `Random.ints()`) can still finish. Negative `maxSize` throws `IllegalArgumentException`. Sequential `limit` is cheap; ordered **parallel** `limit` must keep encounter order and can be expensive (`unordered()` / `sequential()` if you do not need the first *n*).

## Bound the walk, especially infinite ones

`Stream.limit(long maxSize)` returns a stream consisting of this stream’s elements, truncated to be no longer than `maxSize`. Package doc: a short-circuiting intermediate op may turn infinite input into a finite stream; that is necessary but not sufficient — a terminal still has to run ([[What intermediate stream operations do you know in Java]], [[When does a Java stream pipeline actually start executing]]).

**Purpose in practice:** take a prefix (`list.stream().limit(10)`), page-sized chunks when paired with `skip`, or stop `iterate`/`generate` after *n* values. Dump’s “first elements” holds for **ordered** streams. Unordered sources may yield any *n* that satisfy the cap’s size, not a stable “head.”

`skip(n)` drops a prefix (stateful, not short-circuiting). `takeWhile` (Java 9) takes a **predicate** prefix, not a count ([[What intermediate stream operations do you know in Java]]).

API note: ordered parallel `limit(n)` must return the **first** *n* in encounter order, not any *n* — costly for large `maxSize`. `generate` or `unordered()` can speed it up if any *n* are enough. Need order and the parallel `limit` hurts → `sequential()` ([[What is the difference between sequential and parallel streams in Java]]).

`limit` **before** `sorted` sorts a prefix; `sorted` then `limit` is a full sort then top-*n* ([[How do you print 10 random numbers in ascending order with streams]]).

```d2
direction: right
src: "source (maybe infinite)" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
lim: "limit(n)" {
  width: 120
  height: 45
  style.fill: "#fff8e1"
}
out: "≤ n elements" {
  width: 140
  height: 45
  style.fill: "#e8f5e9"
}
src -> lim
lim -> out
```

**Fig. 1.** `limit` is what makes an unbounded pipeline eligible to finish.

```java
import java.util.stream.Stream;

class Demo {
    static Object[] tenFromIterate() {
        return Stream.iterate(0, i -> i + 1)
            .limit(10)
            .toArray();
    }
}
```

**Listing 1.** Without `limit`, `iterate` never ends. `limit(10)` is the bound; `toArray` is the terminal that actually walks those ten.

> [!warning] Lazy cap, not an eager subList
> `stream.limit(10)` with no terminal does nothing. Fewer than `maxSize` source elements yields a shorter stream, not padding. Ordered parallel `limit` is a common performance trap. `limit(-1)` throws `IllegalArgumentException`.

> [!tip] Interview answer
> **`limit(n)` is the lazy short-circuiting “at most n,” first n if ordered — used to bound infinite streams and take a prefix.** Mention the parallel/order cost and `skip`/`takeWhile` as neighbors, not synonyms.
