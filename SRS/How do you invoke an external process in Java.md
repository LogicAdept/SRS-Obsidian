<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps say the basic way is `Runtime.getRuntime().exec(...)`. Pass a command string, and optionally a working directory and an environment array of name=value entries. Arguments may be a string array or spaces inside one string.

They recommend `ProcessBuilder` as the more controlled API and claim `exec` uses it internally. Starting a command yields a `Process` (Java 9+ also `ProcessHandle`) for I/O, status, and waiting. The child is a separate OS process, so the command is platform-dependent.
> [!warning] Unverified traps from the dump
> - A single-string exec tokenizes on whitespace, so paths with spaces fail unless you use the array form or ProcessBuilder tokens.
> - Not draining the child's stdout and stderr can fill OS buffers and deadlock the subprocess.
> - Dumps still paste exec-only examples; they also say ProcessBuilder is the preferred, more controllable start path.
