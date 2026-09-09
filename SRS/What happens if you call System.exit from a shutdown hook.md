<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# What happens if you call System.exit from a shutdown hook

> [!abstract] Short answer
> Nothing terminates and the hook hangs. On Java 20+ the exit contract is serialized: only the invocation that initiates the shutdown sequence terminates the VM with its status; every later `exit` call performs no action and **blocks indefinitely**. A hook calling `System.exit` therefore blocks inside that call, the hook never terminates, the sequence never finishes, and the JVM stays alive until someone calls `Runtime.halt` or the process is killed.

The rationale is visible in the Java 21 contract of `Runtime.exit`: "successful invocations of this method are serialized such that only one invocation initiates the shutdown sequence and terminates the VM with the given status code", and because a successful invocation blocks indefinitely, "if it is invoked from a shutdown hook, it will prevent that shutdown hook from terminating. Consequently, this will prevent the shutdown sequence from finishing."

## The watchdog pattern that actually works

To terminate from inside a hook, use `Runtime.halt`: it does not initiate or await the sequence and immediately stops the JVM with its own status, overriding any pending exit status. A second hook acting as a watchdog rescues a JVM stuck on the `exit`-calling hook.

```d2
direction: right
h1: "Hook 1\ncalls System.exit(7)" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
stuck: "exit is a no-op now:\nblocks forever" {
  width: 240
  height: 90
  style.fill: "#ffcdd2"
}
h2: "Watchdog hook\nwaits, then halt(9)" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
term: "JVM terminates\nstatus 9" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
h1 -> stuck
h2 -> term
```

**Fig. 1.** The `exit`-calling hook is parked forever; only `halt` from another thread ends the shutdown.

```java
public class ExitFromHookDemo {
    public static void main(String[] args) {
        Runtime rt = Runtime.getRuntime();
        rt.addShutdownHook(new Thread(() -> {
            System.out.println("hook: calling System.exit(7)");
            System.exit(7);
            System.out.println("hook: line after System.exit never printed");
        }, "exiting-hook"));
        rt.addShutdownHook(new Thread(() -> {
            try {
                Thread.sleep(1500);
            } catch (InterruptedException ignored) {
            }
            System.out.println("watchdog: halt(9) after stuck hook");
            Runtime.getRuntime().halt(9);
        }, "watchdog"));
        System.out.println("main done");
    }
}
// Output (JDK 21):
// main done
// hook: calling System.exit(7)
// watchdog: halt(9) after stuck hook
// (process exit code: 9)
```

**Listing 1.** The status 7 from the stuck hook is lost; the process exits with the watchdog's `halt(9)` and the line after `System.exit(7)` never prints.

> [!warning] The version landmine
> On Java 16–19 the documented contract was different: an `exit` call with nonzero status made **after all hooks had already run** halted the VM with that status, so older interview answers claim "exit from a hook sets the exit code". That stopped being true in Java 20 — the modern result is a hung shutdown, verified against the SE 20/21 specifications. Legacy cleanup code that "sets the real status via exit from a hook" needs to be rewritten to `halt`.

This is one of the practical reasons hooks must be quick and defensive, see [[What is a JVM shutdown hook]]; the two termination paths are compared in [[What is the difference between System.exit and Runtime.halt]], and late registrations fail too — [[Can you register a shutdown hook after shutdown has begun]].

> [!tip] Interview answer
> On current Java the call blocks forever: only the first `exit` invocation drives the sequence, and a later one — which is what a hook's `System.exit` is — does nothing and parks its thread. The hook never finishes, so the shutdown never finishes and the JVM hangs. To stop the JVM from inside a hook you call `Runtime.halt`, whose status also overrides the pending one.

