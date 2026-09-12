<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What is the difference between volumes and bind mounts in Docker

> [!abstract] Short answer
> A **volume** is a Docker-managed directory (under `/var/lib/docker/volumes/`) whose lifecycle Docker owns: created by name, mountable into many containers, backed up with the CLI, portable across hosts. A **bind mount** maps an arbitrary host directory into the container as-is — great for dev hot-reload, but it couples the container to the host's path layout, UID world, and contents. A third mode, **tmpfs**, keeps data in host memory only.

## Who owns the data

Volumes are the documented preference for persisting container data: they survive the container, are safe to share, can be pre-populated from an image, and are driver-pluggable (NFS, cloud block storage). Sharing one volume between several containers — the interview question behind "how do containers exchange files" — is a named volume mounted into both; the legacy `--volumes-from` flag did the same by copying another container's mounts and is kept only for old setups. Bind mounts are the raw escape hatch: whatever is at that host path simply appears inside the container, writable both ways.

```bash
docker volume create pgdata
docker run -d -v pgdata:/var/lib/postgresql/data postgres:18   # volume: Docker-managed
docker run -d -v /home/me/app/src:/app/src myapp:dev           # bind mount: host path
docker run -d --tmpfs /tmp:rw,size=64m myapp:1.4               # tmpfs: memory-backed
```

**Listing 1.** The three mount kinds in one screen; the modern `--mount type=volume,src=pgdata,dst=...` spelling is equivalent and more explicit. CLI shapes as commonly shown — daemon-required commands not executed in the review environment.

```d2
direction: right
c: "container /var/lib/postgresql/data" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
v: "volume pgdata\n/var/lib/docker/volumes\nDocker-owned, portable" {
  width: 330
  height: 90
  style.fill: "#e3f2fd"
}
b: "bind /home/me/app/src\nhost path verbatim\nhost UID/perms apply" {
  width: 330
  height: 90
  style.fill: "#fff3e0"
}
c -> v: "-v pgdata:..."
c -> b: "-v /home/...:..."
```

**Fig. 1.** Same flag, different owners: the volume is an abstraction Docker manages; the bind mount is a hole punched into the host filesystem.

> [!warning] Bind mounts are the sharp tool in the drawer
> Two classics. Mounting `/var/run/docker.sock` into a container hands it full daemon control — effectively root on the host, the same power as `--privileged` ([[What does it mean to run a Docker container in privileged mode]]). And UID mismatches bite both ways: files written by a container user show up owned by some host UID, and a non-root container ([[How do you run a Docker container as a non-root user]]) may be unable to write a host directory at all. Also remember writes bypass the container layer entirely — the overlay copy-up discussion ([[How does the overlay2 storage driver work]]) does not apply to mounted paths.

> [!tip] Interview answer
> **Volumes are Docker-managed and Docker-lifecycle-owned — portable, shareable, backup-friendly, the default choice for real data. Bind mounts expose an exact host directory — ideal for local development and config injection, risky for anything privileged like the Docker socket. tmpfs is ephemeral in-memory for secrets or scratch. Choose by who should own the data.**

