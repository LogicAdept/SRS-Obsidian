<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump recommended async option: DelegatingSecurityContextExecutor wraps another Executor and captures SecurityContext at submit, then restores it on the worker thread for the task.
> [!warning] Unverified traps from the dump
> - It does not make ThreadLocal magically global. Tasks you submit without this wrapper still see an empty holder.
