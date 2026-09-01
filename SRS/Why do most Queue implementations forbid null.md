<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS

# Why do most `Queue` implementations forbid `null`?

> [!abstract] Short answer
> **`poll` and `peek` already return `null` to mean empty.** A stored `null` would make that signal ambiguous. Implementations **generally** reject `null` (`ArrayDeque`, `PriorityQueue`, concurrent queues, `BlockingQueue`). `LinkedList` is the named exception; even there you should not queue `null`.

## `null` is the empty-queue sentinel

`Queue` is a collection for holding elements **prior to processing**. Insert, remove-head, and examine-head each have a throwing form and a special-value form. The special-value retrieve/inspect pair is `poll` / `peek`: both return **`null` when the queue has no head** [[What are the two method families on Queue]] [[What is the Queue interface in Java]].

Because of that sentinel, implementations **generally do not allow** inserting `null`. Even a type that *can* store `null` should not put one in a `Queue`: you could not tell “no element” from “a null element.”

That is why the usual JDK queues throw `NullPointerException` on insert:

- `ArrayDeque` — **null elements are prohibited**; `offer` / `offerFirst` / `offerLast` specify NPE if the element is `null`
- `PriorityQueue` — **does not permit `null`**; `offer` / `add` NPE; empty `poll` returns `null` [[Does PriorityQueue allow null]]
- `ConcurrentLinkedQueue` / `ConcurrentLinkedDeque` — no `null`s [[What is ConcurrentLinkedQueue]]
- `BlockingQueue` — no `null`; `null` is the sentinel for failed `poll` (including timed `poll`) [[What makes a BlockingQueue blocking]]

`LinkedList` (since 1.2) implements `List` and `Deque` and **permits all elements, including `null`**. Its `Queue` methods arrived in 1.5; `offer` does not throw on `null`, and `poll` / `peek` still return `null` when empty — so a stored `null` collides with the empty signal.

```d2
direction: down
insert: "offer / add" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
npe: "typical Queue\nNPE — null not stored" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
empty: "poll / peek\nnull means no head" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ambig: "LinkedList can store null\npoll/peek still return null" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

insert -> npe
insert -> empty: "after drain"
insert -> ambig: "LinkedList only"
```

**Fig. 1.** On queues that reject `null`, `poll() == null` is empty. On `LinkedList`, that test is not enough.

```java
import java.util.ArrayDeque;
import java.util.LinkedList;
import java.util.Queue;

class QueueForbidsNull {
    static void demo() {
        Queue<String> q = new ArrayDeque<>();
        System.out.println(q.poll() == null); // true — empty
        q.offer("a");
        System.out.println(q.poll());         // a
        // q.offer(null);                     // NullPointerException

        Queue<String> list = new LinkedList<>();
        list.offer(null);
        System.out.println(list.isEmpty());      // false
        System.out.println(list.peek() == null); // true — stored null, not empty
    }
}
```

**Listing 1.** Java 5+ `Queue`. `ArrayDeque.offer(null)` is the NPE path from the spec (commented so the listing runs). `LinkedList.offer(null)` succeeds; `peek() == null` is then **not** “empty.”

> [!warning] `poll() == null` is not “empty” on `LinkedList`
> A queued `null` and an empty list both make `poll` / `peek` return `null`. Use `isEmpty()` or the throwing family (`remove` / `element`), or do not store `null`.

> [!warning] `ArrayDeque` does not allow `null`
> Null elements are prohibited. `offer` throws `NullPointerException`. Do not treat a `Deque`/`List` that permits `null` as the `ArrayDeque` rule.

> [!tip] Interview answer
> **Most `Queue` implementations forbid `null` because `poll` and `peek` already use `null` to mean empty.** `ArrayDeque`, `PriorityQueue`, concurrent queues, and `BlockingQueue` throw on insert. **`LinkedList` still permits `null` as a `List`; do not use that as a queue element.** Prefer a queue that rejects `null`, or check `isEmpty()` instead of `poll() == null`.
