<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Exceptions/Unchecked #SRS

# What happens if you call `Iterator.next` without calling `hasNext` first?

> [!abstract] Short answer
> **It is legal.** `next()` returns the next remaining element. If none remain, it throws `NoSuchElementException`. `hasNext()` is only the safe preview (`true` iff `next()` would not throw). It is not a required preamble [[How would you explain how many elements will if Iterator.next will 10 Iterator.hasNext]].

## `next` does not demand `hasNext`

`Iterator.next()`: “Returns the next element in the iteration. Throws `NoSuchElementException` if the iteration has no more elements.” No clause requires a prior `hasNext()` [[What is the Iterator interface and why do Java collections use it]], [[What is NoSuchElementException]].

`hasNext()`: `true` if `next()` would return an element rather than throw. Repeating `hasNext()` does not consume elements [[How would you explain how many elements will if Iterator.next will 10 Iterator.hasNext]].

Empty iterator: first `next()` throws. After the last successful `next()`, the following `next()` throws. If one element is still unread, `next()` **returns** it without `hasNext()`.

Enhanced `for` always pairs `hasNext` then `next`. A counted loop `for (int i = 0; i < n; i++) it.next()` is valid when `n` is the remaining size; too large `n` is NSE, not CME.

```d2
direction: down
call: "next() with no hasNext()" {
  width: 280
  height: 50
}
ok: "more elements\n→ value, cursor advances" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
nse: "no more elements\n→ NoSuchElementException" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}

call -> ok
call -> nse
```

**Fig. 1.** The branch is “anything left?”, not “did you call `hasNext`?”

```java
class NextWithoutHasNextFirst {
    static String takeOne(java.util.List<String> list) {
        return list.iterator().next(); // OK if list is non-empty
    }

    static void exhaustThenNext(java.util.Iterator<String> it) {
        while (it.hasNext()) {
            it.next();
        }
        it.next(); // NoSuchElementException
    }
}
```

**Listing 1.** `takeOne` never calls `hasNext`. Empty `list` throws on that `next()`. `exhaustThenNext` is the no-more-elements case.

> [!warning] Exhausted ≠ “sitting on the last element”
> A plain `Iterator` has no current element. NSE means **zero** remaining, not “cursor on the last slot.” The `next()` that reads the last unread element succeeds. After that return, the following `next()` throws. Do not confuse NSE with `ConcurrentModificationException`.

> [!warning] `hasNext()` true is not a reservation
> Another `next()` on the same iterator, or a concurrent drain, can still leave this `next()` with nothing. Nested loops that call `next()` twice per `hasNext()` are the usual `NoSuchElementException` bug.

> [!tip] Interview answer
> **`next()` without `hasNext()` returns the next element or throws `NoSuchElementException` if the iterator is empty or already spent.** You are not required to call `hasNext()` first. `hasNext()` only tells you whether that `next()` would succeed.
