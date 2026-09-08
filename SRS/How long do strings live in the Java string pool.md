<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM/Memory/Heap #SRS

# How long do strings live in the Java string pool?

> [!abstract] Short answer
> Pooled strings are **ordinary, GC-managed heap objects** — "forever" is a myth. A **literal** lives as long as its declaring **class** stays loaded: the resolved constant-pool entry holds the reference, and when the class becomes unreachable its literals are collectable with it. A **runtime** `intern()`ed string lives as long as it is reachable from code; HotSpot cleans table entries whose strings become garbage. Inspect with `jcmd <pid> VM.stringtable` or `-XX:+PrintStringTableStatistics` — [[What is the Java string pool]], [[How does Java represent data in memory]].

## Who holds the reference decides the lifetime

- **Literals** — after resolution, the class's run-time constant pool keeps a reference to the shared instance ([[How do string literals enter the Java string pool]]). Class reachable → literal reachable. In an app server, classes are tied to their **classloader**: as long as the loader is pinned, every literal of every class it loaded stays alive — one reason classloader leaks hurt so much ([[What is Metaspace and how does it differ from PermGen]]).
- **Runtime `intern()`** — the string is a normal object; nothing resurrects it once your code drops it. The table's references are maintained by the JVM so that unreachable strings do not accumulate; exact cleaning behavior is an implementation detail, which is why the table statistics, not folklore, are the debugging tool.
- **G1 string deduplication is a different mechanism** — `-XX:+UseStringDeduplication` (G1) merges the backing `byte[]` of *duplicate* `String` objects; it does not touch pool identity and does not need `intern()`.

```bash
jcmd <pid> VM.stringtable -all                 # verbose table dump
jcmd <pid> VM.stringtable                      # statistics: buckets, entries
java -XX:+PrintStringTableStatistics -jar app.jar   # stats at JVM exit
```

**Listing 1.** The supported views of the string table: entry counts, bucket load, and per-literal sizes. Growth between two reads points at code that interns heavily; a flat table under load is healthy.

```d2
direction: right
cls: "Class, reachable\nvia its classloader" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
  cp: "constant pool\n(resolved entry)" {
    width: 200
    height: 40
  }
}
str: "pooled String instance" {
  width: 260
  height: 48
  style.fill: "#e3f2fd"
}
code: "your code's locals / fields" {
  width: 270
  height: 48
  style.fill: "#fff8e1"
}
cls.cp -> str: "holds while class is loaded"
code -> str: "runtime intern: caller holds"
```

**Fig. 1.** Two references keep a pooled string alive: the declaring class's constant pool (literals) and ordinary reachability from code (runtime `intern()`).

> [!warning] Both absolutes are wrong
> "Interned strings live for the JVM's lifetime" — true only for literals of classes that are never unloaded; a runtime-`intern()`ed string dies with its last reference. "The pool leaks memory" — HotSpot's table entries for dead strings are reclaimed, so churn is cost, not a leak. The genuinely unbounded case is *your code* holding interned values in a growing collection — [[How do you find the cause of a memory leak in Java]].

> [!tip] Interview answer
> The pool stores references to normal heap objects, so lifetime follows reachability. A literal is held by its class's constant pool, so it lives exactly as long as that class does — which is why classloader leaks pin strings too. A runtime `intern()`ed string is just a referenced object; HotSpot reclaims dead entries. I watch it with `jcmd VM.stringtable` or `PrintStringTableStatistics`, and I don't confuse G1's string deduplication, which merges backing arrays, with the pool.
