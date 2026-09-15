<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# What is a safepoint in the JVM and how does it enable a garbage collection pause?

> [!abstract] Short answer
> **A safepoint is a program point at which all GC roots are known and all heap object contents are consistent — the OpenJDK HotSpot Glossary requires that "all threads must block at a safepoint before the GC can run."** A stop-the-world pause is not threads vanishing at an arbitrary instruction: each running thread executes until it reaches a safepoint and blocks there, which is why collector phases that scan roots can only start once every thread has arrived.

## The definition, and what it freezes

The glossary defines a **safepoint** as "a point during program execution at which all GC roots are known and all heap object contents are consistent". From the global view, "all threads must block at a safepoint before the GC can run", with one carve-out: "threads running JNI code can continue to run, because they use only handles" — native code talks through handles the GC may update, so those threads keep working until they re-enter Java or block at the safepoint themselves. From the local view, "a safepoint is a distinguished point in a block of code where the executing thread may block for the GC. Most call sites qualify as safepoints." This is the mechanical precondition behind every stop-the-world pause ([[What is a stop the world pause in garbage collection and why do collectors minimize it]]): freeze the mutators at points where their stack, registers, and fields form a complete, stable root set ([[What structures does the garbage collector analyze to find garbage]]).

| Glossary concept | Role at a safepoint |
| --- | --- |
| **Safepoint** | Program point where the thread may block for the GC; "strong invariants" hold only there |
| **GC roots** | Pointers into the heap from outside it — stacks, registers, statics — that are consistent at the safepoint |
| **GC map** | JIT-emitted description of where oops live in a compiled frame; "each code location which might execute a safepoint has an associated GC map" |

## How compiled code meets the pause

Two implementation details from the glossary make safepoints cheap and sound. First, density: "most call sites qualify as safepoints", so threads do not have to run long before reaching one — the delay before a pause is the time for the slowest thread to arrive, not an arbitrary wait. Second, compilation: the JIT compilers emit a **GC map** for every code location that might execute a safepoint, describing "the locations of oops in registers or on stack in a compiled stack frame" — an **oop** being HotSpot's term for a pointer to a Java object. That map is how collector threads walking a paused thread's frame can find every reference without understanding the compiled code's internals. The glossary adds an optimization consequence: "both compiled Java code and C/C++ code may be optimized between safepoints, but less so across safepoints", because invariants valid between safepoints may break across them.

```java
// Safepoints are invisible in source — the JVM places them. You can watch
// them through unified logging (tag: safepoint):
//   java -Xlog:safepoint -Xmx64m SafepointDemo
//
// Representative output (shape varies by release):
//   [0.9s] Safepoint "G1: Concurrent Start Cleanup", Time since last: ..., Reaching safepoint: 0.045ms
//   [2.1s] Safepoint "Revoke biases" ...
class SafepointDemo {
    public static void main(String[] args) throws Exception {
        for (int i = 0; i < 10; i++) {
            byte[] churn = new byte[2 * 1024 * 1024]; // triggers GC safepoints
            java.util.Objects.requireNonNull(churn);
        }
        System.out.println("app code never mentions safepoints");
    }
}
```

**Listing 1.** The application does nothing special — the VM inserts safepoint checks into compiled code and logs each global stop with the time spent "reaching" it, the pause-to-safepoint delay that precedes any collector work.

```d2
direction: down
t1: "Thread A runs\n(call site = safepoint)" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
t2: "GC requested\nevery thread must arrive" {
  width: 260
  height: 55
  style.fill: "#fff8e1"
}
blocked: "All threads block\nat their safepoints" {
  width: 260
  height: 55
  style.fill: "#ffebee"
}
scan: "GC scans roots and heap\nvia GC maps, handles" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
resume: "Threads resume" {
  width: 200
  height: 45
  style.fill: "#f3e5f5"
}
t1 -> t2 -> blocked -> scan -> resume
```

**Fig. 1.** The pause begins only when the last running thread reaches a safepoint; collector work then proceeds against a frozen, fully-mapped root set.

> [!warning] A safepoint is a program point, not the pause itself
> Calling the pause "a safepoint" inverts the mechanism: the safepoint is where a thread *may* block, and the global stop happens after every thread has arrived. The glossary also restricts its scope — safepoints and GC maps are HotSpot/OpenJDK implementation vocabulary, not JVMS or JLS terms.

> [!warning] JNI is the sanctioned exception
> Threads inside JNI code keep running during a safepoint because they hold objects only through handles, which the GC can update under them. They must block when they would load handle contents or re-enter Java. Saying "native threads never stop for GC" or "JNI pauses everything instantly" are both wrong.

> [!tip] Interview answer
> **A safepoint is a program point where all GC roots are known and the heap is consistent; every thread must block at one before GC work can run.** Compiled code carries safepoints at most call sites, the JIT emits GC maps so the collector can read oops out of paused frames, and JNI threads keep running on handles. Stop-the-world pauses start only once all threads have reached a safepoint — even concurrent collectors use them for root-scanning phases.

Related: [[What is ZGC]], [[What is G1 GC]], [[How does the garbage collector decide an object can be collected]], [[What are Minor GC and Full GC]]
