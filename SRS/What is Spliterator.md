<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Streams #Java/Versions/8 #SRS

# What is Spliterator

> [!abstract] Short answer
> **`Spliterator<T>` (Java 8) is an object that traverses and partitions a source** — array, `Collection`, channel, or generator. Sequential walk is `tryAdvance` / `forEachRemaining`. Parallel work is `trySplit` plus `estimateSize` and a bit-set of `characteristics()`. It is **not** an `Iterator`: no `hasNext`/`next` pair, **no `remove`**. Primitive nests `OfInt` / `OfLong` / `OfDouble` avoid boxing. Streams are driven by one.

## Traverse, split, report bits

Eight methods. Four are abstract: `tryAdvance(Consumer)`, `trySplit()`, `estimateSize()`, `characteristics()`. Four have defaults: `forEachRemaining` (loop `tryAdvance` until false — override when you can), `getExactSizeIfKnown` (`estimateSize` if `SIZED`, else `-1`), `hasCharacteristics`, `getComparator` (throws unless `SORTED`).

`tryAdvance` runs the action on one remaining element and returns whether one existed. `trySplit` peels off a second `Spliterator` covering elements this one will **no longer** cover (`null` if it cannot split). `ORDERED` splits must be a strict prefix. Repeated `trySplit` on a finite source must eventually return `null`. Traversal and splitting **exhaust** the spliterator: one bulk computation per instance ([[What internal abstractions power a Java stream pipeline]], [[What backs Java parallelStream under the hood]]).

`estimateSize` is remaining elements for a full `forEachRemaining`, or `Long.MAX_VALUE` if infinite, unknown, or too expensive. `SIZED` means that estimate is exact **before** traversal or split. Characteristics are ORed from `ORDERED`, `DISTINCT`, `SORTED`, `SIZED`, `NONNULL`, `IMMUTABLE`, `CONCURRENT`, `SUBSIZED`. Example: a `Collection` typically reports `SIZED`; a `Set` `DISTINCT`; a `SortedSet` also `SORTED` ([[What types of iterators or cursors exist in Java]], [[Does the Stream API use an Iterator internally]]).

Primitive specializations: `Spliterator.OfInt`, `OfLong`, `OfDouble` (and `OfPrimitive`). Default `tryAdvance(Consumer)` / `forEachRemaining(Consumer)` **box**. Prefer `tryAdvance(IntConsumer)` and friends.

```d2
src: "source\narray / Collection / generator" {
  shape: rectangle
}
sp: "Spliterator\ntryAdvance · trySplit\nestimateSize · characteristics" {
  shape: rectangle
}
left: "this (remainder)" {
  shape: rectangle
}
right: "returned split\n(or null)" {
  shape: rectangle
}
seq: "forEachRemaining\n(current thread)" {
  shape: rectangle
}
src -> sp: "bind"
sp -> left: "keep"
sp -> right: "trySplit"
sp -> seq: "sequential bulk"
```

**Fig. 1.** One spliterator walks or splits. The split-off instance may go to another thread; the original must not be used concurrently.

```java
List<String> names = Arrays.asList("a", "b", "c", "d");
Spliterator<String> left = names.spliterator();
Spliterator<String> right = left.trySplit();
left.tryAdvance(System.out::println);
if (right != null) {
    right.forEachRemaining(System.out::println);
}
boolean sized = left.hasCharacteristics(Spliterator.SIZED);
```

**Listing 1.** `Collection.spliterator()` (since 1.8). `trySplit` may return `null`. `SIZED` makes `getExactSizeIfKnown()` useful.

> [!warning] Not an `Iterator`, and not thread-safe
>
> There is no `remove`. That does **not** mean the source is frozen: `IMMUTABLE` vs `CONCURRENT` are **source** flags. After binding, structural interference on a non-`IMMUTABLE` / non-`CONCURRENT` source is fail-fast at best (`ConcurrentModificationException`) or arbitrary. Spliterators themselves are **not** thread-safe: hand the **returned** split to another thread; two threads on the **same** instance is undefined. Boxing `Consumer` on `OfInt` undoes the primitive win.

> [!tip] Interview answer
>
> **Java 8 cursor for sequential *and* parallel walk: `tryAdvance`, `trySplit`, `estimateSize`, `characteristics`.** Four defaults. `OfInt`/`OfLong`/`OfDouble` for primitives. No `remove`; designed to avoid the `hasNext`/`next` race. Name `trySplit` as why `parallelStream` can divide work. Poor splits (iterator wrapper, unknown size) parallelize badly.
