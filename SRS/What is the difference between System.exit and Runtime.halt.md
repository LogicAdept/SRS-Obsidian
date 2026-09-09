<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# What is the difference between System.exit and Runtime.halt

> [!abstract] Short answer
> `System.exit(n)` (equivalently `Runtime.exit(n)`) initiates the **orderly shutdown sequence**: registered shutdown hooks are started and the JVM waits until all of them terminate, then terminates with status `n`. `Runtime.halt(n)` terminates the JVM **immediately and unconditionally**: no hooks are started, a running sequence is not awaited, and at termination all threads are stopped mid-flight. `halt` never returns.

`halt` also overrides a pending status: if `exit` was already invoked, a later `halt(m)` terminates the process with `m`, not with the status passed to `exit`. This makes `halt` the standard escape hatch from a stuck shutdown — for example a watchdog hook that force-terminates when another hook refuses to die.

## What orderly means for exit

The shutdown sequence has three triggers: live non-daemon threads drop to zero, the first `exit` call, or an external event such as a signal. Once it begins, hooks run concurrently and the sequence finishes only when all hooks terminate. Termination itself is abrupt for everyone: methods do not complete, `finally` clauses do not execute, uncaught-exception handlers are not run, and try-with-resources does not close resources.

```d2
direction: right
exitp: "System.exit(n)" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
hooks: "Shutdown hooks started\nconcurrently, JVM waits" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
termN: "Terminate\nstatus n" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
haltp: "Runtime.halt(m)" {
  width: 190
  height: 70
  style.fill: "#ffebee"
}
termM: "Terminate now\nstatus m, hooks skipped" {
  width: 260
  height: 100
  style.fill: "#ffcdd2"
}
exitp -> hooks -> termN
haltp -> termM
```

**Fig. 1.** `exit` schedules a last chance for cleanup; `halt` goes straight to termination with its own status.

```java
public class HaltSkipsHooksDemo {
    public static void main(String[] args) {
        Runtime.getRuntime().addShutdownHook(new Thread(() ->
                System.out.println("hook: cleanup ran")));
        try {
            System.out.println("main: halting");
            Runtime.getRuntime().halt(9);
        } finally {
            System.out.println("finally: never printed");
        }
    }
}
// Output (JDK 21):
// main: halting
// (process exit code: 9)
```

**Listing 1.** With `halt`, the registered hook never runs and the surrounding `finally` never executes; the process still exits with code 9.

> [!warning] halt is a data-corruption tool
> The API note is explicit: halting may circumvent or disrupt cleanup actions and lead to data corruption — files half-written, transactions half-committed. The mirror lie is that `exit` is always safe to call anywhere: calling it from inside a hook deadlocks the shutdown on Java 20+, see [[What happens if you call System.exit from a shutdown hook]].

Cases where even hooks cannot save you are collected in [[When does a JVM shutdown hook not run]]; the hook mechanism itself is described in [[What is a JVM shutdown hook]].

> [!tip] Interview answer
> `exit` is the polite path: it starts the shutdown sequence, runs all registered hooks concurrently, and terminates the VM with the given status after they finish. `halt` is the rude path: immediate, unconditional termination with no hooks and no waiting, overriding any pending exit status. Use `exit` normally and `halt` only as a watchdog against a shutdown that will not finish.

