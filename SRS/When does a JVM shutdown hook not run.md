<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# When does a JVM shutdown hook not run

> [!abstract] Short answer
> Hooks run only on the orderly path: normal termination, `System.exit`/`Runtime.exit`, or a catching signal such as SIGINT or SIGTERM. They do **not** run when the JVM terminates immediately — `Runtime.halt`, an internal JVM crash, or SIGKILL — and a hook registered after the sequence has begun is rejected with `IllegalStateException`, so it never runs either.

The defining text draws a hard line: the JVM terminates when the shutdown sequence finishes **or when `halt` is called**. At termination all threads are stopped instantly — methods do not complete, `finally` clauses do not execute, uncaught-exception handlers are not run, and try-with-resources does not close anything. Whatever was supposed to happen in a hook after `halt` simply never happens.

## Signals split into two families

On a Unix-like OS, SIGTERM and SIGINT arrive as external events that **start** the orderly sequence — hooks run. SIGKILL is not delivered to the process at all: the kernel removes it, so no Java code, hook or not, executes. The same applies to an OOM-killer strike or a segfault inside native code — the process dies mid-instruction.

```d2
direction: right
trigger: "JVM shutdown trigger" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
orderly: "Orderly: hooks run\nmain ends · exit(n)\nSIGINT · SIGTERM" {
  width: 300
  height: 110
  style.fill: "#e8f5e9"
}
immediate: "Immediate: hooks skipped\nRuntime.halt(n)\nSIGKILL · JVM crash" {
  width: 310
  height: 110
  style.fill: "#ffebee"
}
late: "Registered after\nsequence began: rejected" {
  width: 280
  height: 110
  style.fill: "#fff3e0"
}
trigger -> orderly
trigger -> immediate
trigger -> late
```

**Fig. 1.** Three destinations for a shutdown trigger: orderly with hooks, immediate without them, or rejection of a late registration.

```java
public class Kill9HookDemo {
    public static void main(String[] args) throws Exception {
        Runtime.getRuntime().addShutdownHook(new Thread(() ->
                System.out.println("hook: cleanup ran")));
        System.out.println("ready, sleeping");
        Thread.sleep(60000);
    }
}
// Output (JDK 21), killed with SIGKILL (kill -9):
// ready, sleeping
// (no hook line; process exit code 137)
// Output, killed with SIGTERM (kill -15):
// ready, sleeping
// hook: cleanup ran
// (process exit code 143)
```

**Listing 1.** Same program, two signals: SIGTERM starts the sequence and the hook runs; SIGKILL kills the process before any Java code can react.

> [!warning] Do not bet data safety on hooks
> A killed-9 process loses every guarantee — production tools that must survive `kill -9` persist state transactionally or write-ahead, not in a hook. The subtler version of the same trap: a hook that hangs (network call without timeout, wait on a dead worker) does not skip other hooks, but the shutdown sequence never finishes and the JVM stays alive until someone calls `halt` or sends SIGKILL — see [[What happens if you call System.exit from a shutdown hook]].

The orderly mechanics are in [[What is a JVM shutdown hook]]; the halt semantics in [[What is the difference between System.exit and Runtime.halt]]; ordering guarantees (there are none) in [[In what order do shutdown hooks run]].

> [!tip] Interview answer
> Hooks fire on the orderly path only: normal exit, `System.exit`, SIGINT or SIGTERM. They are skipped by `Runtime.halt`, by SIGKILL and JVM crashes, and a late registration is rejected with `IllegalStateException`. That is why hooks are a best-effort cleanup, not a durability mechanism — anything that must survive a forced kill belongs in transactional storage or a write-ahead log.

