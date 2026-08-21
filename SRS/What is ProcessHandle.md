<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: launching a command gives you a `Process`. From Java 9 you can also use `ProcessHandle` as a more modern view of that OS process: characteristics, status, and related process control, while I/O still goes through `Process`.
> [!warning] Unverified traps from the dump
> - ProcessHandle is Java 9+; older dumps only mention Process from exec.
> - Destroying the Java process does not always kill children unless you arrange that.
