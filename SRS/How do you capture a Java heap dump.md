<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #Java/JVM/Tuning #SRS

# How do you capture a Java heap dump?

> [!abstract] Short answer
> On a live process: **`jcmd <pid> GC.heap_dump /path/dump.hprof`** (add `-all` to include unreachable objects). The same HPROF file comes from `jmap -dump:live,format=b,file=... <pid>`. For failures you cannot be standing next to: launch with **`-XX:+HeapDumpOnOutOfMemoryError`** and **`-XX:HeapDumpPath=/path`**, and the JVM writes the dump when `OutOfMemoryError` is thrown. Both tools pause the JVM and **trigger a full GC by default** — only live objects land in the file unless you ask for all — [[What is a heap dump and a thread dump]], [[How do you find the cause of a memory leak in Java]].

## Attach, flag, or MBean

- **`jcmd`** — `GC.heap_dump [options] <filename>`: `-all` dumps **all objects including unreachable** (skips the pre-dump full GC), `-gz=<1..9>` compresses, `-overwrite` replaces an existing file. Must run on the same machine with the same effective user as the JVM.
- **`jmap`** — `jmap -dump:live,format=b,file=heap.hprof <pid>`; without `live` it dumps **all** objects. The tool is marked experimental/unsupported; `jcmd` is the supported path.
- **On `OutOfMemoryError`** — `-XX:+HeapDumpOnOutOfMemoryError` (off by default) writes the dump where `-XX:HeapDumpPath` points (a directory or file path; `-XX:HeapDumpGzipLevel=1..9` gzips it). This is the dump you actually get from a 3 a.m. production crash.
- **From inside** — the `HotSpotDiagnosticMXBean` (`dumpHeap`) and JConsole do the same without shell access; container images without JDK tools can use them, or a JFR event for allocation profiling instead of a full dump.

```bash
jcmd -l                                       # find the local Java pid
jcmd 12345 GC.heap_dump -overwrite /tmp/live.hprof
jmap -dump:live,format=b,file=/tmp/live.hprof 12345   # same artifact, older tool
java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/dumps -jar app.jar
```

**Listing 1.** Three ways to the same HPROF file: supported attach (`jcmd`), legacy attach (`jmap`), and the crash-time flag. Open the result in a heap analyzer or an IDE memory profiler.

```d2
direction: down
need: "Need a heap dump" {
  width: 240
  height: 48
  style.fill: "#fff8e1"
}
live: "Process alive?\njcmd GC.heap_dump\njmap -dump:live,..." {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
crash: "Dying on OOME?\n-XX:+HeapDumpOnOutOfMemoryError\n-XX:HeapDumpPath" {
  width: 300
  height: 84
  style.fill: "#fce4ec"
}
file: "HPROF file → analyzer\n(dominator tree, paths to GC roots)" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
need -> live: "can attach"
need -> crash: "no one at the wheel"
live -> file
crash -> file
```

**Fig. 1.** Choose by process state: attach to a live JVM, or pre-arm the flag so the dying JVM leaves the evidence behind.

> [!warning] A default dump is a full GC and only "live" objects
> `GC.heap_dump` **requests a full GC** unless `-all` is given, and the file holds only reachable objects — a stop-the-world pause on a big heap, plus a file roughly as large as the live set (hundreds of MB to GBs: check disk space). Taking `-all` dumps in a loop to "watch the leak" is the wrong tool: live-set growth is what GC logs and histograms show — [[Which JVM flags are commonly set when launching a Java process]].

> [!tip] Interview answer
> For a live JVM I run `jcmd <pid> GC.heap_dump path.hprof` — it pauses the app, forces a full GC and writes an HPROF file with live objects (`-all` adds unreachable ones, `-gz` compresses). `jmap -dump:live,...` produces the same file but is the legacy tool. For production failures I always launch with `-XX:+HeapDumpOnOutOfMemoryError` and `HeapDumpPath`, so the crash itself leaves a dump to analyze. A heap dump is not a thread dump: one shows the object graph, the other shows stacks.
