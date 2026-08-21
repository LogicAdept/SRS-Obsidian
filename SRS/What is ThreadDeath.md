<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/Concurrency/Threads #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: calling `Thread.stop()` throws `ThreadDeath`. It is an `Error`, not an `Exception`.

`ThreadDeath` is called a "normal" condition, but applications must still not catch it. Catching it can let a thread continue after `stop()` as if it were alive.

Dump example: a thread's `run` calls `stop()`, catches `ThreadDeath`, and prints that the thread "has died".
> [!warning] Unverified traps from the dump
> - Thread.stop is deprecated/removed in modern JDKs; dumps still use it to explain ThreadDeath.
> - If a static initializer hits ThreadDeath, dumps say no wrapping Error is thrown (unlike other Errors).
