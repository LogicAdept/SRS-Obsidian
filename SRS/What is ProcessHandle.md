<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# What is ProcessHandle

> [!abstract] Short answer
> `ProcessHandle` (Java 9, `java.lang`) identifies and controls **native** OS processes: `current()` and `of(pid)` locate them, `allProcesses()` snapshots everything visible, `isAlive()` tests liveness, `info()` exposes metadata (command, arguments, user, start time, CPU time), `parent()/children()/descendants()` walk the process tree, `onExit()` gives a completion future, and `destroy()/destroyForcibly()` request termination. Unlike `Process`, a handle works for processes you did not start.

The companion of `Process`: a `Process` is always a child started by your JVM and adds stream access (stdin/stdout/stderr); a `ProcessHandle` is a lightweight view of any native process with no stream plumbing. A started child hands out its handle via `process.toHandle()`.

## What the API answers

The metadata accessors on `Info` return `Optional<String>`/`Optional<Instant>` — information the OS withholds comes back empty rather than as a lie. `destroy()` requests a normal termination (SIGTERM on Unix, letting the child run its own shutdown), `destroyForcibly()` the immediate one (SIGKILL); both return `boolean` because OS access controls may simply refuse. Calling `destroy` on your **own** process handle throws `IllegalStateException` — the API note says to use `System.exit` instead.

```d2
direction: right
ph: "ProcessHandle (Java 9)\nany native process" {
  width: 260
  height: 100
  style.fill: "#e8f5e9"
}
watch: "Watch\nisAlive · info()\nparent · children · descendants" {
  width: 280
  height: 110
  style.fill: "#e3f2fd"
}
act: "Act\nonExit() · destroy()\ndestroyForcibly()" {
  width: 250
  height: 100
  style.fill: "#fff3e0"
}
proc: "Process (since 1.0)\nyour child only\n+ stdin/stdout/stderr" {
  width: 250
  height: 100
  style.fill: "#ffebee"
}
ph -> watch
ph -> act
proc -> ph: "toHandle()"
```

**Fig. 1.** A handle can observe and kill any process; the richer `Process` view of your own children delegates to it via `toHandle()`.

```java
public class ProcessHandleDemo {
    public static void main(String[] args) throws Exception {
        ProcessHandle me = ProcessHandle.current();
        System.out.println("current pid = " + me.pid());
        String javaBin = me.info().command().orElse("java");
        Process child = new ProcessBuilder(javaBin, "-cp", ".", "ChildSleep").start();
        ProcessHandle childHandle = child.toHandle();
        System.out.println("child pid = " + childHandle.pid());
        System.out.println("child alive = " + childHandle.isAlive());
        System.out.println("child in my descendants = "
                + me.descendants().anyMatch(h -> h.pid() == childHandle.pid()));
        System.out.println("child in allProcesses = "
                + ProcessHandle.allProcesses().anyMatch(h -> h.pid() == childHandle.pid()));
        childHandle.onExit().join();
        System.out.println("child alive after onExit = " + childHandle.isAlive());
    }
}

class ChildSleep {
    public static void main(String[] args) throws Exception {
        System.out.println("child sleeping");
        Thread.sleep(300);
    }
}
// Output (JDK 21; pid values vary per run):
// current pid = 2871
// child pid = 2889
// child alive = true
// child in my descendants = true
// child in allProcesses = true
// child alive after onExit = false
```

**Listing 1.** The child is visible through the tree (`descendants`), the system snapshot (`allProcesses`), and terminates without any `waitFor` — `onExit().join()` does the waiting.

> [!warning] destroy is a request, not a guarantee
> `destroy()` returns `true` when the termination was successfully **requested** — the process may still shut down slowly or ignore the signal, and even after `destroyForcibly()` `isAlive()` can stay `true` for a brief period. `allProcesses()` is a snapshot: processes in it may already be dead and newer ones are missing. Cancelling the `onExit()` future does not cancel the process — killing requires `destroy`.

Launching and managing your own children is covered in [[How do you invoke an external process in Java]], the launcher comparison in [[What is the difference between Runtime.exec and ProcessBuilder]], and the shutdown machinery of your own JVM in [[What is a JVM shutdown hook]].

> [!tip] Interview answer
> `ProcessHandle` is the Java 9 API for native processes: find them with `current`, `of`, or `allProcesses`, inspect them with `info` and the process tree, watch termination with `onExit`, and kill with `destroy` or `destroyForcibly`. It differs from `Process` by working for processes you did not launch and by having no stream access — a `Process` gives you both through `toHandle`.

