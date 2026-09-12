<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How do Docker health checks work

> [!abstract] Short answer
> A health check is a command Docker runs **inside** the running container on a schedule; its exit code moves the container's health status through `starting` → `healthy` or `unhealthy`. You define it with the `HEALTHCHECK` Dockerfile instruction or `--health-*` flags on `docker run`. The process being alive and the service being usable are different questions, and the health check is what tells them apart.

## The probe contract

`HEALTHCHECK [OPTIONS] CMD command` runs the command with these knobs: `--interval` (default 30s), `--timeout` (30s — a slower run counts as a failure of that probe), `--start-period` (grace window after start, probes do not count toward the failure streak; API 1.29+), `--start-interval` (probe rate during the start period, API 1.44+), and `--retries` (3 consecutive failures needed to flip to `unhealthy`). Exit code 0 means healthy, 1 means unhealthy; any other code is reserved and treated as failure. `HEALTHCHECK NONE` disables a check inherited from the base image.

```dockerfile
HEALTHCHECK --interval=15s --timeout=3s --start-period=40s --retries=3 \
    CMD wget -q --spider localhost:8080/health || exit 1
```

**Listing 1.** A typical JVM-service probe: the start period covers Spring Boot's slow first boot, then every 15 seconds one HTTP round trip decides the status.

The resulting state lives in `docker inspect` under `State.Health`: the current status, `FailingStreak`, and a rolling log of recent probe runs with their output and exit codes. `docker ps` renders it as `(healthy)`, `(unhealthy)`, `(health: starting)` next to the ordinary Up status.

```d2
direction: right
start: "container starts\nstatus = starting" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
run: "probe runs on interval\ncounts against timeout" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
healthy: "exit 0\nstatus = healthy" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
fail: "exit 1 or timeout\nFailingStreak += 1" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
unhealthy: "retries streak reached\nstatus = unhealthy" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
start -> run
run -> healthy: "0"
run -> fail: "1 / timeout"
fail -> healthy: "exit 0\nresets streak"
fail -> unhealthy: ">= retries"
```

**Fig. 1.** Consecutive failures, not total count, decide the flip; one success resets `FailingStreak`.

## What the status is good for

On plain `docker run`, an `unhealthy` status is **informational only** — nothing restarts the container. The status becomes load-bearing through consumers: Compose `depends_on` gains `condition: service_healthy` so a dependent service does not start until the dependency actually answers ([[How does depends_on work in Docker Compose]]), and orchestrators wire the same probe into restart and traffic rules ([[What are Docker restart policies and when does a container restart by itself]]-style policies stay exit-code based). Health probes also have a lifecycle connection: they answer the "process up, service dead" case that exit codes and signal handling ([[What is the PID 1 problem in Docker containers]]) cannot see.

> [!warning] Unhealthy does not mean restarted
> A classic interview trap: with a plain `docker run`, Docker will happily keep an `unhealthy` container running forever — the status alone triggers nothing. Another trap: probing with a shell pipeline without an explicit `exit 1` on failure, so the check passes because the shell itself exits 0. Finally, a probe that needs more than `--timeout` fails even when the endpoint would have answered at 4 seconds — timeout is per probe run, not a grace budget.

> [!tip] Interview answer
> A health check is a scheduled in-container command whose exit code drives the status starting, healthy, unhealthy — configured via HEALTHCHECK or --health flags with interval, timeout, start-period, and retries. Docker reports it in inspect and ps; Compose uses it for service_healthy ordering. Crucially, on plain Docker an unhealthy container is only marked, not restarted — automatic reaction to health needs an orchestrator, while restart policies react only to exit codes.
