<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Java/Runtime #SRS

# What happens when you stop a Docker container

> [!abstract] Short answer
> `docker stop` sends **SIGTERM** to the container's PID 1, waits a grace period (10 seconds by default on Linux), then escalates to **SIGKILL**. `docker kill` sends SIGKILL immediately. The first signal is customizable via the Dockerfile `STOPSIGNAL` instruction or `--stop-signal`, and the wait via `--timeout`/`-t`.

## The two-signal handshake

The whole design assumes PID 1 handles SIGTERM and exits cleanly — for a Java app that means shutdown hooks run and in-flight requests drain. The kernel-side semantics do not depend on Docker, which makes them reproducible on any Linux box:

```java
public class SignalDemo {
    public static void main(String[] args) throws Exception {
        Runtime.getRuntime().addShutdownHook(new Thread(() ->
            System.out.println("[hook] shutdown hook runs on SIGTERM")));
        System.out.println("[app] pid=" + ProcessHandle.current().pid()
            + " waiting; send SIGTERM (15) or SIGKILL (9)");
        Thread.sleep(300_000);
    }
}
```

**Listing 1.** Probe app: registers a shutdown hook, then blocks.

```bash
kill -TERM <pid>   # exit code 143, log: [app] ... / [hook] shutdown hook runs on SIGTERM
kill -KILL <pid>   # exit code 137, log: [app] ...  (hook never ran)
```

**Listing 2.** Observed on Temurin JDK 21.0.12.1, Linux: SIGTERM triggers the hook and yields exit 143; SIGKILL yields 137 with no hook — exactly what separates `docker stop` from `docker kill`. Inside Docker the same 137 also masks cgroup OOM kills ([[What is the lifecycle of a Docker container]] explains where exited codes surface; check `State.OOMKilled` before blaming the signal).

```d2
direction: right
s: "docker stop\n(SIGTERM to PID 1)" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
h: "PID 1 handles it\nhooks drain in-flight work" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
w: "grace period\n--timeout, default 10s" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
k: "docker kill\n(SIGKILL, uncatchable)" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
s -> h
h -> w: "still alive?"
w -> k: "yes"
```

**Fig. 1.** Graceful shutdown is a race the container must win: handle SIGTERM before the daemon runs out of patience.

> [!warning] Exit code 137 in Kubernetes/Docker logs usually means SIGKILL — but ask why
> 137 is 128+9, and it is produced both by `docker kill`/timeout escalation and by the kernel's OOM killer when the cgroup exceeds its memory budget. "The app got SIGKILL" is only half the diagnosis; check `State.OOMKilled` before blaming the orchestrator, and remember a JVM that never receives SIGTERM because of a shell-form entrypoint always burns the full grace period ([[What is the difference between shell form and exec form in a Dockerfile]]).

> [!tip] Interview answer
> **docker stop = SIGTERM to PID 1, ten-second grace, then SIGKILL; docker kill = SIGKILL straight away. Your process must catch SIGTERM and drain — for Java that is shutdown hooks; verified empirically, a hooked JVM exits 143 on SIGTERM and 137 under SIGKILL with no hook. And 137 in logs can equally be an OOM kill, so check OOMKilled first.**

