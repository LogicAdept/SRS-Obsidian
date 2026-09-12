<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Debugging #SRS

# What is the difference between docker exec and docker attach

> [!abstract] Short answer
> `docker exec` starts a **new process** inside the running container's namespaces; its exit changes nothing about the container. `docker attach` connects your terminal to the stdio of the container's **PID 1** — the process that is already running; your Ctrl-C and terminal input go to it, and with the default signal proxying that can stop the container. Different processes, different lifecycle consequences.

## What each command does

`exec` runs an arbitrary command in the container: `docker exec -it api sh` gives an interactive shell that shares the container's filesystem, network, and PID namespace but is a sibling of PID 1, not PID 1 itself. `attach` creates no process — it wires the local terminal to the streams of the main process, so you see the same output `docker logs --follow` would show, plus you can type into the process's stdin if it accepts input. Detaching safely requires the escape sequence `Ctrl-p Ctrl-q` (`--detach-keys` customizes it); plain `exit` on an attached interactive session ends the main process and the container with it, and Ctrl-C forwards SIGINT to PID 1 by default (`--sig-proxy=true`).

```bash
docker exec -it api sh            # new process, safe to exit anytime
docker attach api                 # bind to PID 1 stdio; detach = Ctrl-p Ctrl-q
docker attach --no-stdin api      # only the output stream
```

**Listing 1.** The operational rule: exec for interactive work, attach to interact with the main process itself.

The word `exec` collides across Docker concepts: in a Dockerfile, "exec form" means the JSON-array `ENTRYPOINT`/`CMD` style where no shell wraps the command ([[What is the difference between shell form and exec form in a Dockerfile]]) — the same Unix `exec` primitive that **replaces** a process instead of forking one. The host-level proof of that primitive:

```bash
sh -c 'echo "shell pid inside: $$"; exec sleep 3' &
# ... observed output (Linux):
shell pid inside: 4003
sleep pid seen from outside: 4003   # the shell *is* the sleep: same PID, no child
```

**Listing 2.** Observed on Linux: after `exec`, the shell *is* the sleep — same PID, no child. `docker exec` reuses the word for the opposite move: it **creates** a fresh process inside an existing container.

The PID 1 angle matters for both: what you attach to is the container's PID 1 with its signal-handling quirks ([[What is the PID 1 problem in Docker containers]]), and an exec'd debugging shell inherits the container's user — root by default unless the image sets `USER` or you pass `-u` ([[How do you run a Docker container as a non-root user]]).

> [!warning] Ctrl-C on an attached terminal can kill production
> The classic incident: attach to a foreground container, hit Ctrl-C out of habit, and SIGINT lands on PID 1 — if the app lacks a handler, the container dies ([[What happens when you stop a Docker container]] covers the same signal path for stop). The second trap: expecting `docker logs` output after exec'ing — an exec'd process writes to its own streams, not to the container log captured from PID 1.

> [!tip] Interview answer
> docker exec spawns a new process in the container's namespaces — a debugging shell that can exit without touching the container. docker attach wires your terminal to PID 1's stdio — no new process, your input goes to the main process, and Ctrl-C or exit can terminate it, so you detach with Ctrl-p Ctrl-q. I also keep the naming straight: exec form in a Dockerfile is the no-shell JSON-array style built on the exec syscall, while docker exec is a new process in a running container.
