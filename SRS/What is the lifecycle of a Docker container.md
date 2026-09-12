<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What is the lifecycle of a Docker container

> [!abstract] Short answer
> Created → running → exited → removed, with `paused` and `restarting` as side states. `docker run` is just `docker create` + `docker start`; a stopped container persists (name, filesystem, logs) until explicitly removed or run with `--rm`. Restart policies decide whether an exited container starts again.

## States and the verbs between them

```d2
direction: right
img: "image" {
  width: 150
  height: 70
  style.fill: "#e3f2fd"
}
created: "created\ndocker create" {
  width: 190
  height: 80
  style.fill: "#fff3e0"
}
run: "running\ndocker start / run" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}
paused: "paused\nSIGSTOP/SIGCONT" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
exited: "exited\nstop / crash / main() end" {
  width: 230
  height: 80
  style.fill: "#ffebee"
}
gone: "removed\ndocker rm (--rm auto)" {
  width: 200
  height: 80
  style.fill: "#ffebee"
}
img -> created: "build/pull"
created -> run
run -> paused: "docker pause"
paused -> run: "unpause"
run -> exited: "exit"
exited -> run: "start / restart policy"
exited -> gone: "rm"
```

**Fig. 1.** The verb map. Exited is not deleted: config, writable layer, and logs remain until `docker rm` — that is how you read a crashed container's logs after the fact.

The verbs map onto the states: `docker create` builds the filesystem and config without starting (useful to pre-stage with `--name`), `docker start` boots it, `docker stop`/`docker kill` end the run ([[What happens when you stop a Docker container]]), `docker pause` freezes via the cgroup freezer rather than signaling, and `docker rm` finally disposes. `docker run --rm` collapses the whole cycle to run-and-forget, which is the right shape for one-shot jobs and CI steps.

> [!warning] Exited containers are immortal until you act
> Every `docker run` without `--rm` leaves a container behind after exit — thousands of `Exited (0)` husks eating disk on a CI agent are the classic archaeology. Restart policies are per-container (`--restart no|on-failure|always|unless-stopped`) and are about process death, not host reboots alone; and a crashed loop with `always` restarts forever — the orchestrator-level liveness story is different ([[How would you explain Liveness vs Readiness probe]] is the Kubernetes take).

> [!tip] Interview answer
> **Lifecycle: created by docker create, running after start/run, exited on stop, crash, or main returning, and removed only by docker rm — or automatically with --rm. Paused is the freezer state, restarting comes from restart policies. Remember run = create + start, and exited containers keep their logs and layer until you remove them.**

