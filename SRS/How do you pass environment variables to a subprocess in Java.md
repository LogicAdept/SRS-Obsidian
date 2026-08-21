<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `Runtime.exec` can take an environment string array in name=value form plus an optional working directory. They prefer `ProcessBuilder` when you need a controlled environment and I/O for the child.
> [!warning] Unverified traps from the dump
> - That array configures the child process; it does not mutate the current JVM System.getenv map.
> - Passing a non-null envp to exec can drop inherited variables you did not copy.
