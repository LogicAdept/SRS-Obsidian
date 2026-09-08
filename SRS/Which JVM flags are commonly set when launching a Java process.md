<!--
reps: 0
priority: 0
-->
#Java/JVM/Tuning #SRS

# Which JVM flags are commonly set when launching a Java process?

> [!abstract] Short answer
> The `java` launcher groups flags into **standard** (portable, “most commonly used”), HotSpot **extra** (`-X…`), and HotSpot **advanced** (`-XX…`). In production you almost always set **how to start** (`-cp` / `-jar` / `-m`), **system properties** (`-D`), and a **heap cap** (`-Xmx`, often with `-Xms` the same). Next come GC logs (`-Xlog:gc*`), an OOME heap dump, and only then a collector or pause goal. Stack size is `-Xss`, not a GC flag: [[Which JVM flag controls native thread stack size]].

## Three layers on one command line

Standard options are guaranteed on every JVM implementation: class path, module path, `-D`, assertions, `-verbose:…`, `-version`, agents. Extra `-X` flags (heap, stack, `-Xlog`) and advanced `-XX` flags (collectors, dumps, compressed oops) are **HotSpot-specific** and can change or be absent on another VM.

Boolean `-XX` switches use **`+` to enable** and **`-` to disable**. Sizes take `k`/`m`/`g`. `@argfile` expands a long command line before the VM parses it. `JDK_JAVA_OPTIONS` **prepends** more flags from the environment; it **must not** contain `-jar` or `-h` (the launcher aborts).

Launch shapes: `java [options] MainClass`, `java [options] -jar app.jar` (the JAR’s `Main-Class`; **other class-path settings are ignored**), or `java [options] -m module[/main]`. Class path: [[What is the Java classpath]].

## What production command lines actually pin

**Heap.** `-Xms` is minimum **and initial** heap; `-Xmx` is the maximum (`-XX:MaxHeapSize`). For server deployments the man page notes they are **often set equal** so the heap does not resize in a pause. Defaults are ergonomic (about 1/64 and 1/4 of physical memory, capped by process/container memory and `MaxRAM`). Linux containers: **`-XX:+UseContainerSupport` is on by default**, so those ergonomics see cgroup limits. Metaspace is separate: `-XX:MaxMetaspaceSize`. GC tuning after the heap: [[How would you explain tuning garbage collector settings on the JVM]].

**Logs and dumps.** JDK 9+ unified logging: `-Xlog:gc` (old `PrintGC`) and `-Xlog:gc*` (old `PrintGCDetails`). `-verbose:gc` still exists as a standard switch. `-XX:+HeapDumpOnOutOfMemoryError` writes an HPROF dump (default `java_pid<pid>.hprof` in the cwd); `-XX:HeapDumpPath` relocates it (`%p` is the pid). Diagnosis: [[How do you diagnose memory pressure and OutOfMemoryError]], [[How do you capture a Java heap dump]].

**Collector / pause (only if needed).** G1 is the usual JDK 21 default (`-XX:+UseG1GC`). Throughput: `-XX:+UseParallelGC`. Low pause independent of heap size: `-XX:+UseZGC` and on 21 `-XX:+ZGenerational`. Soft pause hint: `-XX:MaxGCPauseMillis` (G1 default **200** ms). `-XX:+AlwaysPreTouch` commits heap pages at startup so first-touch stalls do not land in a GC pause.

**Other frequent standard flags.** `-Dname=value` sets a system property (quote values with spaces). Assertions are **off** unless you pass `-ea` / `-enableassertions` ([[How do you enable Java assertions at runtime]], [[Why are Java assertions disabled by default]]). Modules: `--module-path` / `-p`, `--add-modules`. Debug: `-agentlib:jdwp=…`.

```d2
direction: down
std: "standard: -cp -jar -D -ea -verbose" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
x: "extra -X: -Xms -Xmx -Xss -Xlog" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}
xx: "advanced -XX: GC, dump, container" {
  width: 340
  height: 50
  style.fill: "#e3f2fd"
}
std -> x
x -> xx
```

**Fig. 1.** Portable start flags first; HotSpot heap/log flags next; `-XX` only for a measured GC, dump, or container need.

```text
java -Xms4g -Xmx4g \
  -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/log/java/heap.hprof \
  -Xlog:gc*:file=/var/log/java/gc.log:time,uptime,level,tags \
  -Dfile.encoding=UTF-8 \
  -jar app.jar
```

**Listing 1.** Conceptual HotSpot launch: pinned heap, OOME dump, unified GC log, one system property, JAR entry point.

```text
java -cp app.jar:lib/* com.example.Main
java -p mods -m com.example/com.example.Main
```

**Listing 2.** Conceptual: class-path launch (`*` expands to JARs in that directory) versus module launch. `-jar` would ignore `-cp`.

> [!warning] `-X` / `-XX` are not a Java Language Spec contract
> Another JVM may reject or ignore them. Even on HotSpot, **obsolete** flags warn and **removed** flags **error**. `-XX:+PrintGCDetails` is a legacy alias; current logs are `-Xlog:gc*`. Mixing `-XX:ThreadStackSize` (kilobytes) with `-Xss` (bytes) is an off-by-1024 trap.

> [!warning] `-jar` drops your class path; `+` and `-` are easy to flip
> With `-jar`, user classes come from that JAR only. `-XX:-HeapDumpOnOutOfMemoryError` **disables** the dump (the default). `-XX:+UseContainerSupport` is already the Linux default — turning it **off** makes heap ergonomics ignore cgroup memory and can OOME the container.

> [!tip] Interview answer
> I set minus Xmx, often matching minus Xms, plus unified GC logging and HeapDumpOnOutOfMemoryError, then classpath or minus jar and any minus D properties. G1 is the usual default, so I only add a collector or MaxGCPauseMillis after measuring. Minus X and XX flags are HotSpot, assertions stay off unless I pass minus ea, and minus jar ignores a separate class path.
