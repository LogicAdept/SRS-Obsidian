<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Java/JVM #SRS

# How does the JVM detect container memory and CPU limits

> [!abstract] Short answer
> Container detection (flag `UseContainerSupport`, **default on since JDK 10**, backported to 8u191) makes the JVM read cgroups: the container's memory budget replaces host RAM for heap ergonomics, and the CPU quota/shares determine `Runtime.availableProcessors()`. With detection, the default max heap is 25% of the container budget (`MaxRAMPercentage=25`) — so explicit `-XX:MaxRAMPercentage=75` is the normal production setting. cgroups v2 support arrived in JDK 15.

## The decision chain

The JVM resolves, in order: explicit `-Xmx` (wins outright), then the container memory limit as the basis, then host RAM. Inside the limit basis it applies percentage ergonomics; thread pools (GC threads, `ForkJoinPool.commonPool`) key off the detected processor count, which respects `cpu.max`/quota rather than the host's core count.

```bash
java -XX:+PrintFlagsFinal -version 2>&1 | grep -E "UseContainerSupport|MaxRAMPercentage |ActiveProcessorCount "
#    int ActiveProcessorCount                     = -1            {product} {default}   <- -1: auto-detect
# double MaxRAMPercentage                         = 25.000000     {product} {default}
#   bool UseContainerSupport                      = true          {product} {default}

java -XshowSettings:system -version 2>&1
# Operating System Metrics:
#     Provider: cgroupv1
#     Effective CPU Count: 2
```

**Listing 1.** Observed on Temurin JDK 21.0.12.1 (Linux, this host is itself cgroupv1-containerized): support is on by default, the percentage default is 25, and the system settings dump exposes which provider and CPU budget the JVM sees.

```bash
java -Xlog:os+container=trace -version 2>&1 | head -5
# [0.000s][trace][os,container] OSContainer::init: Initializing Container Support
# [0.000s][debug][os,container] Detected optional pids controller entry in /proc/cgroups
# [0.001s][debug][os,container] Detected cgroups hybrid or legacy hierarchy, using cgroups v1 controllers
# [0.001s][debug][os,container] OSContainer::init: is_containerized() = true because all controllers are mounted read-only (container case)
# [0.001s][trace][os,container] Path to /cpu.cfs_quota_us is /sys/fs/cgroup/cpu,cpuacct/cpu.cfs_quota_us
```

**Listing 2.** The trace log is the debugging tool when sizing puzzles strike: it names the cgroup provider, the controller paths read, and the derived values (quota, period, active processor count).

```d2
direction: down
lim: "container memory limit\n(cgroup memory.max)" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
q: "-Xmx set?\nyes -> wins; no -> continue" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
pct: "MaxRAMPercentage\ndefault 25% of limit\ntypical prod: 75%" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
heap: "max heap sized to limit basis\nGC/thread pools from CPU view" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}
lim -> q -> pct -> heap
```

**Fig. 1.** Heap sizing inside a container: explicit flag, else cgroup limit times percentage — never host RAM when detection is active.

> [!warning] Old JVMs and oversized -Xmx both end as exit code 137, not OutOfMemoryError
> Two classics. A pre-8u191 Java 8 ignores the cgroup: on a 64-core/256-GB host it sizes a huge heap and the kernel OOM-kills the container the moment RSS crosses the limit — the app never sees an `OutOfMemoryError` ([[How do you diagnose memory pressure and OutOfMemoryError]] is the in-heap story, this is the out-of-heap one). Conversely, a hand-set `-Xmx` at or above the container limit leaves nothing for metaspace, code cache, and threads — same OOM-kill. And note `MaxRAMPercentage=25` means a 2-GB container gets a 500-MB heap by default: almost always not what you meant ([[What is the JVM]] sizes the non-heap parts).

> [!tip] Interview answer
> **Since JDK 10 (8u191 backported) the JVM reads cgroups by default: UseContainerSupport makes the container limit the memory basis and CPU quota the processor count; heap defaults to 25% of that basis via MaxRAMPercentage, so production sets ~75 explicitly; cgroups v2 needs JDK 15+. Pre-8u191 JVMs or an -Xmx at the limit end in OOM-killed exit 137 — the kernel kills, the JVM never throws. Debug with -Xlog:os+container=trace.**

