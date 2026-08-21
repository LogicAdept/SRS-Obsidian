<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: hooks must be registered before shutdown starts. Once the shutdown sequence has begun, `addShutdownHook` fails. They also say you cannot deregister hooks at that point.
> [!warning] Unverified traps from the dump
> - The failure is IllegalStateException once shutdown is in progress.
> - Registering the same Thread instance twice fails even before shutdown (identity, not equals).
