<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# How do you invoke an external process in Java

> [!abstract] Short answer
> Build a `ProcessBuilder` with the program and its arguments as an exact list, call `start()` to get a `Process`, then manage the lifecycle: read the child's streams, wait with `waitFor()` or `waitFor(timeout, unit)`, and take the exit code from the return value or `exitValue()`. Use `inheritIO()` when the child should share your console.

`start()` launches the command in the builder's configured directory and environment. The `Process` object exposes the child's three streams from the parent's point of view — `getInputStream()` reads the child's stdout, `getErrorStream()` its stderr, `getOutputStream()` writes to its stdin. `waitFor()` returns the exit code on termination; `exitValue()` throws `IllegalThreadStateException` if the child is still running. Since Java 9, `onExit()` returns a `CompletableFuture<Process>` for asynchronous waiting.

## A complete parent-child run

The parent starts a small child class with the same JVM binary, inherits I/O so the child's output goes straight to the console, and waits with a timeout — the sequence every "run a tool from Java" feature is built on.

```java
import java.util.concurrent.TimeUnit;

public class InvokeProcessDemo {
    public static void main(String[] args) throws Exception {
        String javaBin = ProcessHandle.current().info().command().orElse("java");
        ProcessBuilder pb = new ProcessBuilder(javaBin, "-cp", ".", "ChildSleep");
        pb.inheritIO();
        Process p = pb.start();
        System.out.println("started, alive = " + p.isAlive());
        boolean done = p.waitFor(3, TimeUnit.SECONDS);
        System.out.println("done in 3s = " + done + ", exit = " + p.exitValue());
    }
}

class ChildSleep {
    public static void main(String[] args) throws Exception {
        System.out.println("child sleeping");
        Thread.sleep(300);
    }
}
// Output (JDK 21):
// started, alive = true
// child sleeping
// done in 3s = true, exit = 0
```

**Listing 1.** `start()` returns immediately — `isAlive` is still true; `waitFor(3, SECONDS)` returns `true` with exit code 0 once the child terminates.

> [!warning] The pipe-buffer deadlock
> If you do **not** call `inheritIO` or redirect to files, the child's stdout/stderr flow into OS pipes with a small buffer (64 KB on Linux). A chatty child blocks forever on write when the buffer fills and nobody drains it — the process hangs, `waitFor` never returns. Read the streams on dedicated threads, merge them with `redirectErrorStream(true)`, or redirect them away. The second classic mistake: calling `exitValue()` before termination and surviving the `IllegalThreadStateException`.

Killing a misbehaving child is `destroy()` for a polite termination or `destroyForcibly()` for the immediate one, with `isAlive()` possibly staying true for a brief moment after. Both come with the modern process API in [[What is ProcessHandle]]; the legacy launcher and why to avoid it in [[What is the difference between Runtime.exec and ProcessBuilder]]; feeding the child's environment in [[How do you pass environment variables to a subprocess in Java]].

> [!tip] Interview answer
> I use ProcessBuilder: exact command list, optional directory and environment, `inheritIO` or explicit stream handling, then `start()`. On the `Process` I wait with `waitFor(timeout, unit)` to bound the runtime and take the exit code; `exitValue` only works after termination. The pitfall everyone hits is undrained output blocking the child on a full pipe — either inherit, redirect, or read streams concurrently.

