<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What are Docker restart policies and when does a container restart by itself

> [!abstract] Short answer
> There are four policies: `no` (default), `on-failure[:max-retries]`, `always`, and `unless-stopped`, set with `--restart` or changed live with `docker update --restart`. The container never restarts itself — the **Docker daemon** detects exit and starts a new process in the same container. A policy only takes effect after the container starts successfully, which the daemon defines as staying up for at least 10 seconds.

## The four policies

| Policy | Restarts on exit | After manual stop | After daemon restart |
|---|---|---|---|
| `no` | never | — | — |
| `on-failure[:N]` | only non-zero exit code, up to N retries | no | no |
| `always` | any exit | restarts when the daemon comes back | yes |
| `unless-stopped` | any exit | stays stopped | no |

```bash
docker run -d --name api --restart on-failure:5 api:1.42
docker update --restart unless-stopped api
docker update --restart unless-stopped $(docker ps -q)   # fleet-wide
```

**Listing 1.** Setting a policy at start and changing it on a running container with `docker update`.

The retry counter matters for crash loops: `on-failure:5` gives up after five failed attempts, and the count is exposed as `RestartCount` in `docker inspect`. `always` and `unless-stopped` differ only in one scenario — an explicit `docker stop` — which `always` "forgets" after a daemon restart and `unless-stopped` does not. This is why production services usually get `unless-stopped` or `always`, while `on-failure` suits batch jobs that may legitimately fail. The exit path itself is the same one described in [[What happens when you stop a Docker container]].

```d2
direction: right
exit: "container main process\nexits (code N)" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
policy: "dockerd evaluates\nrestart policy" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
ok: "started successfully?\n(up >= 10s before first exit)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
again: "new process, same container\nRestartCount += 1" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
giveup: "no / retries exhausted\nstays exited" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
exit -> policy
policy -> ok
ok -> again: "policy says restart"
ok -> giveup: "no / max-retries hit"
again -> exit: "next exit"
```

**Fig. 1.** The daemon, not the container, owns the loop; a policy only fires for containers that had a successful start.

## What restart policies cannot do

The policy is purely exit-code based. A server that hangs while its process lives produces no exit, so no restart happens — the container is "running" and useless at the same time. Detecting that requires a health probe ([[How do Docker health checks work]]), and acting on it requires an orchestrator ([[How does Docker differ from Kubernetes]]); plain Docker has no "restart on unhealthy" rule.

> [!warning] Restart policy is not self-healing infra
> "The container restarts itself" is a popular lie: if the Docker daemon is down, nothing restarts, and `on-failure` ignores daemon restarts entirely. Also, `always` still restarts a container you manually stopped, as soon as the daemon restarts — the state you wanted lost is silently resurrected. For daemon-level availability you run dockerd under systemd, not under a restart policy.

> [!tip] Interview answer
> Restart policies — `no`, `on-failure: N`, `always`, `unless-stopped` — tell the Docker daemon to start the container again after exit. The container never restarts itself, dockerd does it, and only after a successful start of at least 10 seconds. `on-failure` reacts to non-zero exit codes and counts retries, `unless-stopped` respects a manual stop across daemon restarts while `always` does not. A hung process gets no restart, because the exit code never appears — that is health checks and orchestrators territory.
