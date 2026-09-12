<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How do resource requests and limits work in Kubernetes

> [!abstract] Short answer
> A **request** is what a container is *promised*: the scheduler packs pods onto nodes by summing requests, and the runtime gives the container at least that much. A **limit** is the *ceiling*: memory beyond it means the container is killed (`OOMKilled`), CPU beyond it is just throttled. Their combination also assigns the pod a **QoS class** — Guaranteed, Burstable, or BestEffort — which decides who gets evicted first under node pressure.

## Requests drive placement, limits drive enforcement

Requests are a scheduling currency: the kube-scheduler sees every container's CPU and memory request and only places pods where the sum fits the node's allocatable capacity — the actual usage may be far lower, which is exactly how overcommit works. Limits are a runtime currency: memory limits become cgroup caps ([[How does Docker isolate containers with Linux namespaces and cgroups]] — the same cgroup machinery Docker uses), and crossing a memory limit triggers the kernel OOM killer on that container — exit code 137, reason `OOMKilled` on the pod; CPU limits are enforced by the CFS throttler, so a CPU-hungry container is slowed, not killed, which is why CPU starvation shows up as latency spikes and not crashes. Containers may run without requests or limits — that is a scheduling and fairness decision, not a safety one ([[What are the main components of the Kubernetes architecture]] — kubelet and the eviction manager also watch raw usage, not just limits).

QoS is arithmetic, worth memorizing: **Guaranteed** — every container sets both requests and limits and they are equal; **BestEffort** — nothing set; **Burstable** — everything else. Under node memory pressure the kubelet evicts in QoS order, BestEffort first, Guaranteed last, and among equals by usage-over-request. Requests also feed the CPU-weighted scheduling of compressible resources and are what autoscaling reads ([[How does autoscaling work in Kubernetes]] — the HPA target is a percentage *of requests*).

```yaml
containers:
  - name: app
    image: busybox:1.36
    resources:
      requests:
        cpu: 100m
        memory: 64Mi
      limits:
        memory: 128Mi
```

**Listing 1.** The empirics pod's resources block: `100m` is one tenth of a CPU core (millicores), memory in bytes with suffixes; CPU has a request but no limit — deliberately, so bursts throttle rather than starve.

```d2
direction: right
req: "request\nscheduler packs by this" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
mem: "memory limit\nexceeded -> OOMKilled (137)" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
cpu: "cpu limit\nexceeded -> throttled only" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
qos: "QoS: Guaranteed / Burstable / BestEffort\neviction order under pressure" {
  width: 420
  height: 90
  style.fill: "#e8f5e9"
}
req -> mem
req -> cpu
req -> qos: "both set and equal =\nGuaranteed"
```

**Fig. 1.** One knob, two consequences: placement (requests), enforcement (limits — kill vs throttle), and a derived class (QoS) that ranks pods when a node runs out.

> [!warning] A pod exceeding memory is killed, not warned
> The traps: "the node had free RAM" — irrelevant; the *limit* is per-container cgroup cap and the kernel enforces it regardless of node spare capacity. Setting memory request far below limit inflates overcommit and evictions on a full node. CPU limits on latency-sensitive JVM services routinely cause throttling with no signal in app logs — the complaint sounds like GC, the cause is cfs_quota. And omitting requests entirely drops the pod to BestEffort — first against the wall at the first node hiccup ([[How do you debug a Pod that fails to start]] — OOMKilled cycles hide as CrashLoopBackOff).

> [!tip] Interview answer
> Requests are the scheduling promise — the bin-packing input — and the floor the runtime reserves; limits are per-container cgroup ceilings. Memory over limit means the kernel kills the container, OOMKilled, exit 137; CPU over limit is only throttled. Together they set QoS: equal requests and limits is Guaranteed, nothing is BestEffort, in between is Burstable — and eviction under node pressure walks that order. JVM-specifically, requests also feed the container-aware heap sizing, so wrong requests mean wrong heaps.
