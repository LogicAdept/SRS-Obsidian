<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What is the difference between shell form and exec form in a Dockerfile

> [!abstract] Short answer
> Shell form (`CMD java -jar app.jar`) wraps the command in `/bin/sh -c`: you get variable substitution and shell syntax, but `sh` is the process — signals go to it, not your app. Exec form (`CMD ["java","-jar","app.jar"]`) is a JSON array that execs the binary directly: no shell, no substitution — and the process receives signals itself. For `CMD`/`ENTRYPOINT`/`RUN`, exec form is the signal-safe default.

## What each form buys

Shell form is readable and flexible: pipes, globs, `$VAR` expansion all work because a real shell runs the line. The cost is the extra process — `sh` becomes PID 1 and your app is a child whose signals depend on `sh` forwarding them, which the reference states plainly: the executable "will not be the container's PID 1, and will not receive Unix signals", so `docker stop`'s SIGTERM never arrives ([[What happens when you stop a Docker container]]).

```dockerfile
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75"
# shell form: shell expands $JAVA_OPTS, but sh wraps the JVM
ENTRYPOINT java $JAVA_OPTS -jar app.jar
# exec form + explicit shell to keep expansion AND exec chaining:
ENTRYPOINT ["sh", "-c", "exec java $JAVA_OPTS -jar app.jar"]
```

**Listing 1.** Two idioms for env-based flags: plain shell form (simple, signal-blind) versus exec form invoking `sh -c` with `exec` (substitution **and** the JVM replaces the shell). Run reference material, not an executed build — no daemon in the review environment.

The empirical process-shape difference, observed on Linux:

```bash
sh -c 'sleep 20'        # ps: sh (1799) -> sleep (1801): two processes
sh -c 'exec sleep 20'   # ps: sleep (1805): one process, shell replaced
```

**Listing 2.** `exec` swaps the shell image for the target binary, collapsing the wrapper; the child becomes the process Docker talks to ([[What is the PID 1 problem in Docker containers]] — same fact seen from the PID-1 side).

> [!warning] Exec form is JSON, and shell rules do not apply
> Exec form requires double quotes and real JSON: single quotes silently fail to parse and the builder falls back to treating the line as shell form — with surprising results. And because no shell runs, `RUN ["echo", "$HOME"]` prints the literal string `$HOME`; escape backslashes matter, and anything needing pipes or expansion must explicitly invoke a shell (`["sh","-c","..."]`).

> [!tip] Interview answer
> **Shell form runs your line through /bin/sh -c: easy syntax, but the shell is PID 1 and eats the signals. Exec form is a JSON array that execs directly: no substitution, but your process gets SIGTERM and clean exit codes. Java images typically use exec form — with sh -c exec if they need env expansion.**

