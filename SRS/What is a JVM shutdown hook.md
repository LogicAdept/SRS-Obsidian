<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: a shutdown hook is an initialized but unstarted `Thread` registered with `Runtime.getRuntime().addShutdownHook(hook)`. The JVM starts it when shutting down so the process can clean up or save state.

Typical dump registration:

```java
Runtime.getRuntime().addShutdownHook(new Thread(() -> {
    // cleanup
}));
```
> [!warning] Unverified traps from the dump
> - The hook thread must not already be started; the JVM starts it.
> - Dumps call hooks more reliable than finalize; finalize is a separate, discouraged mechanism.
