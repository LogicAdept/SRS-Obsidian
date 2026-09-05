<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/References #SRS

# What is the difference between `SoftReference` and `WeakReference`?

> [!abstract] Short answer
> Both are **reference objects** weaker than a normal (strong) pointer. A **softly reachable** object is reachable only through a **soft** reference: the GC **may** clear those refs **in response to memory demand**, and **must** have cleared all of them before throwing `OutOfMemoryError`. A **weakly reachable** object is reachable through a **weak** reference and **not** through strong or soft ones: when the GC decides that, it **will** atomically **clear** the weak refs and make the object **finalizable**. Soft → memory-sensitive **caches**; weak → **canonicalizing maps** that must not pin keys — [[What is WeakHashMap used for]], [[How would you explain OutOfMemoryError]].

## Reachability, then a different GC contract

Strongest to weakest: strong → **soft** → **weak** → phantom → unreachable. Phantom refs are for **post-mortem** cleanup (`Cleaner`); they are not this comparison.

**`SoftReference`.** Intended for **memory-sensitive caches**. If the GC finds an object **softly reachable**, it **may** atomically clear all soft refs to it (and to softly-reachable objects that reach it via strong refs). **No** timing or order is specified except: every soft ref to a softly-reachable object is **cleared before** `OutOfMemoryError`. VMs are **encouraged** not to clear recently created or recently used soft refs. A referent that is still **strongly** reachable (actually in use) is **not** cleared — a cache can keep strong refs to hot entries.

**`WeakReference`.** Intended for **canonicalizing mappings**. If the GC finds an object **weakly reachable**, it **will** atomically clear all weak refs to it (and weak refs to other weakly-reachable objects reachable from it via strong and **soft** refs), declare those objects **finalizable**, and later **enqueue** registered refs. Weak refs **do not** stop the referent becoming finalizable and reclaimed.

So: a **soft** chain keeps an object out of the **weak** category. “Collected on the first GC” is wrong for **soft** (discretion) and overstated for **weak** (only once the GC **determines** weak reachability — there must be a collection that notices). `get()` returns `null` after the ref is cleared.

**`ReferenceQueue`:** register at construction; some time after the matching reachability change, the GC clears the ref and **enqueues** it. `WeakHashMap` polls such a queue on access (weak **keys**).

```java
import java.lang.ref.SoftReference;
import java.lang.ref.WeakReference;

public final class SoftVsWeak {
    public static void main(String[] args) {
        Object cached = new byte[1024];
        Object key = new Object();
        SoftReference<Object> soft = new SoftReference<>(cached);
        WeakReference<Object> weak = new WeakReference<>(key);
        cached = null;
        key = null;
        // After a GC: weak.get() is typically null; soft.get() may still be non-null.
        System.out.println(soft.get() + " / " + weak.get());
    }
}
```

**Listing 1.** Dropping the last **strong** refs. Neither `get()` is required to be `null` **before** a GC. After the GC classifies the objects, weak refs **must** be cleared; soft refs **may** remain until memory demand (and **will** be gone before OOME).

```d2
direction: down
obj: "Object" {
  width: 160
  height: 40
}
strong: "strong ref" {
  width: 160
  height: 36
  style.fill: "#e8f5e9"
}
soft: "only SoftReference" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
weak: "only WeakReference" {
  width: 200
  height: 40
  style.fill: "#ffe0b2"
}
obj -> strong: "in use: never cleared"
obj -> soft: "softly reachable: GC may clear"
obj -> weak: "weakly reachable: GC will clear"
```

**Fig. 1.** Same referent, different remaining path. Soft is optional reclamation under memory demand; weak is “do not pin.”

> [!warning] Soft is not “keep until OOME”
> The only hard rule is: softly-reachable objects’ soft refs are **gone before** `OutOfMemoryError`. The GC **may** clear them **earlier**. “Lives until the heap is full” is a slogan.

> [!warning] Weak is not “the next instruction”
> Clearing happens when the collector **determines** weak reachability, not at the assignment `key = null`. Without a GC, `weak.get()` can still return the object. A remaining **soft** or **strong** path means it is **not** weakly reachable.

> [!tip] Interview answer
> Soft references are for caches: the GC may clear them under memory pressure and must clear them before `OutOfMemoryError`. Weak references are for maps that must not keep keys alive: once an object is only weakly reachable, the GC will clear those refs and allow finalization. I do not say weak is “the first GC for sure in wall-clock time,” and I do not promise a soft cache survives until OOME.
