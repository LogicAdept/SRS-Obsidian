<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: do not call `System.exit(0)` from a hook. After shutdown has started, a zero-status `exit` can hang the process because `exit` waits for the shutdown sequence that is already running that hook.

They say a non-zero status or a halt-style call can force termination instead.
> [!warning] Unverified traps from the dump
> - Dumps sometimes write System.halt; the API is Runtime.halt, not a System method.
> - Calling System.exit from a hook can deadlock the shutdown sequence.
