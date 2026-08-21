<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`Throwable` is the root of everything that can be thrown or caught. It splits into `Error` (serious JVM/system problems dumps say not to handle in application code) and `Exception` (conditions a program may recover from). `Exception` is one branch, not the whole tree, so `catch (Exception e)` misses `Error`.
> [!warning] Unverified traps from the dump
> - Saying all exceptions extend Exception is false for Error and for Throwable itself.
> - RuntimeException sits under Exception, so it is an Exception even though it is unchecked.
