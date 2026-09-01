<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/ArrayDeque #SRS

> [!abstract] Short answer
> **Call `push`, `pop`, and `peek` on a `Deque` — they all hit the head, which gives LIFO.** `push(e)` is `addFirst(e)`, `pop()` is `removeFirst()`, and the method named `peek()` is `peekFirst()` (returns `null` if empty). Prefer `ArrayDeque` over legacy `Stack`. The throwing inspect that matches old `Stack.peek` is `getFirst()`, not `Deque.peek()`.

## Head is the top

A deque is a double-ended queue. Used as a **queue**, you insert at the tail and take from the head (FIFO). Used as a **stack**, you insert **and** take at the **beginning** — Last-In-First-Out. That is why `Deque` is the replacement type for `java.util.Stack` ([[Why is java.util.Stack discouraged and what should you use instead]], [[What is the difference between a Queue and a Stack]]).

The usual concrete type is `ArrayDeque`: resizable array, no capacity cap, **no nulls**, not thread-safe, and most end operations (including `push` / `pop` / `peek`) run in **amortized constant time**. It is the implementation the API calls out as likely faster than `Stack` for this job. `LinkedList` is also a `Deque`, but that is a different trade-off ([[What is the difference between ArrayDeque and LinkedList as a Deque]]).

```d2
direction: right
push: "push(e)" {
  width: 140
  height: 55
  style.fill: "#e8f5e9"
}
pop: "pop()" {
  width: 140
  height: 55
  style.fill: "#ffebee"
}
peek: "peek()" {
  width: 140
  height: 55
  style.fill: "#fff8e1"
}
head: "deque head\n(first element = top)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
push -> head: "addFirst"
pop -> head: "removeFirst"
peek -> head: "peekFirst"
```

**Fig. 1.** Stack protocol on a `Deque`: every stack call is a first/head call. Queue `add` / `offer` still go to the **tail** — do not mix the two if you mean a stack.

`pop()` throws `NoSuchElementException` on an empty deque (`removeFirst`). `peek()` does **not**: it returns `null` (`peekFirst`). The throwing examine-head methods are `getFirst()` and `element()`. That split is the same two families as on `Queue` ([[What are the two method families on Queue]], [[What are the First and Last methods on Deque]]).

The interface’s **Stack-to-Deque mapping table** lists `peek()` → `getFirst()`. That row is the legacy `Stack.peek` contract (throw if empty). The method actually named `peek` on `Deque` is the `Queue` method and stays `peekFirst`.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.NoSuchElementException;

class DequeAsStack {
    static void demo() {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(1);              // addFirst: head → 1
        stack.push(2);              // addFirst: head → 2, then 1
        Integer top = stack.peek(); // 2, still [2, 1]
        Integer popped = stack.pop(); // 2, now head → 1

        Deque<Integer> empty = new ArrayDeque<>();
        Integer missing = empty.peek(); // null — not an exception
        try {
            empty.pop();            // NoSuchElementException
        } catch (NoSuchElementException expected) {
            // pop is removeFirst
        }
        try {
            empty.getFirst();       // also throws — Stack.peek equivalent
        } catch (NoSuchElementException expected) {
            // throwing inspect of the head
        }
    }
}
```

**Listing 1.** `ArrayDeque` as a stack. Iterator / `toString` order is head-to-tail, which is also pop order. `peek` on empty is `null`; `pop` / `getFirst` throw.

On a capacity-restricted `Deque`, `push` can throw `IllegalStateException` when full (`addFirst`). `ArrayDeque` grows instead; it still rejects `null` with `NullPointerException`. Because `ArrayDeque` forbids null elements, a `null` from `peek` / `pollFirst` means empty, not a stored null.

> [!warning] `Deque.peek()` does not throw
> Empty `pop()` throws `NoSuchElementException`. Empty `peek()` returns `null`. Treating `peek` as the throwing family — or as different from `peekFirst` — is wrong. For a throwing look at the top, call `getFirst()` (or `element()`).

> [!warning] Do not `add` when you meant `push`
> `add` / `offer` are tail inserts (`addLast` / `offerLast`). `push` is a head insert. Mixing them on one deque is neither a clean stack nor a clean queue. Stay on `push` / `pop` / `peek` (or the `*First` names) for LIFO.

> [!tip] Interview answer
> Use a `Deque`, almost always `ArrayDeque`, and talk to the head: `push` is `addFirst`, `pop` is `removeFirst`, `peek` is `peekFirst`. That is LIFO and the replacement for `java.util.Stack`. `pop` throws on empty; `peek` returns `null` — if you want the old throwing peek, call `getFirst`.
