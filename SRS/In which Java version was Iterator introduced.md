<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`Enumeration` — JDK 1.0.** **`Iterator` — JDK 1.2.**

Same dump: Enumeration is for legacy `Vector`, `Stack`, `Hashtable`. Iterator is for the collections framework (`ArrayList`, `HashSet`, `HashMap`, `LinkedList`, …). Method rename: `hasMoreElements` / `nextElement` vs `hasNext` / `next`, plus `remove()` on Iterator.

> [!warning] Unverified traps from the dump
> - `ListIterator` is also a 1.2 collections-framework cursor in the same dumps; `Spliterator` is a later (Java 8) dump item.
