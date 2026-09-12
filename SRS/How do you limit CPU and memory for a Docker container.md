<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Java/Runtime #SRS

# How do you limit CPU and memory for a Docker container

> [!abstract] Short answer
> `docker run --memory 512m --cpus 1.5` writes cgroup limits: memory over the hard limit triggers the kernel OOM killer against the container's main process (exit 137, `State.OOMKilled=true`), and CPU is enforced by the scheduler quota. Related knobs: `--memory-swap`, `--cpu-shares` (relative weight), `--cpuset-cpus`. Unbounded is the default — a container without `--memory` can starve the whole host.

## What each flag actually does

`--memory` sets the cgroup memory hard limit (RAM + page cache); `--memory-swap` bounds RAM+swap together and defaults to twice the memory limit, so a container may page before being killed (`--memory-swap -1` allows unbounded swap). `--cpus 1.5` maps to the CFS quota — 150% of one core per period — while `--cpu-shares` (default 1024) only matters under contention: it weights how idle CPU is split, it is not a reservation. `docker update --memory --cpus` changes limits on a running container; `docker stats` reads the same cgroup counters back ([[How does Docker isolate containers with Linux namespaces and cgroups]] is the mechanism underneath).

```bash
docker run -d --name api \
  --memory 1g --memory-swap 1g \
  --cpus 1.5 \
  api:1.42
docker update --memory 2g api          # live resize
docker stats --no-stream api          # usage vs limit, today
```

**Listing 1.** Memory-swap equal to memory disables swapping for the container — over-limit allocations are killed instead of paged.

## The two different "out of memory" failures

This distinction is the senior-level payload of the topic. A **JVM heap** exhaustion is handled inside the process: `OutOfMemoryError` is thrown, shutdown hooks run, the process exits with its own code. A **cgroup** breach is handled by the kernel: the OOM killer SIGKILLs the process, exit code 137, no hooks, `OOMKilled: true` in inspect. Both failure modes look identical from the outside (`docker ps` shows Exited), and blaming the JVM for an OOM kill without checking `State.OOMKilled` is the classic misdiagnosis ([[How do you debug a container that exits immediately]] walks the inspect path):

```bash
java -Xmx32m JVMOome
# Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
# 	at JVMOome.main(JVMOome.java:8)
java exit code after OOME: 1
```

**Listing 2.** Observed on Temurin 21: a heap OOME exits 1 gracefully. The cgroup OOM kill would instead show exit 137 with `OOMKilled=true` — a kernel decision, not a JVM one.

For JVM services the limits and the runtime must agree: modern JVMs read the cgroup limits (container support) and size the heap from `MaxRAMPercentage`, so `--memory 1g` plus the default 25% gives a ~256 MB heap that survives [[How does the JVM detect container memory and CPU limits]] — provided the image is not an old JDK 8 build that ignores cgroups and sizes heap from host RAM, the fastest route to repeated 137s.

> [!warning] CPU shares are weights, not guarantees
> `--cpu-shares 2048` promises nothing on an idle host and everything only under contention; treating it as a quota is a classic misread. The second trap: `--memory` without `--memory-swap` still allows the container to page to swap at 2× the limit — a "memory-limited" service that starts thrashing instead of dying. And the JVM-specific lie: "the JVM always sees container limits" — true only for cgroup-aware builds (JDK 10+ backported to 8u191), on cgroup v1 and v2 hosts alike.

> [!tip] Interview answer
> Memory and CPU limits are cgroup settings: --memory is a hard limit whose breach makes the kernel OOM-kill the container with exit 137 and OOMKilled true, --cpus is a CFS quota, --cpu-shares is only a contention weight, and --memory-swap bounds paging — set it equal to memory to forbid swap. A JVM heap OutOfMemoryError is a different beast: the process handles it and exits with code 1. Container-aware JVMs size the heap from these cgroup limits via MaxRAMPercentage, so the flag and the runtime have to agree.
