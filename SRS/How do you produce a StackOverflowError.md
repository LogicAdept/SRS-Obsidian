<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps generate `StackOverflowError` with unbounded recursion: a method that calls itself with no terminating base case (example: `recursivePrint` incrementing an int, or a static `m()` that only calls `m()`).

Each call consumes stack frames until the thread's stack is full. Java Runtime then throws `java.lang.StackOverflowError`.

Dump contrast: filling the heap with retained objects is `OutOfMemoryError: Java Heap Space`, not stack overflow.
> [!warning] Unverified traps from the dump
> - A tight infinite loop without new frames does not grow the Java stack the way recursion does.
> - Some dump titles say StackOverflowException; the type is StackOverflowError.
