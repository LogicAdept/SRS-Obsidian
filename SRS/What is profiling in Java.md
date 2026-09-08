<!--
reps: 0
priority: 0
-->
#Java/JVM/Tuning #SRS

# What is profiling in Java?

> [!abstract] Short answer
> Profiling is measuring what a running Java program actually does — which methods consume CPU, where allocation happens, which locks threads fight over — instead of guessing. In the JDK the built-in tool is JDK Flight Recorder (JFR): a low-overhead event framework started with `jcmd <pid> JFR.start` and analyzed with the `jfr` tool or JDK Mission Control. External profilers attach as agents and either sample or instrument bytecode.

## The two measurement strategies

**Sampling** profilers periodically record what each thread is doing and build a statistical picture; overhead is low and near-proportional to the sample rate, but rare events may be missed. **Instrumentation** rewrites bytecode so every method entry/exit (or allocation) is counted; the data is exact per event, but the rewrite itself changes timing and can distort the profile. JFR is sampling-based with preallocated event buffers: the specification targets at most 1% overhead out of the box and no measurable overhead when not enabled, which is why JFR-style recording is considered safe for production while classic instrumentation agents usually are not.

```d2
direction: right
app: "running JVM" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
jfr: "JFR (built-in)\nevents: CPU, allocation, IO, locks" {
  width: 330
  height: 90
  style.fill: "#e8f5e9"
}
agent: "agent (external)\nsampling or bytecode instrumentation" {
  width: 330
  height: 90
  style.fill: "#fff3e0"
}
rec: "recording file (.jfr)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
analysis: "analysis\njfr tool · JMC" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
app -> jfr
app -> agent
jfr -> rec
agent -> rec
rec -> analysis
```

**Fig. 1.** Two sources of profile data — the built-in event framework and external agents — both end in the same recording/analysis step.

## The JDK workflow

JFR ships inside HotSpot: start a recording on a live process, dump it, and inspect it. The `jcmd` diagnostic command controls the recording; the `jfr` command prints and aggregates the file. Older JDKs exposed the `hprof` instrumentation agent, but it was removed in JDK 9 — its heap-dump role lives on in `jcmd GC.heap_dump`.

```java
// Built-in profiling flow (run against a live JVM, <pid> from jcmd -l):
//   jcmd <pid> JFR.start name=app duration=60s filename=rec.jfr
//   jcmd <pid> JFR.dump name=app                 // write events collected so far
//   jfr summary rec.jfr                          // event counts per type
//   jfr view hot-methods rec.jfr                 // aggregated hot spots
```

**Listing 1.** The three commands worth knowing: start a recording, dump it, view hot spots — no restart, minimal overhead.

> [!warning] The profile is not the truth — it is a measurement
> Instrumented profilers add work to every measured call, so small hot methods can dominate the profile only because they were instrumented, and inlining opportunities change under the profiler (the observer effect). Samplers have their own bias: threads are sampled at points the runtime chooses, so results cluster there and short-lived states are undercounted. Treat a profile as a hypothesis generator: reproduce the finding, then verify with a targeted experiment or benchmark. See [[How do you diagnose memory pressure and OutOfMemoryError]] for the memory side and [[What is a heap dump and a thread dump]] for the point-in-time siblings of profiling.

Profiling pairs with flag-level tuning: before profiling, know which flags your JVM already runs with — see [[Which JVM flags are commonly set when launching a Java process]]; for GC tuning driven by profiles, [[How would you explain tuning garbage collector settings on the JVM]].

> [!tip] Interview answer
> Profiling means measuring run-time behavior — CPU per method, allocation sites, lock contention — instead of guessing. In the JDK, JFR is the built-in, production-safe, sampling-based profiler: start it with jcmd JFR.start, analyze with the jfr tool or Mission Control. External profilers attach as agents and either sample cheaply or instrument bytecode exactly — but instrumentation changes timing, so a profile is evidence to verify, not proof.
