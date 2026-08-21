<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: hooks run on normal exit (last non-daemon thread ends or `System.exit`) and on many orderly signals (Ctrl+C, SIGTERM). They do not run if `Runtime.halt` is called or if the OS sends SIGKILL / TerminateProcess. A JVM crash can also skip them.

SIGTERM may start hooks, but the OS can still kill the process before they finish.
> [!warning] Unverified traps from the dump
> - Popular lie: shutdown hooks always run when the JVM exits.
> - Long or blocking hooks can be cut off when the OS imposes a shutdown timeout.
