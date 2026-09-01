<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS

# How would you explain how many elements will if Iterator.next will 10 Iterator.hasNext?

> [!abstract] Short answer
> **None are skipped.** Ten `hasNext()` calls still leave the cursor where it was. `hasNext()` only asks whether `next()` would return an element instead of throwing. `next()` is what returns the element and **advances**. After ten `hasNext()`s, the first `next()` is still the first remaining element.

## `hasNext` is a query; `next` consumes

`boolean hasNext()`: returns `true` if the iteration has more elements — in other words, if `next()` would return an element rather than throw. It does not return an element and does not move the iteration [[What is the Iterator interface and why do Java collections use it]].

`E next()`: returns the **next** element in the iteration (and thereby consumes it). `NoSuchElementException` if there is none [[What happens if you call Iterator.next without calling hasNext first]].

So `hasNext()` ten times, then `next()` once → **zero** elements skipped; you get the same element you would have gotten with a single `hasNext()` + `next()`. Calling `hasNext()` in a tight loop without `next()` never drains the iterator. OpenJDK `ArrayList.Itr.hasNext` is `cursor != size` (or `remaining > 0` on `ArrayDeque`) — a read of position, not an increment.

You **may** call `next()` without `hasNext()` if you know there is an element; `hasNext` is not a required preamble, it is the safe test [[What happens if you call Iterator.next without calling hasNext first]], [[How are Iterable Iterator and for-each related in Java]].

```d2
direction: down
hn: "hasNext() × 10\nquery only" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
nx: "next() × 1\nreturns first remaining" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
skip: "elements skipped: 0" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}

hn -> nx -> skip
```

**Fig. 1.** Repeating the check does not walk. Only `next()` walks.

```java
class HasNextDoesNotSkip {
    static String firstAfterTenChecks(java.util.Iterator<String> it) {
        for (int i = 0; i < 10; i++) {
            it.hasNext();
        }
        return it.next(); // same element as after a single hasNext()
    }
}
```

**Listing 1.** For `["a", "b", "c"]` this returns `"a"`, not `"c"` and not a tenth element. Ten `next()` calls would be what consumes ten elements (or throws `NoSuchElementException` if fewer remain).

> [!warning] Do not implement `hasNext` by calling `next`
> That would skip elements and break the contract (`hasNext` means “`next` would succeed”). The usual nested-iterator bug is calling `next()` too often, not `hasNext()` too often.

> [!warning] Ten `next()` is a different question
> If the dump is misread as “`next` ten times then `hasNext`”: after ten successful `next()` calls, `hasNext()` is `true` iff **more than ten** elements remained at the start. That is consumption; `hasNext` still does not skip extra ones.

> [!tip] Interview answer
> **Zero elements skipped.** `hasNext()` only checks that a `next()` would not throw; it does not advance. After ten `hasNext()` calls, `next()` still returns the first remaining element. `next()` is what walks the iterator.
