<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# How do concurrent garbage collectors keep the object graph consistent while the application runs?

> [!abstract] Short answer
> **They pair a snapshot rule with small pieces of code on every reference access.** G1 marks a Snapshot-At-The-Beginning taken at its Initial Mark pause; ZGC reads state through colored pointers behind load barriers (plus store barriers in generational mode); Shenandoah reaches every object through an indirection pointer. JEP 439 states the requirement: since the collector "reads and modifies the object graph at the same time as the application, it must take care to give the application a consistent view of the object graph."

## The problem a concurrent tracer must solve

A stop-the-world tracer sees a frozen graph; a concurrent one starts tracing while mutators keep overwriting fields, promoting objects, and allocating. Without extra machinery the tracer can miss a live object — an old object gets a reference to a new one after the old was already traced — and relocating collectors can leave a mutator holding a stale address after the object moved. Every HotSpot concurrent collector therefore combines two ingredients: a rule for what counts as live for this cycle, and a barrier mechanism that enforces the rule at reference reads or writes. All of them still anchor the cycle in stop-the-world pauses ([[What is a stop the world pause in garbage collection and why do collectors minimize it]]).

| Collector | Liveness rule | Barrier mechanism |
| --- | --- | --- |
| **G1** | SATB: everything live at the Initial Mark pause stays live for the cycle | Write-barrier upkeep of remembered sets; STW anchors: Concurrent Start, "two special stop-the-world pauses: Remark and Cleanup" |
| **ZGC** | Colored pointers carry the object's known state | "Load barriers in combination with colored object pointers... enable ZGC to do concurrent operations, such as object relocation, while Java application threads are running" (JEP 333); generational mode adds store barriers (JEP 439) |
| **Shenandoah** | Concurrent marking from scanned roots | "An indirection pointer to every Java object... enables the GC threads to compact the heap while the Java threads are running" (JEP 189) |

## G1: snapshot-at-the-beginning

The guide's G1 chapter is explicit: "G1 marking uses an algorithm called Snapshot-At-The-Beginning (SATB). It takes a virtual snapshot of the heap at the time of the Initial Mark pause, when all objects that were live at the start of marking are considered live for the remainder of marking." The consequence is conservative retention: "objects that become dead (unreachable) during marking are still considered live for the purpose of space-reclamation", which "may cause some additional memory wrongly retained compared to other collectors" — but it "potentially provides better latency during the Remark pause", and "the too conservatively considered live objects during that marking will be reclaimed during the next marking." SATB's cost lands as bookkeeping around reference writes that could overwrite a reference the snapshot still needs ([[What is G1 GC]]).

## ZGC and Shenandoah: barriers and forwarding

ZGC's core design, per JEP 333, is "the use of load barriers in combination with colored object pointers (i.e., colored oops)": "in addition to an object address, a colored object pointer contains information used by the load barrier to determine if some action needs to be taken before allowing a Java thread to use the object" — that is what lets relocation finish while mutators run. JEP 439's generational mode extends the scheme: "a colored pointer is a pointer to an object in the heap which, along with the object's memory address, includes metadata that encodes the known state of the object", and "generational ZGC also uses store barriers to efficiently keep track of references from objects in one generation to objects in another generation. A store barrier is a fragment of code injected by ZGC into the application wherever the application stores references into object fields." Shenandoah solves the moving-object problem differently: mark and compact run concurrently behind "an indirection pointer to every Java object", so pauses are needed only "to scan the thread stacks to find and update the roots of the object graph" — with the project page's summary: "CMS and G1 both perform concurrent marking of live objects. Shenandoah adds concurrent compaction" ([[What is ZGC]], [[What is Shenandoah GC]]).

```java
class ConsistencyDemo {
    static Object holder = new byte[1];

    public static void main(String[] args) {
        Object fresh = new byte[2];
        // 1) A store overwrites holder during a concurrent marking cycle.
        //    SATB (G1): the JIT-emitted write barrier records the OLD value,
        //    so the snapshot's view of the graph stays intact.
        holder = fresh;
        // 2) A read of a moved object under ZGC/Shenandoah goes through the
        //    load barrier / indirection, so the app always sees the new copy.
        System.out.println(holder == fresh);
    }
}
```

**Listing 1.** The Java source shows plain field access; the correctness machinery lives in JIT-inserted barriers the source never displays. The comment traces what each mechanism does at these two lines.

```d2
direction: down
snap: "Cycle starts\nSATB snapshot taken" {
  width: 250
  height: 55
  style.fill: "#fff8e1"
}
trace: "Concurrent trace\nmutators keep running" {
  width: 270
  height: 55
  style.fill: "#e8f5e9"
}
bar: "Store overwrites reference\nbarrier preserves the rule" {
  width: 320
  height: 55
  style.fill: "#ffebee"
}
move: "Relocation\nload barrier or indirection\nfixes stale references" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
snap -> trace -> bar -> move
```

**Fig. 1.** A concurrent cycle stays correct because every reference write or read passes a checkpoint that upholds the cycle's liveness rule; the mutator never observes an inconsistent graph.

> [!warning] Textbook taxonomy is not the guide's vocabulary
> Names like tri-color marking or incremental update describe the same problem in GC literature, but Oracle's documentation for HotSpot says SATB (G1) and colored pointers with load and store barriers (ZGC). Answering a HotSpot question with paper-only terms, or claiming "SATB means only the start matters" while missing the retention cost, reads as recitation rather than understanding.

> [!warning] The machinery is invisible in Java
> Barriers are JIT-interpreted runtime code, not annotations or flags in source. A card or answer that shows "where the barrier is" in Java code as if it were visible is wrong; the observable surface is GC logs, pause names, and throughput effects — plus the JEP-level contract that the application gets a consistent view.

> [!tip] Interview answer
> **Concurrent collectors stay correct by combining a per-cycle liveness rule with reference-access barriers.** G1 uses Snapshot-At-The-Beginning: everything live at Initial Mark stays live, write-barrier bookkeeping protects the snapshot, and retention of dead-during-marking objects is the accepted cost. ZGC puts state metadata into colored pointers and checks it in load barriers — store barriers join in generational mode to track cross-generation references. Shenandoah routes every object through an indirection pointer so concurrent compaction can update references. All still use short stop-the-world pauses for roots and cycle boundaries.

Related: [[What is G1 GC]], [[What is ZGC]], [[What is Shenandoah GC]], [[What is CMS Concurrent Mark Sweep GC]], [[What structures does the garbage collector analyze to find garbage]]
