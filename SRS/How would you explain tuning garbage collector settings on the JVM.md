<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #Java/JVM/Tuning #SRS

# How would you explain tuning garbage collector settings on the JVM?

> [!abstract] Short answer
> **Measure first, then set the heap and a pause or throughput goal — do not start from a bag of generation flags.** On Java 21 let G1 run with defaults, give it `-Xmx` (and usually `-Xms`), optionally `-XX:MaxGCPauseMillis`, and read `-Xlog:gc*`. `-Xss` is thread stack, not GC. `-XX:+PrintGCDetails` is replaced by unified logging.

## Order of knobs

The Java 21 guide’s first move is: run the app and **let the VM pick the collector**, then change **heap size** if needed, then pick Serial / Parallel / G1 / ZGC only if the goal still fails ([[How does garbage collection work on the JVM]], [[Can developers control garbage collection or JVM memory settings]]).

For **G1** (usual default) the tuning chapter is blunt: keep defaults, set a pause-time goal if you must, and set maximum heap with `-Xmx`. G1 is aimed at small, uniform pauses at high throughput, not max throughput and not lowest latency. Relax `MaxGCPauseMillis` or grow the heap for throughput; tighten the pause target for latency. **Do not pin the young generation** with `-Xmn`, `-XX:NewRatio`, and friends — young size is how G1 meets the pause goal; a fixed nursery **disables** that control. When moving from CMS or Parallel, **strip old GC flags** and leave `-Xmx` / optional `-Xms` plus the pause goal.

Heap flags (HotSpot extra options, not portable to every JVM):

- `-Xms` — minimum **and** initial heap (multiple of 1024, > 1 MB).
- `-Xmx` — maximum heap (multiple of 1024, > 2 MB); same as `-XX:MaxHeapSize`. Default max is chosen at run time. Servers often set `-Xms` equal to `-Xmx`.
- `-XX:MaxMetaspaceSize` — class metadata, **not** the Java heap.
- `-Xss` — **thread stack** size (platform default, e.g. 1024 KB on Linux/x64). It is not a young-gen or collector flag.

`-XX:MaxGCPauseMillis` is a **soft** G1 goal (default 200 ms). Parallel is for throughput when one-second pauses are acceptable; ZGC (`-XX:+UseZGC -XX:+ZGenerational` in 21) when pauses must stay around a millisecond ([[What is G1 GC]], [[How would you explain major garbage collector algorithms on the JVM]]).

Logs: `-verbose:gc` still prints GC events. Legacy `-XX:+PrintGCDetails` maps to **`-Xlog:gc*`**. G1 diagnosis starts at `-Xlog:gc*=debug` and looks for `Pause Full (G1 Compaction Pause)` and `(Evacuation Failure)`. Full GCs from `System.gc()` are mitigated with `-XX:+ExplicitGCInvokesConcurrent` (G1) or ignored with `-XX:+DisableExplicitGC` ([[How do you diagnose memory pressure and OutOfMemoryError]], [[Which JVM flags are commonly set when launching a Java process]]).

```d2
direction: down
run: "Run with defaults\nlog gc*" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}
heap: "Set -Xmx / -Xms\nnot a nursery pin" {
  width: 220
  height: 55
  style.fill: "#fff8e1"
}
goal: "Pause goal or\nswitch collector" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
run -> heap
heap -> goal
```

**Fig. 1.** Logs and live set first. Heap second. Collector or pause goal last.

```text
java -Xms2g -Xmx2g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -Xlog:gc*:file=gc.log \
  -XX:+DisableExplicitGC \
  YourApp
```

**Listing 1.** A sane G1 starting point: fixed heap, default-ish pause *goal*, unified GC log, ignore `System.gc()`. Add `-Xss` only if threads overflow the stack — not to “tune GC.”

> [!warning] `-Xmn` fights G1
> A fixed young generation overrides pause-time control. The same dump that lists `-Xms`/`-Xmx` often adds `-Xmn` from Parallel-era recipes. On G1, delete it.

> [!warning] `PrintGCDetails` is not the modern switch
> Use `-Xlog:gc*` (or `-Xlog:gc*=debug` while hunting Full GCs). `-Xloggc:` is documented as replaced by `-Xlog:gc:`.

> [!tip] Interview answer
> **Start with G1 defaults, a measured heap, and GC logs — not a pile of generation flags.** `-Xmx`/`-Xms` size the heap; `MaxGCPauseMillis` is a soft goal; do not pin `-Xmn` on G1. `-Xss` is thread stack, and `PrintGCDetails` is now `-Xlog:gc*`. Change collector only after the live set and logs say the current one cannot hit the goal.
