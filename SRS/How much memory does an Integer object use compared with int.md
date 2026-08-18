<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps contrast `int` as 4 bytes of raw value with `Integer` as a heap object of about 16–20 bytes because of the object header (plus the wrapped `int`). Wrappers are slower due to allocation and GC. That overhead is why dumps tell you not to use `Integer`/`Long` as loop accumulators.

> [!warning] Unverified traps from the dump
> - The 16–20 byte figure is a dump approximation; it depends on JVM, compressed oops, and alignment.
> - Cached small `Integer`s are reused, so not every boxing allocates a fresh object.
