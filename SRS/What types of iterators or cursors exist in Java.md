<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Java has **four** iterators / cursors:

- `Enumeration`
- `Iterator`
- `ListIterator`
- `Spliterator` (dump spelling: “Spilterator”)

Dump nicknames: `Iterator` is the **universal cursor** (any collection, read + remove, **forward only**). `ListIterator` is the **most powerful** cursor: bidirectional, read / remove / **replace** / **add**, but **only for `List`**. `Enumeration` is the legacy cursor (read-only). `Spliterator` is listed as the fourth type; another dump: it describes **characteristics** for **parallel** processing (Java 8).

> [!warning] Unverified traps from the dump
> - One compilation misspells `Spliterator`.
> - “Universal cursor” is dump jargon, not an API type.
