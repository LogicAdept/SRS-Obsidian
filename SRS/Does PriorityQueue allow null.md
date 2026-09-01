<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS

# Does `PriorityQueue` allow `null`?

> [!abstract] Short answer
> **No.** A `PriorityQueue` **does not permit `null` elements.** `offer` / `add` throw `NullPointerException`. Copy constructors throw if the source collection, or any of its elements, is `null`. That is stricter than “queues in general”: most `Queue`s reject `null`, but `LinkedList` is a documented exception.

## Forbidden as an element, used as empty

`PriorityQueue` is a heap-backed unbounded queue. Its class contract states it does not permit `null` elements. `offer(E)` and `add(E)` both specify `NullPointerException` if the element is `null`. OpenJDK `offer` is a null check first, then `siftUp` — `null` never enters the heap [[What is java.util.PriorityQueue]].

The `Queue` contract explains why: implementations **generally** do not allow `null`, because `poll()` (and `peek()`) return `null` to mean **empty**. Inserting `null` would make “no element” indistinguishable from “a null element.” Even types that permit `null` should not put one in a `Queue` [[Why do most Queue implementations forbid null]].

`PriorityQueue.poll()` / `peek()` follow that sentinel: empty → `null`. OpenJDK `poll` treats a `null` in `queue[0]` as empty (`if ((result = queue[0]) != null)`), which is another reason a stored `null` cannot be a legal element.

```d2
direction: down
insert: "offer / add / collection ctor" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
npe: "element == null\nNullPointerException" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
ok: "non-null element\nheap insert" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
empty: "poll / peek on empty\nreturn null (not an element)" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

insert -> npe
insert -> ok
ok -> empty: "after drain"
```

**Fig. 1.** `null` as an insert is a failure. `null` from `poll`/`peek` means the queue has no head.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

class PriorityQueueNull {
    static void demo() {
        PriorityQueue<String> pq = new PriorityQueue<>();
        pq.offer("ok");
        // pq.offer(null);           // NullPointerException
        // pq.add(null);             // same: add delegates to offer
        new PriorityQueue<>(List.of("a", "b")); // ok — List.of itself rejects null

        ArrayList<String> withNull = new ArrayList<>();
        withNull.add("a");
        withNull.add(null);
        // new PriorityQueue<>(withNull); // NullPointerException — null element in source

        pq.clear();
        System.out.println(pq.poll() == null); // true — empty sentinel, not a stored null
        System.out.println(pq.contains(null)); // false — OpenJDK does not throw
    }
}
```

**Listing 1.** Live lines run. Commented inserts are the NPE paths from the Java SE spec (`offer`/`add` and the collection constructor). `List.of` cannot even build a null-containing list; an `ArrayList` that holds `null` still fails when copied into a `PriorityQueue`. OpenJDK `contains(null)` / `remove(null)` do not throw: `indexOf` skips a `null` probe and reports not found.

A `null` **comparator** is legal and means natural ordering (`comparator()` returns `null`). That is not a `null` element. Natural ordering still forbids non-`Comparable` inserts (`ClassCastException`) [[What does PriorityQueue require of its elements]].

`Queue` names `LinkedList` as an implementation that does **not** prohibit `null`. `PriorityQueue` is not that exception. Do not use `LinkedList`’s permission as a `PriorityQueue` rule [[Does LinkedList implement Queue and Deque in Java]].

> [!warning] Empty `poll` is `null`; that is not “nulls are allowed”
> `peek()` / `poll()` returning `null` means **no head**. It is the reason `offer(null)` is rejected, not evidence that the heap can hold `null`.

> [!warning] `null` comparator ≠ `null` element
> Passing `null` as the comparator (or seeing `comparator() == null`) selects natural order. `offer(null)` still throws.

> [!tip] Interview answer
> **No. `PriorityQueue` does not allow `null` elements — `offer`/`add` throw `NullPointerException`.** `poll`/`peek` use `null` to mean empty, which is why most queues forbid `null`. **`LinkedList` as a `Queue` is the usual exception; still do not put `null` in a queue.**
