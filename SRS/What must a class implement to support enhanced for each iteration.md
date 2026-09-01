<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Language/Loops #SRS

# What must a class implement to support enhanced for each iteration?

> [!abstract] Short answer
> **`Iterable<T>`** — and therefore **`Iterator<T> iterator()`**. Enhanced `for` will compile on `obj` only if `obj`’s type is an array or a subtype of `Iterable`. A class is not an array, so it must implement `Iterable` and return a live `Iterator` whose `hasNext()` / `next()` walk the elements. Implementing **`Iterator` alone does not** make the class a for-each target.

## What the class actually supplies

```d2
direction: down
cls: "your class" {
  width: 200
  height: 50
  style.fill: "#eceff1"
}
itbl: "implements Iterable<T>\niterator()" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
itr: "returns a new Iterator<T>\nhasNext / next" {
  width: 280
  height: 70
  style.fill: "#c8e6c9"
}
loop: "for (T x : obj)" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
cls -> itbl
itbl -> itr
loop -> itbl
```

**Fig. 1.** The class implements `Iterable`. The **cursor** is a separate `Iterator`. Enhanced `for` calls `iterator()` once, then `hasNext()` / `next()` until false.

`Iterable.iterator()` is the only abstract method you must write. `remove()` on `Iterator` is optional; the default throws `UnsupportedOperationException`. The for-each rewrite never calls `remove()`. `next()` with no remaining element throws `NoSuchElementException`.

Why `Iterable` is the type test, and why arrays skip it: [[What language feature enables the enhanced for each loop]]. The rewrite: [[How would you explain the enhanced for each loop in Java]]. You do not implement `Collection`; `Collection` already extends `Iterable`, so lists and sets work without extra code.

```java
import java.util.Iterator;
import java.util.NoSuchElementException;

final class Range implements Iterable<Integer> {
    private final int start;
    private final int endExclusive;

    Range(int start, int endExclusive) {
        this.start = start;
        this.endExclusive = endExclusive;
    }

    @Override
    public Iterator<Integer> iterator() {
        return new Iterator<Integer>() {
            private int next = start;

            @Override
            public boolean hasNext() {
                return next < endExclusive;
            }

            @Override
            public Integer next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                return next++;
            }
        };
    }

    public static void main(String[] args) {
        for (int n : new Range(1, 4)) {
            System.out.print(n);
        }
        // 123
        for (int n : new Range(1, 4)) {
            System.out.print(n);
        }
        // 123 again — each for-each got a fresh iterator()
    }
}
```

**Listing 1.** `Range` implements `Iterable`, not `Iterator`. Each enhanced `for` calls `iterator()` and gets a **new** cursor, so a second loop over the same instance starts at `start` again.

A type that implements only `Iterator` is a cursor, not a for-each source. You can write `while (it.hasNext())`, but `for (E e : it)` does not compile unless that type is also `Iterable`. A duck-typed `iterator()` method that is not the `Iterable` method is the same compile-time error.

```java
class HasIteratorMethod {
    public java.util.Iterator<String> iterator() {
        return java.util.Collections.singletonList("x").iterator();
    }

    static void willNotCompile(HasIteratorMethod bag) {
        // for (String s : bag) { }  // not Iterable, not an array
    }
}
```

**Listing 2.** The compiler checks `Iterable` (or array), not “a method named `iterator`.”

> [!warning] Do not make the collection its own `Iterator`
> If `iterator()` returns `this`, every loop shares one cursor. The first `for (T x : obj)` drains it; a second loop sees `hasNext() == false`. Returning `null` fails the same way as `for (T x : (Iterable<T>) null)` — `NullPointerException` on `iterator()` / `hasNext()`. Enhanced `for` is specified to call `iterator()` at entry and then walk **that** iterator. Return a new iterator each time.

> [!warning] `remove()` is not part of for-each support
> You do not need `remove()` for `for (T x : obj)` to compile or run. The optional `remove` is a mutation API on the iterator, with unspecified behavior if the collection is modified any other way during iteration: [[Can you modify a collection while iterating with a for-each loop]].

> [!tip] Interview answer
> **A class must implement `Iterable` and provide `iterator()` that returns an `Iterator` with `hasNext` and `next`.** `Iterator` alone is not enough. Return a **new** iterator each call; do not use the collection object as the cursor. Arrays need no interface.
