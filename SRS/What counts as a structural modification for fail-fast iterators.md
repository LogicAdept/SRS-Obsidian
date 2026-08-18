<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **structural modification** means **adding, removing, or updating** any element of the collection **while a thread is iterating** it. Fail-fast iterators throw `ConcurrentModificationException` on that.

Dump mechanism: keep a **modification count**; if the iterating thread sees the count change, it throws `ConcurrentModificationException`.

> [!warning] Unverified traps from the dump
> - The dump lumps **update** together with add/remove. Other collection dumps treat replacing a `HashMap` value (key already present) as **not** structural.
> - `Iterator.remove()` after `next()` is the usual dump exception to “do not modify during iteration.”
