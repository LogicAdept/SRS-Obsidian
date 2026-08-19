<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: every core `Queue` operation comes in two flavours — one that **throws** on failure and one that returns a special value (`false` or `null`). Use the throwing form when failure is a bug; use the returning form when emptiness/fullness is expected control flow.

| Operation | Throws on failure | Returns special value |
| --- | --- | --- |
| Insert | `add(e)` (`IllegalStateException` if full) | `offer(e)` (`false`) |
| Remove head | `remove()` (`NoSuchElementException` if empty) | `poll()` (`null`) |
| Examine head | `element()` (`NoSuchElementException` if empty) | `peek()` (`null`) |

```java
Queue<Integer> q = new ArrayDeque<>();
q.poll();   // null — empty, no exception
q.remove(); // NoSuchElementException
q.peek();   // null
q.element(); // NoSuchElementException
```

Dump: `offer` / `poll` / `peek` are the safer default for bounded/concurrent queues where failure is normal.

> [!warning] Unverified traps from the dump
> - Empty-stub card `What is the peek method on stacks queues or streams` is a different cue (peek across stack/queue/stream).
> - `poll() == null` means empty only if the queue forbids null elements.
