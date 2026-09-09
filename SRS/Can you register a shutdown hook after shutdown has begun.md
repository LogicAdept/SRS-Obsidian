<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# Can you register a shutdown hook after shutdown has begun

> [!abstract] Short answer
> No. Registration **and** de-registration are prohibited once the shutdown sequence has begun: both `Runtime.addShutdownHook(hook)` and `Runtime.removeShutdownHook(hook)` throw `IllegalStateException` at that point. Hooks must be registered during normal operation — typically at startup, right after the resource they are meant to clean up.

The sequence begins on the first `exit` call, when the last non-daemon thread ends, or when an external event such as SIGINT or SIGTERM arrives. From that moment the set of hooks is frozen; the JVM starts exactly what was registered before and waits for all of it to terminate.

## What still throws and what still works

A duplicate registration of the same thread (compared with `==`) throws `IllegalArgumentException` even in normal times, and the hook thread must be unstarted. Starting brand-new threads during the shutdown, in contrast, remains legal — new threads run concurrently with the hooks — it is only the hook set itself that can no longer change.

```java
public class RegisterHookDuringShutdownDemo {
    public static void main(String[] args) {
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            try {
                Runtime.getRuntime().addShutdownHook(new Thread(() -> {}, "late"));
                System.out.println("hook: late hook registered");
            } catch (IllegalStateException e) {
                System.out.println("hook: caught " + e.getClass().getSimpleName());
            }
        }));
        System.out.println("main done");
    }
}
// Output (JDK 21):
// main done
// hook: caught IllegalStateException
```

**Listing 1.** A hook trying to register one more hook during the sequence catches `IllegalStateException`; the JVM then exits normally once the hooks finish.

> [!warning] Lazy registration is a hidden bug
> A library that registers its hook on first use — inside a lazy singleton or a static initializer triggered by the first request — loses that cleanup forever whenever shutdown beats the first use. Frameworks you embed can hit this on fast-failing starts: the process gets SIGTERM mid-init, the not-yet-registered hook is rejected, and resources leak. Register eagerly at startup, or catch the `IllegalStateException` where lateness is possible.

The frozen-hook-set rule also explains why `removeShutdownHook` is equally unavailable at shutdown — you cannot unregister a hook to skip its cleanup either. Related traps: [[What happens if you call System.exit from a shutdown hook]] for the exit-inside-hook hang, and [[What is a JVM shutdown hook]] for the full lifecycle; [[When does a JVM shutdown hook not run]] lists the cases where even a registered hook never starts.

> [!tip] Interview answer
> No — once the shutdown sequence has started, `addShutdownHook` and `removeShutdownHook` both throw `IllegalStateException`; the hook set is frozen. Register hooks at startup, keep them quick and thread-safe, and if a component can be shut down before it finished initializing, either register its hook eagerly or be ready to catch the rejection.

