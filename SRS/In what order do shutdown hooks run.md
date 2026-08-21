<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: if several hooks are registered, execution order is unspecified. They may run concurrently because each hook is a `Thread`. Do not assume sequential cleanup or that registration order is start order.
> [!warning] Unverified traps from the dump
> - Sharing mutable state between hooks without synchronization is a race.
> - You cannot order hooks by calling addShutdownHook first or last.
