<!--
reps: 0
priority: 0
-->
#Java/JVM/GarbageCollector #SRS

# How does the garbage collector decide an object can be collected?

> [!abstract] Short answer
> **When the object is unreachable from GC roots.** HotSpot traces from live threads and other VM-internal roots. If there is no path, the object is eligible — a cycle among the unreachable objects does not save them. Soft, weak, and phantom refs sit on a weaker ladder; they do not count as strong reachability.

## Reachability from roots, not a count

A **reachable** object is one a live thread could still use in a continuing computation. Reachability is transitive through ordinary fields: if `A` is reachable and `A.next` is `B`, then `B` is reachable. HotSpot collectors are tracing: they mark what they can walk to from **GC roots** and treat the rest as garbage. There is no per-object counter to get stuck on a cycle ([[How does garbage collection treat cyclic references between live objects]]).

HotSpot names roots as references from an **active thread** and **internal JVM** structures. In the language rules that matches:

- **Live threads** — locals, parameters, and the operand stack that a thread might still use. A compiler may treat a stack local as dead once it is no longer used, even before you assign `null`. Heap fields are not rewritten that way.
- **Statics** — a `static` field keeps an object if that write still holds and the class’s **loader** is itself reachable. A class can be unloaded only when its defining loader can be reclaimed.
- **JNI** — the VM tracks objects passed to native code so the collector will not free them. A **local** JNI reference pins for the native call; a **global** reference pins until `DeleteGlobalRef`. A **weak global** reference does *not* prevent collection.

G1’s per-pause “roots” are the narrower set needed to evacuate a collection set (VM internals, code, and the rest of the heap). That is the same idea applied to a subset of regions, not a second definition of liveness ([[How does garbage collection work on the JVM]]).

`java.lang.ref` then grades what tracing found:

| Strength | Meaning |
| --- | --- |
| Strongly reachable | A thread can reach it without traversing a `Reference` object. Newly allocated objects start here. |
| Soft / weak / phantom | Only reachable through those reference types. |
| Unreachable | None of the above. **Eligible for reclamation.** |

Weakly reachable objects may be cleared and made finalizable first. **Finalizer-reachable** objects (only reachable from something waiting for `finalize`) are not reclaimable until after that dance. Interview talk of “is garbage” usually means **not strongly reachable**; “may the collector reuse the bits” means **unreachable** on that ladder. Timing of the actual collection is unspecified; eligibility is not a promise that the next `System.gc()` reclaims the bytes ([[What reference types exist in Java such as strong weak soft and phantom]], [[How would you explain what counts as garbage from the JVM perspective]]).

```d2
direction: down
roots: "GC roots\n(live thread, reachable statics, JNI, VM internals)" {
  width: 420
  height: 70
  style.fill: "#e8f5e9"
}
live: "strongly reachable cluster" {
  width: 280
  height: 50
}
dead: "no path from a root\neligible, even if A ⇄ B" {
  width: 280
  height: 60
  style.fill: "#ffebee"
}
roots -> live
live -> dead: "drop the last root path"
```

**Fig. 1.** The collector asks “is there a path from a root?”, not “does anything still point here?”

```java
final class Node {
    Node other;
}

public final class Reachability {
    static Node pin;

    public static void main(String[] args) {
        Node a = new Node();
        Node b = new Node();
        a.other = b;
        b.other = a;
        pin = a;          // root: static of a live class
        a = null;
        b = null;         // locals gone; cycle still live via pin
        pin = null;       // no root path; both eligible
    }
}
```

**Listing 1.** Mutual fields do not decide liveness. Clearing `pin` does. The objects become eligible; the VM still chooses *when* to reclaim.

> [!warning] Eligible is not “collected on the next line”
> Unreachable means the collector *may* reuse the storage. It does not mean the heap shrinks now, or that `System.gc()` will do it. Finalizers and `Cleaner` run only after reachability changes, and they can delay reclamation.

> [!warning] Scope ending is not a GC event
> Leaving a block does not collect anything by itself. The object becomes garbage when it is unreachable; a collection happens later when that generation fills (or an explicit `System.gc()` hint is honored).

> [!warning] JNI weak globals are not pins
> Ordinary JNI local/global references keep the object. `NewWeakGlobalRef` is documented to allow collection; treating it like `NewGlobalRef` is a leak in the other direction (use-after-free in native code).

> [!tip] Interview answer
> **The GC traces from roots — live threads, reachable statics, JNI and other VM internals — and collects objects with no path.** Cycles among those objects are fine; cycles with no root are garbage. Soft/weak/phantom references are a weaker ladder, not extra roots. Unreachable means eligible, not “freed in the next statement.”
