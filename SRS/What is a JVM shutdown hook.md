<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# What is a JVM shutdown hook

> [!abstract] Short answer
> A shutdown hook is an **initialized but unstarted `Thread`** registered with `Runtime.getRuntime().addShutdownHook(hook)`. At the beginning of the shutdown sequence the JVM starts all registered hooks and waits until every one of them terminates; only then does the JVM exit. Hooks are the last chance to flush logs, close pools, or release locks on the way down.

The sequence starts when live non-daemon threads drop to zero, when `System.exit`/`Runtime.exit` is called for the first time, or when an external event such as SIGINT (Ctrl+C) or SIGTERM arrives. Hooks run concurrently with each other and with any daemon or non-daemon threads still alive from before the sequence began — the application is not frozen while hooks work.

## Registration rules and failure behavior

The hook object must be an unstarted thread; registering the **same** thread twice (compared with `==`) throws `IllegalArgumentException`, and any registration or removal after the sequence has begun throws `IllegalStateException`, see [[Can you register a shutdown hook after shutdown has begun]]. An uncaught exception inside a hook is handled by its `UncaughtExceptionHandler`; after the handler completes, the hook is considered terminated normally — other hooks and the exit status are unaffected.

```d2
direction: right
reg: "addShutdownHook(hook)\nunstarted Thread" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
trig: "Shutdown trigger\nexit · last thread ends · signal" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
run: "All hooks started\nconcurrently" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
done: "All hooks terminated\nJVM exits" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
reg -> trig -> run -> done
```

**Fig. 1.** Registration happens during normal operation; the JVM does the starting, waiting, and exiting.

```java
public class ShutdownHookBasicsDemo {
    public static void main(String[] args) {
        Thread hook = new Thread(() ->
                System.out.println("hook: flushing logs and closing resources"));
        Runtime.getRuntime().addShutdownHook(hook);
        System.out.println("main done");
    }
}
// Output (JDK 21):
// main done
// hook: flushing logs and closing resources
```

**Listing 1.** The hook fires on normal `main` termination — the same path used by `System.exit` or a SIGTERM.

> [!warning] Hooks run at a delicate time
> The specification asks for defensive, thread-safe, deadlock-free hooks that finish quickly: when the shutdown comes from user logoff or system shutdown, the OS may cut the time budget. Do not rely on services that register their own hooks (they may already be shutting down), and do not wait on the AWT event thread — that is a documented deadlock scenario. A hook that never terminates keeps the JVM alive forever, which is exactly the trap in [[What happens if you call System.exit from a shutdown hook]].

The order question and the skip cases have their own cards: [[In what order do shutdown hooks run]] and [[When does a JVM shutdown hook not run]].

> [!tip] Interview answer
> A shutdown hook is an unstarted thread registered on `Runtime`; the JVM starts all of them at the beginning of shutdown — normal exit, `System.exit`, or SIGINT/SIGTERM — and waits for every hook to finish before terminating. Uncaught exceptions in a hook do not stop other hooks or change the exit code. Hooks are for quick, defensive cleanup, not for long computations.

