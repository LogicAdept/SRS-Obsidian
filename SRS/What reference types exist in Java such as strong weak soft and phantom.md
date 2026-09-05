<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/References #SRS

# What reference types exist in Java such as strong weak soft and phantom?

> [!abstract] Short answer
> Ordinary Java pointers are **strong**. `java.lang.ref` adds three **reference objects**, weakest last: **soft**, **weak**, **phantom**. Reachability is **strong → soft → weak → phantom → unreachable**. Soft refs are for memory-sensitive **caches**; weak refs for **canonicalizing maps** that must not pin keys; phantom refs (and **`Cleaner`**) for **post-mortem** cleanup. Cycles among **strong** refs still die when nothing can reach them from a thread without crossing a reference object — [[What is the difference between SoftReference and WeakReference]], [[What JVM runtime memory regions exist]].

## Four strengths, one collector

**Strong.** Reachable by some thread **without** traversing a `Reference`. A `new` result starts strongly reachable from the creating thread. While any strong path exists, the object is not softly/weakly/phantom reachable.

**Soft (`SoftReference`).** Not strong, but reachable by traversing a **soft** ref. The GC **may** clear those refs under **memory demand**, and **must** have cleared every soft ref to a softly reachable object **before** `OutOfMemoryError`. Intended for **caches**. HotSpot’s `-XX:SoftRefLRUPolicyMSPerMB` only **hints** how long a softly reachable object may linger per free heap megabyte.

**Weak (`WeakReference`).** Not strong or soft, but reachable by traversing a **weak** ref. When the GC **determines** that, it **atomically clears** those weak refs and the object becomes **finalizable**. It does **not** wait for heap pressure. Canonicalizing maps: `WeakHashMap` uses weak **keys** and polls a `ReferenceQueue`.

**Phantom (`PhantomReference`).** Not strong, soft, or weak; **has been finalized**; and a phantom ref still refers to it. The collector **clears** those refs and **enqueues** registered ones. **`get()` always returns `null`** so the referent cannot be resurrected. Prefer **`Cleaner`**: it is built on phantom refs + a queue; the cleaning `Runnable` must **not** capture the object being cleaned.

Notification: construct the ref with a `ReferenceQueue` (phantom with a **null** queue is never enqueued). Some time after the matching reachability change, the GC clears the ref and **enqueues** it. Keep the **`Reference` object itself** strongly reachable, or it will never appear on the queue.

```java
import java.lang.ref.PhantomReference;
import java.lang.ref.ReferenceQueue;
import java.lang.ref.SoftReference;
import java.lang.ref.WeakReference;

public final class RefKindsDemo {
    public static void main(String[] args) {
        Object strong = new Object();
        SoftReference<Object> soft = new SoftReference<>(new byte[64]);
        WeakReference<Object> weak = new WeakReference<>(new Object());
        ReferenceQueue<Object> queue = new ReferenceQueue<>();
        PhantomReference<Object> phantom =
                new PhantomReference<>(new Object(), queue);
        System.out.println(phantom.get());
        System.out.println(strong != null && soft.get() != null);
        System.out.println(weak.get());
        System.out.println(queue.poll());
    }
}
```

**Listing 1.** `strong` is a plain pointer. Soft/weak `get()` can still see the referent until the GC clears the ref. Phantom `get()` is **always** `null`; watch **`queue`** (or use `Cleaner`) instead.

```d2
direction: down
s: "Strong (ordinary pointer)" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
so: "Soft — caches; cleared before OOME" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}
w: "Weak — maps; cleared when weakly reachable" {
  width: 340
  height: 40
  style.fill: "#fff8e1"
}
p: "Phantom / Cleaner — post-mortem; get() is null" {
  width: 360
  height: 40
  style.fill: "#fce4ec"
}
s -> so -> w -> p: "weaker"
```

**Fig. 1.** Strength is a **reachability** lattice, not four heap generations. An object is classified by the **strongest** remaining path.

> [!warning] Not JLS “reference types”
> JLS **reference types** are class, array, and interface types versus **primitives**. Soft/weak/phantom are **`java.lang.ref`** wrappers around a **referent**. Mixing the two terms fails interviews.

> [!warning] Weak is not “next GC”; phantom is not `get()`
> Weak refs clear when the collector **notices** weak reachability — there is no “first collection” guarantee, and they ignore free heap. Soft refs can **outlive** a GC if memory is plentiful. Phantom **`get()` is always `null`**, even before enqueue. A strong **cycle** is still collected when it is not reachable from a thread; reference counting is not how the JVM GC works.

> [!tip] Interview answer
> Java has strong references plus SoftReference, WeakReference, and PhantomReference, from strongest to weakest. Soft is for caches and must be cleared before OutOfMemoryError; weak is for maps that must not pin keys; phantom is for cleanup after finalization and get always returns null. Prefer Cleaner for post-mortem work, and do not confuse this with JLS class-versus-primitive reference types.
