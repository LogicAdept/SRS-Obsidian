<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #OperatingSystems/Concurrency #SRS

# What is the PID 1 problem in Docker containers

> [!abstract] Short answer
> The container's entrypoint runs as **PID 1** of its pid namespace, and the kernel treats PID 1 specially: default signal dispositions are disabled (SIGTERM is ignored unless the program handles it), and orphaned child processes are re-parented to PID 1, which must reap their zombie state. A naive entrypoint that ignores signals or never reaps breaks graceful shutdown and leaks zombies.

## Why PID 1 is not just another process

Two kernel rules collide with simple Dockerfiles. First, PID 1 has no default handlers: signals that would kill an ordinary process do nothing unless explicitly handled — a `sleep`-like entrypoint just ignores `docker stop`'s SIGTERM until the 10-second SIGKILL. Second, when a container process forks children that exit while the parent is busy, the children become zombies; with no init in the namespace, the re-parenting target is your entrypoint, and anything it fails to `wait()` on stays as a zombie forever.

```bash
# shell form: sh is PID 1, app is its child
sh -c 'sleep 20' &    # ps: PID 1799 sh, PID 1801 sleep  <- TWO processes

# exec form: exec replaces the shell, app IS PID 1
sh -c 'exec sleep 20' &   # ps: PID 1805 sleep             <- ONE process
```

**Listing 1.** Observed with `ps -o pid,ppid,comm` on Linux: shell form leaves `sh` in the middle — it receives the signals, and the app hangs off it; `exec` collapses the wrapper away. This is why idiomatic entrypoint scripts end with `exec java -jar app.jar` — the exec-form idiom of [[What is the difference between shell form and exec form in a Dockerfile]].

Docker's answer to the reaping half is `docker run --init`: the daemon inserts its tiny init (`docker-init`, backed by tini) as PID 1, which forwards signals to your process and reaps orphans — as the run reference puts it, "ensures the usual responsibilities of an init system, such as reaping zombie processes" ([[What happens when you stop a Docker container]] covers the signal half).

> [!warning] The JVM is a signal-aware but not a reaping-for-others entrypoint
> The JVM installs handlers for SIGTERM/SIGINT (shutdown hooks run) and it reaps the children it spawns itself via its process reaper, so `exec java` as PID 1 is usually fine for simple services. The failure mode is compositional: a shell or bash wrapper that does not `exec`, or an app that spawns its own subprocess trees — each layer that ignores signals or fails to wait creates zombies or eats SIGTERM. Wrapping every container in `--init` is the cheap insurance.

> [!tip] Interview answer
> **PID 1 in a container is special twice: no default signal dispositions, so unhandled SIGTERM is ignored until SIGKILL, and it inherits orphaned children, so unreaped zombies accumulate. Use exec-form ENTRYPOINT (or exec in scripts) so your app is PID 1 and gets the signals, or add docker run --init to get tini as a proper signal-forwarding, zombie-reaping init.**

