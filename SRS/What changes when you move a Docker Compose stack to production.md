<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker/Compose #SRS

# What changes when you move a Docker Compose stack to production

> [!abstract] Short answer
> Compose stays a **single-host** tool, so "production" means hardening the same file — restart policies, healthchecks, resource and log limits, pinned images, file-based secrets — via an override file merged with `-f`, plus accepting its limits: no cross-node scheduling, no self-healing beyond the local daemon, and rollouts you perform manually. Beyond one host you are choosing Swarm or Kubernetes, not Compose flags.

## The override-file pattern

The docs' recommended shape is a base `compose.yaml` for development plus `compose.production.yaml` holding only the deltas — Compose merges them left-to-right:

```bash
docker compose -f compose.yaml -f compose.production.yaml up -d
```

**Listing 1.** The production run; every change below lives in the override file, not in a forked copy of the whole stack.

```yaml
services:
  api:
    image: registry.example/api:1.42.0   # pinned, never :latest
    restart: unless-stopped              # survive daemon/host restarts
    healthcheck:
      test: ["CMD-SHELL", "curl -f localhost:8080/health || exit 1"]
      interval: 15s
      timeout: 3s
      retries: 3
    logging:
      driver: json-file
      options: { max-size: "10m", max-file: "3" }
    secrets: [db_password]               # file, not -e
```

**Listing 2.** The deltas that matter: pinned version instead of a mutable tag, a restart policy, a healthcheck for ordering and local supervision, log rotation so one service cannot fill the host disk, and secrets instead of inline env ([[What are Docker restart policies and when does a container restart by itself]], [[How does Docker logging work and what are logging drivers]]).

Deploying a code change is `docker compose build web && docker compose up -d --no-deps web` — `--no-deps` recreates only the changed service and leaves its dependencies alone, which is the closest Compose gets to a rolling update. Pointing `DOCKER_HOST` at a remote daemon runs the same file against another host, but the topology stays one daemon: if that host dies, the stack is down — there is no rescheduling to another node ([[How does depends_on work in Docker Compose]] covers the startup-order half of the same file).

## Where the ceiling is

The honest production answer has two parts: what Compose gains (declarative startup, healthcheck-gated ordering, per-service restart policies on one box) and what it lacks — multi-node placement, rolling deploys with readiness gating, and reconciliation after node loss. Those are orchestrator features: `deploy:` sections in a Compose file reach their full meaning only on a Swarm ([[What is Docker Swarm mode and how does it compare to Kubernetes]]), and anything beyond that is Kubernetes. "Compose in production" is a legitimate answer for single-host products, edge boxes, and small self-hosted setups — stated with the ceiling, not as a general claim.

> [!warning] restart: always is not availability
> A restart policy resurrects containers only on the host whose daemon is alive; it fixes crash loops, not host loss, and it will restart a service whose dependency is still unhealthy unless the healthcheck-based ordering is actually in the file. The other frequent miss: shipping the dev compose file as-is — with `build:`, bind-mounted source code, and `:latest` tags — because "compose is compose" is false the moment the base image or the code path differs.

> [!tip] Interview answer
> I keep one compose file and add a production override: pinned image versions, restart policy, healthchecks, log rotation caps, resource limits, and file-based secrets — merged with two -f flags, deployed with build plus up --no-deps for one service. I state the ceiling explicitly: Compose is single-host, so no cross-node rescheduling or real rolling updates; restart is not availability. For a single-box product that is a solid setup; the moment I need self-healing across hosts, that file graduates to Swarm or Kubernetes.
