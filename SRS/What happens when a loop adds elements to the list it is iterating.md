<!--
reps: 0
priority: 0
-->
#Career/Interview/Exercises #Java/Collections/Iteration/FailFast #Java/Collections/List/ArrayList #Java/Exceptions/Error #SRS

# What happens when a loop adds elements to the list it is iterating?

> [!abstract] Short answer
> **Two different failures.** An enhanced `for` loop dies with `ConcurrentModificationException` on the iterator's second `next()` — `list.add(0, 1)` is a structural modification the iterator did not make. An index loop `for (int i = 0; i < list.size(); i++) { list.add(0, 2); }` **never ends by its own condition**: `size` grows by one per iteration, so it stops only when the JVM can no longer allocate and throws `OutOfMemoryError` — an `Error`, not an `Exception`.

## The enhanced for fails fast

```java
List<Integer> list = new ArrayList<>();
list.add(0);

for (Integer integer : list) {          // enhanced for = hidden iterator
    list.add(0, 1);                     // structural modification, not via the iterator
}

for (int i = 0; i < list.size(); i++) {
    list.add(0, 2);                     // bounded by nothing: size grows with i
}

System.out.println(list.get(1));        // never reached
```

**Listing 1.** As written, the method dies in the first loop; with that loop removed or caught, the second loop runs until memory is gone.

Trace the first loop: the hidden iterator's first `next()` returns `0`; the body adds `1`, bumping `modCount` and `size` to 2; `hasNext()` — which in `ArrayList` does **not** inspect `modCount` — still sees `cursor != size`; the second `next()` runs `checkForComodification` and throws [[What is ConcurrentModificationException]]. Fail-fast detection is **best-effort** and does not require a second thread [[How can a single-threaded program get ConcurrentModificationException]] [[What counts as a structural modification for fail-fast iterators]].

```d2
direction: down
fe: "enhanced for\nhidden Iterator" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
add1: "list.add(0, 1)\nmodCount++  size++" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
cme: "second next()\nmodCount mismatch\nConcurrentModificationException" {
  width: 300
  height: 75
  style.fill: "#ffebee"
}
idx: "index loop\ni < list.size()" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
inv: "i == k, size == s + k\ncondition stays true" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
grow: "backing Object[] keeps growing\nadd(0, 2) shifts every element" {
  width: 310
  height: 65
  style.fill: "#fff3e0"
}
oom: "heap exhausted\nOutOfMemoryError" {
  width: 260
  height: 55
  style.fill: "#ffebee"
}

fe -> add1
add1 -> cme
idx -> inv
inv -> grow
grow -> oom
```

**Fig. 1.** The iterator path ends in a `ConcurrentModificationException`; the index path ends in memory exhaustion.

## How far the index loop goes

After `k` iterations `i == k` and `size == s + k` for the starting size `s`, so `i < list.size()` holds for every `k` — the loop cannot terminate through its own condition. Each `add(0, 2)` also shifts every existing element one slot right, so the total work grows quadratically and the loop visibly slows down as the list grows. The literal `2` autoboxes to a **cached** `Integer`, so the allocation pressure comes from the growing `Object[]` backing array and its grow-copies, not from boxing [[Does ArrayList always add elements in O(1) time]]. The end is the JVM throwing `OutOfMemoryError` when it cannot allocate an object and the garbage collector cannot make more memory available — usually reported as *Java heap space* — long before `ArrayList` reaches its `Integer.MAX_VALUE`-scale element ceiling [[How would you explain StackOverflowError OutOfMemoryError]].

> [!warning] "Infinite" is not forever, and CME is not a guarantee
> The index loop ends in an `Error`, not an `Exception` — a surrounding `catch (Exception e)` will not stop it. And the fail-fast `ConcurrentModificationException` is a best-effort bug detector, not a promise: correctness must not depend on catching it.

## How you avoid each failure

An in-walk **add** to a list goes through `ListIterator.add`, not `list.add`; an in-walk remove goes through `Iterator.remove` or `removeIf` [[Can you modify a collection while iterating with a for-each loop]] [[How do you avoid ConcurrentModificationException while iterating a collection]]. Building a batch is cleaner still: collect the new elements in a side list and `addAll` after the walk. For the index loop, hoist the bound once — or do not add to the very list whose `size` you are measuring.

```java
int n = list.size();              // read the bound once
for (int i = 0; i < n; i++) {
    list.add(0, 2);               // exactly n iterations
}
```

**Listing 2.** Capturing the bound makes the loop terminate: it runs `n` times and stops.

> [!tip] Interview answer
> **The first loop throws `ConcurrentModificationException` on the second `next()`** — the body's `add` is a structural modification the iterator did not make. **The index loop never terminates by itself**: `size` grows exactly as fast as `i`, so the condition holds forever, and the run ends only when the heap is exhausted and the JVM throws `OutOfMemoryError` — the iteration count is bounded by memory, not by the loop condition.
