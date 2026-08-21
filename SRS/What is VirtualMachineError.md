<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps place `VirtualMachineError` under `Error` as the parent of JVM resource failures, notably `OutOfMemoryError` and `StackOverflowError` (and they mention further subclasses).

It is an Error, so dumps treat it as unchecked and not something application code should catch and recover from.
> [!warning] Unverified traps from the dump
> - OOM and StackOverflowError are VirtualMachineError children, not siblings of Error itself.
> - Linkage failures (NoClassDefFoundError, ExceptionInInitializerError) sit under LinkageError, not VirtualMachineError.
