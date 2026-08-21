<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `NoSuchElementException` is a common unchecked exception (`RuntimeException`) thrown by accessors when the requested element does not exist — `Iterator.next()` without a remaining element, `Queue.remove()` / `element()` on an empty queue, `Optional.get()` on empty.
> [!warning] Unverified traps from the dump
> - Empty Optional.get() is NoSuchElementException, not NullPointerException.
> - Queue.poll() / peek() return null on empty instead of throwing.
