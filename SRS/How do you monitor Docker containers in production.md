<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How do you monitor Docker containers in production

> [!abstract] Short answer
> The engine's built-in observability surface is four commands: `docker stats` (live CPU/memory/network/block metrics read from cgroups), `docker events` (a real-time stream of state changes), `docker system df` (disk usage), and `docker logs`. They answer "what is happening now" on one host; history, dashboards, and alerting need an exporter plus Prometheus/Grafana or a SaaS equivalent.

## The built-in surface

`docker stats` streams per-container rows — CPU %, memory used versus limit, network and block I/O, and PIDs — and `--no-stream` snapshots once, which is what you want in scripts and dashboards' health checks. `docker events --filter type=container --filter event=die` is the audit trail: start, die, oom, health_status, and every API action appear as they happen. `docker system df` shows how much of the host the images, containers, volumes, and build cache occupy ([[How do you clean up unused Docker objects and dangling images]] pairs with it).

```bash
docker stats --no-stream
docker events --since 10m --filter type=container
docker inspect --format '{{.State.OOMKilled}} {{.State.ExitCode}}' api
```

**Listing 1.** The first-response trio: a point-in-time resource snapshot, the recent state history, and the verdict on why a container died.

The numbers are not magic: the engine reads the container's cgroup accounting files. On this cgroup-v1 host the same counters are directly visible, which is exactly what a metrics exporter polls:

```text
cpuacct.usage (total CPU ns for this cgroup): 47855600491
memory.usage_in_bytes: 1769861120
memory.limit_in_bytes: 4294967296
VmRSS:	    1964 kB
```

**Listing 2.** Observed cgroup files on a 4 GB-limited pod: CPU time in nanoseconds, memory usage against the hard limit — the same figures `docker stats` renders as percentages ([[How do you limit CPU and memory for a Docker container]] defines those limits).

A production setup layers three levels: **host metrics** from cAdvisor or a node exporter (the cgroup numbers above, aggregated), **engine events** forwarded into the log pipeline for alerting on restart loops and OOM kills, and **application metrics** from inside the container — a JVM service exposes its own JMX/Micrometer endpoints ([[How does the JVM detect container memory and CPU limits]] shows where the JVM reads its limits), because the engine cannot see garbage-collection pauses or thread-pool saturation.

> [!warning] docker stats is a flashlight, not a monitoring system
> The CLI surface is per-host, stateless, and point-in-time: no history, no cross-host view, no alerts — and `docker events` only streams while you are connected, so an incident between connections is invisible unless events were shipped somewhere. The classic gap: memory% looks fine because cgroup usage counts RAM, while the real symptom — swap thrashing or cache pressure — lives in counters the CLI row never shows.

> [!tip] Interview answer
> Built in, I get docker stats for live cgroup metrics, docker events for the state-change stream — die, oom, health_status — docker system df for disk, and inspect State for exit codes and OOMKilled. Those counters come from cgroup files, which is exactly what cAdvisor and node exporters scrape into Prometheus. For a JVM service I add application metrics from inside, because the engine cannot see GC pauses or pool saturation. The CLI is for the first five minutes; history and alerting need the exporter stack.
