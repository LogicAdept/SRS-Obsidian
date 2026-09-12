<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Debugging #SRS

# How do you debug a container that exits immediately

> [!abstract] Short answer
> Work the evidence in order: `docker logs` for what the process printed, `docker inspect` for the exit code and `OOMKilled` flag, `docker run --entrypoint sh -it` to get a shell inside the image instead of the crashing command, and `docker events`/`docker start -a` to watch the death happen live. Most fast exits are one of four things: bad command (exec/CMD typo), failed startup dependency, permission denied, or OOM kill.

## The four-step drill

```bash
docker logs crashy                                # stdout/stderr before death (stderr counts!)
docker inspect -f '{{json .State}}' crashy
#   {"Status":"exited","ExitCode":1,"Error":"","OOMKilled":false,...}
docker run -it --rm --entrypoint /bin/sh myapp:1.0   # interactive shell in the same image
docker start -a crashy                            # re-run attached, watch it die again
```

**Listing 1.** The drill: logs first, `State` JSON second — ExitCode maps the class of failure (1 app exception, 126/127 command/permission, 137 SIGKILL or OOM, 143 SIGTERM), then reproduce inside a shell. CLI output shapes per the container reference; daemon commands not executed in the review environment.

Exit-code triage in practice: `126`/`127` point at the entrypoint itself — a shell-form CMD typo'd into a non-existent binary, or an exec-form line that is not valid JSON and got mangled ([[What is the difference between shell form and exec form in a Dockerfile]]). `137` means SIGKILL: either an explicit kill or the cgroup OOM killer — read `OOMKilled` before theorizing ([[What happens when you stop a Docker container]] has the signal map). `1` is your application failing at boot — the logs step then matters most, and a missing dependency shows up there as a connect exception (which is the Compose readiness story, [[How does depends_on work in Docker Compose]]).

> [!warning] `docker logs` dies with the container — and with the wrong logging setup
> Once the container is `docker rm`'d, its stdout/stderr are gone unless a logging driver shipped them out (journald, fluentd, cloud) — CI agents that `--rm` everything lose crash evidence by design. The subtler trap: the app logged to a file inside the container; `docker logs` shows nothing because PID 1 never wrote to stdout — twelve-factor logging ([[What is an executable JAR in Spring Boot]] images assume console output) is a precondition for this entire drill to work.

> [!tip] Interview answer
> **Sequence: docker logs for the output, docker inspect .State for ExitCode and OOMKilled, then docker run --entrypoint sh to explore the actual image, and start -a or events to watch it die. Interpret the code: 1 is the app, 126/127 is the command, 137 is SIGKILL or OOM. And remember logs vanish with rm unless a driver shipped them — so container output must go to stdout/stderr.**

