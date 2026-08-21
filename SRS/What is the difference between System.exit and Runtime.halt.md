<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `System.exit` starts an orderly shutdown: registered shutdown hooks run, then the VM stops. `Runtime.halt` terminates immediately and does not start hooks or wait for hooks that are already running. halt can abort a shutdown that is already in progress.
> [!warning] Unverified traps from the dump
> - System.exit(n) is Runtime.getRuntime().exit(n), not halt.
> - By convention a nonzero status means abnormal termination for both exit and halt.
> - Dumps treat halt as the escape when a hook deadlocks; it skips cleanup.
