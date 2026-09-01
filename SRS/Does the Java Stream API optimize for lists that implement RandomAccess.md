<!--
reps: 0
priority: 0
-->
#Java/Streams #Java/Collections/List #Java/Versions/8 #SRS

# Does the Java Stream API optimize for lists that implement `RandomAccess`?

> [!abstract] Short answer
> **Not inside `map` / `filter` / `collect`.** `list.stream()` builds a sequential stream from the list’s **spliterator**. The default `List.spliterator()` (Java 8) does the `RandomAccess` check: index `get(int)` traversal (and half-range splits) versus an `Iterator`. Concrete lists may override `spliterator()` entirely.

## The check is on `spliterator()`, not on stream ops

`RandomAccess` is a **marker** (Java 1.4) for `List` implementations with fast (generally constant-time) indexed access. Its stated purpose is that generic **list algorithms** can switch strategy: `ArrayList`-style index loops vs `LinkedList`-style iterators. A rule of thumb in the contract: if `get(i)` in a counted loop beats `Iterator.next()`, implement the marker ([[Why was ArrayList added when Vector already existed]]).

`Collection.stream()` (Java 8) does not look at `RandomAccess`. Its default implementation creates a sequential `Stream` from `spliterator()`. `parallelStream()` does the same with a possibly parallel stream. Pipeline stages then split and traverse that spliterator ([[What is the Java Stream API]], [[What internal abstractions power a Java stream pipeline]], [[What is the difference between sequential and parallel streams in Java]]). OpenJDK `Stream` has no `RandomAccess` mention.

`List.spliterator()` is where the marker is used. Default implementation (late-binding, reports `SIZED` and `ORDERED`, plus `SUBSIZED`):

- If `this instanceof RandomAccess` → traverse with `List.get(int)`. `IndexOutOfBoundsException` is turned into fail-fast `ConcurrentModificationException`. If the list is also an `AbstractList`, `modCount` adds more fail-fast. OpenJDK uses `AbstractList.RandomAccessSpliterator`, which `trySplit`s by cutting the index range in half.
- Otherwise → a spliterator from the list’s `Iterator` (iterator fail-fast). That is the sequential-access path ([[Does the Stream API use an Iterator internally]]).

So a custom `RandomAccess` list that **keeps** the default `spliterator()` gets index-based streaming “for free.” A list that **overrides** `spliterator()` (typical for JDK `ArrayList`) follows its own implementation, marker or not.

```d2
direction: down
stream: "list.stream()" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
spl: "spliterator()" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
ra: "instanceof RandomAccess\nget(i) + index splits" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
it: "not RandomAccess\nIterator spliterator" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
stream -> spl
spl -> ra
spl -> it
```

**Fig. 1.** Stream construction asks the list for a spliterator. Only the default `List.spliterator()` branches on `RandomAccess`.

```java
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.RandomAccess;

class Demo {
    static boolean defaultWouldUseGet(List<?> list) {
        return list instanceof RandomAccess;
    }

    static long count(List<String> list) {
        return list.stream().count();
    }

    static void demo() {
        defaultWouldUseGet(new ArrayList<>());  // true
        defaultWouldUseGet(new LinkedList<>()); // false
        count(List.of("a", "b"));
    }
}
```

**Listing 1.** `ArrayList` is the documented random-access example; `LinkedList` is the sequential example. `stream()` works on both; the marker only changes the **default** spliterator strategy.

> [!warning] `RandomAccess` on a linked list is a slowdown
> The marker promises that `get(i)` is the fast loop. If you implement `RandomAccess` on a structure where `get(i)` is O(n), default `List.spliterator()` will call `get` per element and `trySplit` by index — the quadratic case the `RandomAccess` contract warns about. Do not stamp the interface to “help” streams.

> [!warning] Structural change during `get` becomes `ConcurrentModificationException`
> On the RandomAccess default path, `IndexOutOfBoundsException` from `get` is reported as `ConcurrentModificationException`. That is fail-fast, not a different stream bug. Mutating the list after the late-binding spliterator binds is still interference.

> [!tip] Interview answer
> **The stream pipeline does not special-case `RandomAccess`; `list.stream()` just uses `spliterator()`.** The default `List.spliterator()` does: `RandomAccess` lists walk with `get(int)` and split by index; others use the iterator. `ArrayList` vs `LinkedList` is the textbook pair, and a fake `RandomAccess` on a linked structure makes that default path worse.
