<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #Java/Collections/List/Vector #Java/Streams/Operations/Intermediate #SRS

# What is the `peek` method on stacks, queues, or streams in Java?

> [!abstract] Short answer
> **Three different APIs share the name.** On a `Queue`/`Deque`, `peek` **looks at the head without removing it** (`null` if empty). On `java.util.Stack`, `peek` looks at the **top** and **throws** if empty. On a `Stream`, `peek` is an **intermediate** debug hook (`Consumer`); it is not a head inspect.

## Look vs debug hook

`Queue.peek()` retrieves, but does not remove, the head, or returns `null` if empty. The throwing twin is `element()` (`NoSuchElementException`). Same split as `poll` vs `remove()` [[What are the two method families on Queue]] [[What is the Queue interface in Java]] [[Why do most Queue implementations forbid null]].

On a `Deque`, `peek` is **exactly** `peekFirst()`: first element, or `null` if empty. That is also the stack mapping: when a deque is used as a stack, `peek` still reads the **beginning** (same as queue) [[What is the Deque interface in Java]] [[What are the First and Last methods on Deque]] [[What is the difference between a Queue and a Stack]].

`java.util.Stack.peek()` looks at the top without popping. Empty → `EmptyStackException`, not `null`. Prefer `Deque`/`ArrayDeque` over legacy `Stack`.

`Stream.peek(Consumer)` returns a stream that runs the action as elements are **consumed** from the result. Intermediate, mainly for **debugging** (see values as they pass a pipeline point). In parallel, the action may run on whatever thread the upstream uses. If the pipeline **elides** elements (`findFirst`, `count()` when it can skip traversal), the action **is not** called for those elements.

```d2
direction: down
name: "peek" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
q: "Queue / Deque\nhead, no remove; null if empty" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
st: "Stack\ntop, no pop; throws if empty" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
s: "Stream\nintermediate Consumer; debug" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

name -> q
name -> st
name -> s
```

**Fig. 1.** Same word, three contracts. Do not treat `Stream.peek` as `Queue.peek`.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Queue;
import java.util.stream.Stream;

class PeekMeanings {
    static void demo() {
        Queue<Integer> q = new ArrayDeque<>();
        System.out.println(q.peek()); // null — empty
        q.offer(1);
        System.out.println(q.peek()); // 1 — still in the queue
        System.out.println(q.poll()); // 1

        Deque<Integer> d = new ArrayDeque<>();
        d.push(2);
        System.out.println(d.peek()); // 2 — first end; does not pop

        Stream.of("one", "two", "three", "four")
            .filter(e -> e.length() > 3)
            .peek(e -> System.out.println(e)) // three, four — debug
            .map(String::toUpperCase)
            .forEach(e -> {});
    }
}
```

**Listing 1.** Java 8+. `Queue`/`Deque.peek` inspect the head. `Stream.peek` only runs because `forEach` consumes the pipeline.

> [!warning] `Stream.peek` is not “look at the first element”
> It does not return the head. It is not a terminal operation. Short-circuit or `count()` optimizations can skip the action.

> [!warning] Empty `Queue.peek` is `null`; empty `Stack.peek` throws
> `poll() == null` / `peek() == null` also collide with a stored `null` on `LinkedList`. `element()` / `getFirst()` throw instead.

> [!tip] Interview answer
> **`Queue.peek` inspects the head without removing it (`null` if empty); `element()` throws.** `Deque.peek` is `peekFirst` (stack or queue). **`Stream.peek` is a debug intermediate `Consumer`, not a collection inspect — and it may not run for every element.**
