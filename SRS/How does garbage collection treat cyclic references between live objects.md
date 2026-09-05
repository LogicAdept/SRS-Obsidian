<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# How does garbage collection treat cyclic references between live objects?

> [!abstract] Short answer
> **A cycle among live objects is just more ordinary field edges.** If any object in the cycle is strongly reachable from a live thread (or another GC root), the whole strongly reachable cluster stays. The cycle does not get special treatment, and it does not pin objects once no path from a root remains.

## Reachability from roots

An object is **reachable** when some live thread could still use it in a continuing computation. Reachability is **transitive** through ordinary fields: if `A` is reachable and `A.other` refers to `B`, then `B` is reachable too. A two-node cycle `A ⇄ B` is the same rule twice. HotSpot collectors are **tracing**: they start from GC roots (active threads, statics of a live loader, JVM internals) and mark everything they can walk to. A cycle is not a special case in that walk.

Two cases:

1. **Live cycle** — a local, a static, or another live object still points into the ring. Every node on that strong path stays. The collector does not “break” the cycle to free memory.
2. **Dead cycle** — the last root path is gone. The objects still point at each other on the heap, but nothing live can reach them. The whole circularly linked group is unreachable and can be reclaimed together. That is why a parent/child or doubly-linked list does not leak after you drop the structure.

`java.lang.ref` grades this: **strongly reachable** means a thread can reach the object without traversing a `SoftReference`, `WeakReference`, or `PhantomReference`. A cycle of only weak references is not a live strong cluster.

The JVM spec does not mandate tracing versus some other algorithm; it only requires automatic reclamation and that objects are never explicitly deallocated. HotSpot’s collectors do that by tracing. The language still requires that an unreachable circular group can be reclaimed ([[How does the garbage collector decide an object can be collected]], [[How would you explain what counts as garbage from the JVM perspective]]).

```d2
direction: down
root: "GC root\n(live thread / static)" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
a: "A" {
  width: 80
  height: 50
}
b: "B" {
  width: 80
  height: 50
}
dead: "A ⇄ B with no root\nboth reclaimable" {
  width: 260
  height: 60
  style.fill: "#ffebee"
}
root -> a
a -> b: "field"
b -> a: "field"
a -> dead: "drop the root"
b -> dead
```

**Fig. 1.** Tracing follows the cycle from a root and keeps both nodes. The same cycle with no incoming root is garbage.

```java
final class Node {
    Node other;
}

public final class LiveCycle {
    static Node keep;

    public static void main(String[] args) {
        Node a = new Node();
        Node b = new Node();
        a.other = b;
        b.other = a;
        keep = a;
        a = null;
        b = null;             // live cycle: only the static still reaches A, then B
        keep = null;          // dead cycle: mutual fields remain, no root
    }
}
```

**Listing 1.** After `a` and `b` are cleared, `keep` is the root that keeps both nodes. Clearing `keep` leaves only the heap cycle, which is not enough.

> [!warning] A cycle is not a leak by itself
> Two objects that only point at each other, with no path from a live thread, a static of a reachable loader, or other JVM-internal roots, are garbage. The leak pattern is a **forgotten root** (a static cache, a long-lived collection, a listener list), not the back-pointer.

> [!warning] “Still in a local” is not the same as reachable
> A compiler may treat a stack local as dead once it is no longer used, even before you assign `null`. Heap fields of the cycle are not fair game for that rewrite. Clear the *root* you actually still need; do not rely on `System.gc()` to prove the cycle died ([[What reference types exist in Java such as strong weak soft and phantom]]).

> [!tip] Interview answer
> **A cycle among live objects stays live because something reachable still points into it — not because cycles are special.** Drop the last root path and the whole ring is garbage. Parent/child and doubly-linked structures do not leak by themselves; a leak is a forgotten static, collection, or thread that still reaches the graph.
