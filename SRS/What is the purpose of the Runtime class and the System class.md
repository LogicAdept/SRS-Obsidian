<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps treat `java.lang.Runtime` as the application's handle on the Java runtime system. There is one instance per application; you obtain it with `Runtime.getRuntime()`, not `new`. They list querying memory, requesting GC, `exec`, and shutdown hooks as typical uses.

They treat `java.lang.System` as a static facade for process-level resources: standard input, standard output, standard error, `currentTimeMillis`, and terminating the application.
> [!warning] Unverified traps from the dump
> - Dumps fold heap size and GC request APIs into Runtime; those are JVM memory and collector topics, not this process-level tag.
> - You cannot construct Runtime or System with new. Runtime is a singleton via getRuntime(); System is a non-instantiable static class.
> - System.exit is not a separate shutdown path; dumps that contrast the two classes still have System.exit delegate to Runtime.exit.
