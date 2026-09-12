<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Security/AppSec #SRS

# How do you manage secrets in Docker at runtime

> [!abstract] Short answer
> Runtime secrets should reach the container as **files**, not environment variables: Swarm mounts each secret under `/run/secrets/` (one file per secret name) as an in-memory tmpfs mount, delivered to the node only when a task needs it. Compose has the same `secrets:` mechanism for single hosts. Environment variables are the default answer people reach for — and the one that leaks through `docker inspect`, crash dumps, and every child process.

## The mechanism

In Swarm mode a secret is a first-class object stored in the manager's Raft log and distributed encrypted over mutual TLS; a service task gets a read-only file at `/run/secrets/db_password` (path = the secret's name) backed by tmpfs, so the value lives in memory on the node, not in the image or on disk:

```bash
printf 'S3cr3t!' | docker secret create db_password -
docker service create --name api \
  --secret db_password \
  api:1.42
# inside the container:
cat /run/secrets/db_password
```

**Listing 1.** Create the secret once, attach it by name; the application reads a file instead of parsing the environment. Rotating means creating a new secret version and updating the service — tasks restart with the new file.

Compose supports the same shape for single-host stacks: a top-level `secrets:` block with either a `file:` source (the value lives on the host, mounted in as tmpfs) or `external: true` (managed elsewhere), then `secrets:` on the service. Build-time secrets are a separate problem solved by `RUN --mount=type=secret`, which keeps the value out of layers and `docker history` entirely ([[What is the difference between ARG and ENV in a Dockerfile]] contrasts the build-time variables).

## Why not environment variables

`-e SECRET=...` works everywhere, which is why it dominates — and leaks in four ways: the value is visible to any process via `docker inspect` and the container's `/proc/1/environ`; it is inherited by every child process, so a subprocess dump or a shell escape exfiltrates it; entrypoint scripts that log the environment print it; and some tooling echoes env into crash reports. The file approach exposes the value only to the processes that open the path, and nothing enumerates it by default. The Kubernetes world has the same split — env-based pod secrets versus Secret volumes ([[How would you explain ConfigMap vs Secret]]) — so the habit transfers across orchestrators.

> [!warning] Swarm secrets are not an encryption-at-rest guarantee for the whole node
> Secrets are encrypted in the Raft log and on the wire, and mounted as tmpfs in tasks — but any process running as root inside the container reads `/run/secrets/*`, and anyone who controls the Docker daemon controls the cluster's secrets. A secret is access control around the value, not a vault: real rotation, audit, and long-term storage still belong to an external system, with the mounted file being just the last delivery step.

> [!tip] Interview answer
> At runtime the right default is file-based secrets: in Swarm, docker secret objects delivered as tmpfs files at /run/secrets, in Compose the secrets block with file or external sources — the app reads a file, so the value never sits in the environment where docker inspect, child processes, and crash logs leak it. Build-time secrets are separate: RUN --mount=type=secret keeps them out of layers and history. Secrets reduce exposure at delivery; rotation and storage still belong outside the cluster.
