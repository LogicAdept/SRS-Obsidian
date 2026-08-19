<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** `PriorityQueue` does not allow `NULL` objects. Like other queues, not `null`.

Sibling dump: `offer(null)` on typical queues is `NullPointerException` because `poll`/`peek` use `null` as empty.

> [!warning] Unverified traps from the dump
> - `LinkedList` as a `Queue` is the usual null-permitting exception, not `PriorityQueue`.
> - Empty stub `What is java.util.PriorityQueue` already exists; do not treat this as that definition card.
