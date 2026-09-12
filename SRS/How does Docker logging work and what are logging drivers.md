<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How does Docker logging work and what are logging drivers

> [!abstract] Short answer
> Docker captures whatever the container's PID 1 writes to stdout/stderr and hands it to a **logging driver**; the default `json-file` driver stores each line as a JSON document on the host, and `docker logs` reads it back. Other drivers ship the stream straight to syslog, journald, Fluentd, GELF, cloud log services, or nowhere (`none`). The driver is fixed at container creation — changing it means recreating the container.

## The pipeline

An application that logs to stdout needs no log files, no rotation inside the container, and no log shipping agent: the engine treats the two streams of the main process as the container's log. Drivers available in the engine include `json-file` (default), `local` (a compressed binary format optimized for the same host), `syslog`, `journald`, `fluentd`, `gelf`, `awslogs`, `splunk`, `etwlogs` (Windows), `gcplogs`, and `none`. A per-container override looks like:

```bash
docker run -d --name api \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  api:1.42
```

**Listing 1.** The default driver with rotation: at most 3 files of 10 MB, so one container's logs are capped at ~30 MB inside the host's per-container directory under /var/lib/docker/containers.

With `json-file` rotation, the oldest file is deleted when the cap is reached — lines outside the window are gone, not archived. The `local` driver exists for exactly this high-volume case and defaults to 5 files of 20 MB, compressed; it is the docs' recommended default when logs stay on the host. `docker logs --tail N --since 10m --follow` works against drivers that support reading back; `--follow` streams the live stdout/stderr of PID 1, which is also the first diagnostic for a container that dies ([[How do you debug a container that exits immediately]]).

```yaml
# daemon.json — fleet-wide default
{
  "log-driver": "local",
  "log-opts": { "max-size": "20m", "max-file": "5" }
}
```

**Listing 2.** Cluster-wide rotation policy in the daemon config; per-container `--log-driver`/`--log-opt` wins over it.

## Where this breaks in interviews

Three recurring traps. First, an application that writes log **files** inside the container instead of stdout: `docker logs` shows nothing, rotation never applies, and the writable layer fills up ([[What is the difference between volumes and bind mounts in Docker]] covers where data should live instead) — the twelve-factor style is "log to stdout, let the platform ship it". Second, `docker logs` silently produces nothing for non-reading drivers like `fluentd` or `none`: the stream went to the remote system, and `none` means discarded — yet people run `docker logs` expecting output. Third, log options must be set at creation: `docker container update` has no log settings, so a rotation fix means a rebuild of the container, ideally through Compose or an orchestrator ([[What changes when you move a Docker Compose stack to production]] shows where the log policy belongs there).

> [!warning] Rotation is a rolling window, not retention
> `max-size`/`max-file` implement "keep the newest N megabytes" — the oldest chunks are deleted, so post-incident analysis a week later may find nothing. If retention matters, ship the stream out of the node (fluentd/syslog/gelf drivers) instead of growing json-file forever, because an unrotated default quietly eats the host disk and takes the daemon's storage down with it.

> [!tip] Interview answer
> Docker redirects the container's stdout and stderr to a logging driver chosen at container creation — json-file by default, with local, syslog, journald, fluentd, gelf and cloud drivers as alternatives. json-file stores JSON lines under the container directory and rotates by max-size and max-file; docker logs simply reads that back. The classic pitfall: an app writing files inside the container bypasses the whole pipeline, and with shipping drivers docker logs shows nothing by design.
