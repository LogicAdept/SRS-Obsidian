<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the shared kernel pattern in DDD context mapping?

> [!abstract] Short answer
> A shared kernel is an explicitly bounded subset of the domain model that two contexts own together: the teams agree on the contained types, integrate them into each context's model, and jointly approve every change before it ships. It is the highest-coupling choice on the context map, and it works only when the shared subset stays small and guarded.

## How the kernel is built

The teams pick the minimal vocabulary both contexts genuinely need - identity types, a few value objects, maybe one canonical calculation - and designate that code as the kernel. Everything in the kernel is a joint model, not "their library": neither team may rename, repurpose, or release a kernel change unilaterally, because both contexts' models depend on it. In practice the kernel is its own module with its own version, consumed by both sides, and both sides run integration checks against it in their builds. The moment one team can change the kernel without the other's build passing, it is not a shared kernel anymore - it is just a copy.

```java
// The kernel: one jointly owned module, one version, two consumers.
static final class Kernel {
    static final String VERSION = "2";                      // agreed by both teams
    record CustomerId(long value) {}
    static long normalize(long customerId) { return Math.abs(customerId); }
}
// Both contexts call Kernel.normalize, so the result is identical by construction.
System.out.println(up.expose(id));       // 42
System.out.println(down.accept(id));     // customer/42
// Joint CI guard: a unilateral kernel change fails this check before it ships.
if (!Kernel.VERSION.equals(expected)) throw new IllegalStateException("kernel version drift");
```

**Listing 1.** Verified on JDK 21.0.12.1: upstream and downstream see identical normalization because there is exactly one kernel; the version guard is the joint check both teams run.

```d2
direction: right
up: "Upstream context" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
down: "Downstream context" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
kernel: "Shared kernel\nsmall jointly owned subset\njoint approval for changes" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
up -> kernel: "owns and consumes"
down -> kernel: "owns and consumes"
```

**Fig. 1.** The kernel is not a service or an API - it is a shared model fragment with two owners, which is exactly why its size is the critical constraint.

## When the pattern pays

A shared kernel fits when two contexts are so intertwined that translating every exchange costs more than coupling - typical for identity types and money types that both sides compute against, or when a coordinated legacy migration needs a stable common core. The alternative for almost everything else is looser: open host service with a published language for wide consumption, or an anti-corruption layer when the upstream model is hostile ([[What are the open host service and published language patterns]], [[What is the anti-corruption layer pattern]]). The kernel's appeal is zero translation; its price is coordinated release planning and the loss of autonomous evolution in exactly the area you shared. The full menu of choices sits on the context map ([[What is context mapping in DDD]]).

> [!warning] The kernel grows until it is a distributed monolith
> Every dispute about where a type lives resolves too easily into "put it in the kernel" - and the kernel creeps from two types to a shared business layer with a shared schema and a shared release train. The rule that keeps it honest: adding to the kernel must be harder than translating once, and every kernel addition needs both teams' sign-off. If the kernel needs a roadmap meeting of its own, it is already too big.

> [!tip] Interview answer
> A shared kernel is a deliberately small subset of the model that two bounded contexts own jointly: shared types, joint approval for every change, integration checks in both builds. It removes all translation between the two contexts but couples their release cycles, so it is reserved for the few types that both sides genuinely compute against - and kept aggressively small.

