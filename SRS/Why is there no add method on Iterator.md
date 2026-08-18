<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: an iterator’s **only job is to enumerate** a collection. Every collection already has `add()`. Putting `add` on `Iterator` is pointless because a collection **may or may not be ordered**, and `add()` **cannot have the same implementation** for ordered and unordered collections.

> [!warning] Unverified traps from the dump
> - `ListIterator` **does** have `add()`. The dump is about `Iterator`, not every cursor.
> - The dump does not mention fail-fast / `modCount` as the reason.
