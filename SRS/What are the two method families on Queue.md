<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS

# What are the two method families on `Queue`?

> [!abstract] Short answer
> **Throw vs special value.** Insert, remove-head, and examine-head each have both: `add` / `remove` / `element` throw on failure; `offer` / `poll` / `peek` return `false` or `null`. `offer` exists because **capacity-restricted** queues treat “no space” as a normal outcome, not a bug. `poll` / `peek` returning `null` means empty **only if the queue does not store `null`**.

## Throw on failure vs return `false` / `null`

`Queue` adds insert, extract, and inspect beyond `Collection`. Each exists in two forms: one throws if it cannot complete; the other returns a special value (`null` or `false`). The special-value **insert** is designed for capacity-restricted implementations; in most implementations insert cannot fail [[What is the Queue interface in Java]].

| | Throws | Special value |
|---|---|---|
| Insert | `add(e)` → `IllegalStateException` if full | `offer(e)` → `false` |
| Remove head | `remove()` → `NoSuchElementException` if empty | `poll()` → `null` |
| Examine head | `element()` → `NoSuchElementException` if empty | `peek()` → `null` |

`offer` differs from `Collection.add`: `add` can fail only by throwing; `offer` returns `false` when insertion is a **normal** failure (fixed-capacity / bounded queues). `remove()` and `poll()` differ **only** when the queue is empty. `element()` and `peek()` return the head without removing it; they split the same way.

```d2
direction: down
op: "insert / remove head / examine head" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
throw: "add · remove · element\nexception = failure is a bug" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
spec: "offer · poll · peek\nfalse / null = expected miss" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

op -> throw
op -> spec
```

**Fig. 1.** Same three operations, two policies. Bounded producers usually `offer` (or `BlockingQueue.put`); empty consumers use `poll`/`peek` or `take`.

```java
import java.util.ArrayDeque;
import java.util.Queue;

class QueueTwoFamilies {
    static void demo() {
        Queue<Integer> q = new ArrayDeque<>();
        System.out.println(q.poll());  // null — empty
        System.out.println(q.peek());  // null
        // q.remove();   // NoSuchElementException
        // q.element();  // NoSuchElementException
        System.out.println(q.offer(1)); // true — ArrayDeque is not capacity-restricted
        System.out.println(q.add(2));   // true; on a full bounded queue this throws
    }
}
```

**Listing 1.** Java 5+ `Queue`. `ArrayDeque` has no fixed cap, so `add`/`offer` both succeed here. The empty-queue split (`poll`/`peek` vs `remove`/`element`) still shows. A bounded `BlockingQueue` is where `offer` returning `false` matters; `put`/`take` are a **third** pair that **wait** [[How do you implement producer-consumer with a BlockingQueue]].

`Deque` repeats the same two families at **both** ends (`addFirst` vs `offerFirst`, …) and maps `Queue` methods to last-in / first-out [[What are the First and Last methods on Deque]].

`Queue` implementations generally forbid `null`, because `poll` uses `null` to mean empty. `LinkedList` is the named exception; even then you should not insert `null` [[Why do most Queue implementations forbid null]] [[Does PriorityQueue allow null]].

> [!warning] `poll() == null` is not “empty” if the queue holds `null`
> On `LinkedList` as a `Queue`, a stored `null` and an empty queue both make `poll`/`peek` return `null`. Prefer queues that reject `null`, or use `isEmpty()` / the throwing family.

> [!warning] `add` on a full bounded queue is not `offer`
> `add` throws `IllegalStateException`. `offer` returns `false`. For “wait until space,” that is `BlockingQueue.put`, not either `Queue` insert.

> [!tip] Interview answer
> **Every `Queue` mutation/inspect of the head comes in two families: throw (`add`/`remove`/`element`) or special value (`offer`/`poll`/`peek`).** Use `offer` when a full buffer is normal. **`poll`/`peek` return `null` on empty — do not store `null` if you rely on that.**
