<!--
reps: 0
priority: 0
-->
#Java/Collections/List/Vector #Java/Collections/Queues/ArrayDeque #SRS

> [!abstract] Short answer
> **`Stack` is a Java 1.0 `Vector` with five LIFO methods on the last slot.** `push` is `addElement`; `peek` / `pop` read (and `pop` then removes) `elementAt(size - 1)`. It is a `List` and it is synchronized because `Vector` is. Prefer a `Deque`, usually `ArrayDeque` — not because `Stack` is `@Deprecated` (it is not), but because `Deque` is the complete LIFO API without the `Vector` contract.

## How: last index is the top

`Stack` extends `Vector`. The five extra methods are `push`, `pop`, `peek`, `empty`, and `search`. The top of the stack is the **last** component of the vector, not the first. `push(item)` has exactly the same effect as `addElement(item)`. Empty `peek` / `pop` throw `EmptyStackException`. `search` returns a **1-based** distance from the top (`1` is the topmost item) or `-1`.

That is LIFO only by convention. Because `Stack` is-a `Vector`, it is also a `List` and `RandomAccess`: `get(i)`, `add(index, e)`, `set`, and the rest remain. You can reach under the top. A stack ADT would not offer that ([[What is the difference between a Queue and a Stack]]).

```d2
direction: right
vec: "Vector / List\nindexed array, synchronized" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
st: "Stack\npush/pop/peek/empty/search\ntop = last index" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
dq: "Deque + ArrayDeque\nLIFO at the head, no Vector" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
vec -> st: "extends (1.0)"
st -> dq: "prefer (1.6+)"
```

**Fig. 1.** Inheritance made a growable array look like a stack. `Deque` is composition of LIFO operations, not a `List` subclass ([[How do you use a Deque as a stack]]).

## Why it looks that way — and why you still replace it

`Stack` dates from **1.0**, before the Collections Framework (`List` retrofit on `Vector` is 1.2) and before `Deque` (**1.6**). The cheap reuse was: take `Vector`, append at the end, call that a stack.

`Vector` is synchronized, unlike the later collection implementations. `Stack.push` itself is not a `synchronized` method, but it only calls `addElement`, which is. `pop` / `peek` / `search` are `synchronized`; `empty()` delegates to `size()`. The dump story “partially synchronized except `push`” is the wrong takeaway: you still pay `Vector`’s per-call lock, and you still inherit every `List` mutator. For a local stack that tax is wasted; `ArrayDeque` is not thread-safe and is the type the API shows as likely faster when used as a stack.

`Deque` is documented as the more complete, consistent LIFO set and **should be used in preference** to `Stack`. The class javadoc’s example is `Deque<Integer> stack = new ArrayDeque<>()`. Empty `Deque.pop` throws `NoSuchElementException`; `Deque.peek` returns `null` — different from `EmptyStackException` on `Stack.peek` / `pop` ([[Why is java.util.Stack discouraged and what should you use instead]]).

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.EmptyStackException;
import java.util.Stack;

class StackHowWhy {
    static void demo() {
        Stack<Integer> legacy = new Stack<>();
        legacy.push(1);                 // addElement — last slot is top
        legacy.push(2);
        Integer top = legacy.peek();    // 2
        Integer gone = legacy.pop();    // 2
        int dist = legacy.search(1);    // 1 — 1-based distance from top
        Integer under = legacy.get(0);  // 1 — List access, not a stack op

        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(1);
        stack.push(2);

        try {
            new Stack<Integer>().pop();
        } catch (EmptyStackException expected) {
            // not Deque's NoSuchElementException
        }
    }
}
```

**Listing 1.** LIFO at the vector’s end, plus leftover `List` methods. New code uses `Deque` / `ArrayDeque`.

> [!warning] `Stack` is not `@Deprecated`
> The API never retired the class. “Obsolete” in interview talk means **prefer `Deque`**, not an annotation you can quote. `get` / `insert` anywhere still compile.

> [!warning] `search` is not a `List` index
> Distance `1` is the top. `0` is not a valid hit. Absence is `-1`. Mixing `search` with `get(i)` off-by-one is the usual bug.

> [!warning] `push` is not an unsynchronized hole
> `push` is unsynchronized as a method and still mutates through synchronized `addElement`. Do not pick `Stack` for “thread-safe stack” or for “`push` is racy.” For a single-threaded stack, drop the `Vector` locks and use `ArrayDeque`.

> [!tip] Interview answer
> **`Stack` is a 1.0 `Vector`: `push` appends, `peek`/`pop` use the last index, and every `List` method still works.** That is why it is synchronized and why it is a leaky stack. Prefer `Deque`, almost always `ArrayDeque` — the documented replacement since 1.6, not a deprecated tombstone.
