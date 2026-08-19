<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/ArrayDeque #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `Deque` provides `push`, `pop`, and `peek`, which operate on the **head** as a LIFO stack: `push` is `addFirst`, `pop` is `removeFirst`, `peek` is `peekFirst`.

```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); // [1]
stack.push(2); // [2, 1]  (head is the top)
stack.peek();  // 2
stack.pop();   // 2 → [1]
```

Dump: both ends are O(1). Note `pop` / `peek` here throw `NoSuchElementException` on an empty deque (unlike `poll` / `peekFirst`, which return `null`).

> [!warning] Unverified traps from the dump
> - Sibling dump “replace `Stack` with `ArrayDeque`” already exists untagged on `#Java/Collections`; this card is the `push`/`pop` mapping.
> - Dump `peek()` on a stack-shaped `Deque` is the throwing family, not `peekFirst()`.
