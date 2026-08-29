<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/Concurrency/Threads #SRS

# How do you capture a Java thread dump?

> [!abstract] Short answer
> Attach to the live JVM with **`jcmd <pid> Thread.print`**. Add **`-l`** for `java.util.concurrent` locks. **`Thread.dump_to_file`** writes **all** threads (including unmounted virtual threads) to a file; **`Thread.print`** prints platform threads and **mounted** virtual threads only. HotSpot also dumps to that process’s **stdout** on **Control+\\** (Linux), **Control+Break** (Windows), or **`kill -QUIT <pid>`**. That dump does **not** terminate the process. A heap dump is a different artifact — [[How do you capture a Java heap dump]].

## Attach, signal, or snapshot

`jcmd` must run on the **same machine** as the JVM, with the **same effective user and group** that launched it. `jcmd -l` lists local Java PIDs (not JVMs in a separate Docker PID namespace — use `ps` there). Then:

- `jcmd <pid> Thread.print` — stacks of platform threads and mounted virtual threads. **`-l`**: concurrent locks. **`-e`**: extended thread info.
- `jcmd <pid> Thread.dump_to_file dump.txt` — all threads to a file. **`-format=json`** or `plain` (default). **`-overwrite`**. `%p` in the path expands to the PID.

`jstack <pid>` prints Java stacks the same way as a classic dump; **`-l`** adds lock detail. The command is **experimental and unsupported** and may disappear. If the VM ignores Control+\\, the troubleshooting path is **`jstack`** or **`jhsdb jstack`** (mixed native frames with `--mixed` when a thread looks stuck in `RUNNABLE`).

Without JDK attach: send **SIGQUIT** (`kill -QUIT <pid>`). Output goes to the **target** process’s stdout (often a redirected log). After the stacks, HotSpot runs **deadlock detection** on synchronized monitors and `java.util.concurrent` locks.

In-process: `ThreadMXBean.dumpAllThreads` (locked monitors / ownable synchronizers when the VM supports them) — [[How can you check if a thread holds a monitor lock in Java]]. `Thread.getAllStackTraces()` is only **live platform threads**, omits virtual threads, and each stack is a **snapshot** that may be taken at a different instant.

```bash
jcmd -l
jcmd 12345 Thread.print -l
jcmd 12345 Thread.dump_to_file -format=plain /tmp/threads-%p.txt
kill -QUIT 12345
```

**Listing 1.** Same-host attach (`jcmd`) versus SIGQUIT to the process itself. Replace `12345` with the VM pid. `jstack 12345` is the older attach tool.

```java
import java.lang.management.ManagementFactory;
import java.lang.management.ThreadInfo;
import java.lang.management.ThreadMXBean;

public final class InProcessThreadDump {
    public static void main(String[] args) {
        ThreadMXBean mx = ManagementFactory.getThreadMXBean();
        boolean monitors = mx.isObjectMonitorUsageSupported();
        boolean syncs = mx.isSynchronizerUsageSupported();
        for (ThreadInfo info : mx.dumpAllThreads(monitors, syncs)) {
            System.out.print(info);
        }
    }
}
```

**Listing 2.** Management snapshot from inside the JVM. `dumpAllThreads(true, true)` throws `UnsupportedOperationException` if that VM does not track monitors or synchronizers.

```d2
direction: down
q: "Need stacks of a live JVM" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
jcmd: "jcmd pid Thread.print\n(+ dump_to_file for all VTs)" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
sig: "Ctrl+\\ / Ctrl+Break\nkill -QUIT → that stdout" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
hung: "VM ignores signal\njstack / jhsdb jstack" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}
q -> jcmd: "can attach"
q -> sig: "console or no JDK tools"
q -> hung: "no dump printed"
```

**Fig. 1.** Preferred path is `jcmd`. SIGQUIT still works when you can only signal. A hung VM that does not print needs a serviceability attach (`jstack` / `jhsdb`).

> [!warning] `Thread.print` is not every virtual thread
> Unmounted virtual threads are missing from `Thread.print` / classic `jstack` output. Use `Thread.dump_to_file` when the app runs on virtual threads.

> [!warning] SIGQUIT writes the target’s stdout, not yours
> In a container or a service with redirected logs, the dump is in **that** stream. `jcmd` prints to **your** terminal. `jcmd` also fails across a user mismatch or a Docker PID you listed with `jcmd -l`.

> [!tip] Interview answer
> I attach with `jcmd <pid> Thread.print` and `-l` if I need concurrent locks. For virtual threads I use `Thread.dump_to_file`. If I cannot attach, `kill -QUIT` or Control+Break dumps to the process stdout without killing it; a hung VM that ignores that gets `jhsdb jstack`.
