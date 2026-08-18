<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **no.** While a for-each loop is running, you **cannot modify** the collection.

A related dump’s single-thread CME sample does exactly that: enhanced-for over an `ArrayList`, then `list.remove(...)` inside the loop.

> [!warning] Unverified traps from the dump
> - For-each is implemented with an `Iterator`. Structural `Collection.remove` is the usual `ConcurrentModificationException` story, not a separate for-each rule.
> - `Iterator.remove()` after `next()` is the dump’s allowed way to delete during iteration — that is not the enhanced-for body calling `list.remove`.
