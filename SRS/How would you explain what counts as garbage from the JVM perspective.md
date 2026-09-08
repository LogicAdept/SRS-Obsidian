<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# How would you explain what counts as garbage from the JVM perspective?

> [!abstract] Short answer
> **Garbage is a heap object no live thread can still use — unreachable from GC roots.** It is not “a local I am done with,” not a primitive in a frame, and not “something still has a field pointing here.” Soft/weak/phantom and finalizers are a delay on the way to reclamation, not extra strong life.

## What the collector is allowed to reuse

The JVM heap holds **class instances and arrays**. Those are what the garbage collector reclaims. An instance counts as garbage when it is **unreachable**: it cannot appear in any potential continuing computation from a **live thread**. HotSpot traces from GC roots (that thread’s still-live locals and operand-stack references, statics of a reachable loader, JNI local/global refs, other VM internals). No path → garbage, even if the object graph is a knot of mutual fields ([[How does the garbage collector decide an object can be collected]], [[How does garbage collection treat cyclic references between live objects]]).

What does **not** count as garbage in that sense:

- A **primitive local** (`int n` in a frame). It is not a heap object. The frame is popped when the method returns; that is not a GC of `n`.
- A **reference local** that the compiler has proved will never be used again. The *object* may already be garbage while the slot still exists; the slot itself is not “collected.”
- **Method-area / Metaspace** class metadata. It goes away when the class is unloaded because its **loader** became garbage — a different pool than `-Xmx` ([[What JVM runtime memory regions exist]]).
- Objects that are only **softly, weakly, or phantom-reachable**, or **finalizer-reachable**. They are not strongly reachable, but they are not yet reclaimable storage in the `java.lang.ref` / finalization sense ([[How does the garbage collector decide an object can be collected]], [[What reference types exist in Java such as strong weak soft and phantom]]).

So “garbage from the JVM’s perspective” is **unreachable heap objects**. The popular slogan “objects with no references” is wrong twice: cycles have references and are still garbage; a forgotten `static` is a reference and they are not.

```d2
direction: down
heap: "Heap instances and arrays" {
  width: 280
  height: 50
}
q: "Path from a GC root\n(without a Reference object)?" {
  width: 300
  height: 60
  style.fill: "#fff8e1"
}
live: "not garbage" {
  width: 160
  height: 45
  style.fill: "#e8f5e9"
}
dead: "garbage\n(eligible to reclaim)" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
heap -> q
q -> live: "yes"
q -> dead: "no"
```

**Fig. 1.** Only heap objects enter the question. The answer is reachability from roots, not a count of fields.

```java
public final class WhatIsGarbage {
    static Object root;

    public static void main(String[] args) {
        int local = 1;                    // not a heap object
        Object a = new Object();          // heap; reachable from a local
        Object b = new Object();
        a = b;                            // first instance: no root path → garbage
        root = b;                         // b's instance is not garbage
        root = null;                      // now it is
        System.out.println(local);
    }
}
```

**Listing 1.** `local` never becomes GC garbage. The first `new Object()` does, the moment nothing reachable still names it — including after `a = b`, while `b` stays live.

> [!warning] Garbage is not “out of scope”
> Leaving a block does not collect. The object is garbage when unreachable; a collection runs later when that generation fills (or a hint is honored). A `static` that still points into a discarded graph means **no** garbage there yet.

> [!warning] Native and off-heap are outside this definition
> JNI **pins** heap objects (local/global refs). Direct buffers and `malloc` in native code are not Java-heap garbage; leaking them will not look like a young-gen chart ([[How does garbage collection work on the JVM]]).

> [!tip] Interview answer
> **Garbage is unreachable heap objects — instances and arrays the GC may reuse.** The JVM traces from roots; cycles without a root count as garbage, and a leftover static does not. Stack primitives and Metaspace are different stories. Soft/weak/phantom refs mean “not strongly reachable yet,” not “already collected.”
