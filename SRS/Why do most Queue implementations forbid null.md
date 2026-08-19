<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `null` is overloaded as the “queue is empty” signal: `poll()` and `peek()` return `null` when there is nothing to return. Allowing a real `null` element would make that signal ambiguous.

```java
Queue<String> q = new ArrayDeque<>();
q.offer(null); // NullPointerException
q.poll();      // null only ever means “empty”
```

Dump: `ArrayDeque`, `PriorityQueue`, `ConcurrentLinkedQueue`, and the blocking queues all reject `null`. The lone exception is **`LinkedList`** (a pre-`Queue` class).

Same dump on `ArrayDeque` specifically: no-null keeps the returning-value method family unambiguous.

> [!warning] Unverified traps from the dump
> - `LinkedList` as a queue still permits `null`; dumps treat that as a reason not to use it as a queue.
> - Another compilation wrongly claimed `ArrayDeque` allows null — do not treat that as the dump used here.
