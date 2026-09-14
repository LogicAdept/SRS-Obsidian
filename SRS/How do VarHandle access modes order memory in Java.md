<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency/Atomics #SRS

# How do VarHandle access modes order memory in Java

> [!abstract] Short answer
> **`VarHandle` (JDK 9+) exposes per-access memory ordering: `getVolatile`/`setVolatile` give the full volatile semantics, `getAcquire`/`setRelease` give one-way release-acquire ordering, `getOpaque`/`setOpaque` give only per-variable coherence, and plain `get`/`set` are unordered; separate fence methods — `fullFence`, `acquireFence`, `releaseFence`, `loadLoadFence`, `storeStoreFence` — control ordering directly.** The atomic classes are built on these modes.

The modes form a strength ladder. Volatile mode is the familiar full guarantee: a `setVolatile` publishes everything before it to any later `getVolatile` of that variable ([[What is the volatile visibility rule in the Java Memory Model]]). Acquire-release mode is strictly weaker: `setRelease` orders the releasing thread's prior writes only against a later `getAcquire` of the *same* variable — it does not provide the sequentially consistent read-write discipline volatile has, which makes it cheaper and suitable for one-directional flags and state machines. Opaque mode guarantees only coherence — a thread sees the latest write to that variable in a total order per variable — with no cross-variable ordering at all. The JDK source of `java.util.concurrent.atomic` states it directly: instances of Atomic classes maintain values "using methods otherwise available for fields using associated atomic `VarHandle` operations" ([[How would you explain Java atomic types in java.util.concurrent.atomic]]).

```d2
direction: right
vol: "getVolatile / setVolatile\nfull volatile hb semantics" { style.fill: "#e8f5e9" }
acr: "getAcquire / setRelease\none-way release-acquire pair" { style.fill: "#fff3e0" }
opq: "getOpaque / setOpaque\ncoherence per variable only" { style.fill: "#e3f2fd" }
plain: "get / set\nno ordering" { style.fill: "#f5f5f5" }
vol -> acr: "weaker"
acr -> opq: "weaker"
opq -> plain: "weaker"
```

**Fig. 1.** The access-mode ladder from strongest to weakest ordering. `compareAndSet`/`getAndSet` operate at volatile strength; their `weak...` variants may spuriously fail with weaker constraints.

```java
static final VarHandle STATE;               // created via MethodHandles.lookup

volatile-ordered:
STATE.setVolatile(this, 1);                 // release + more
int v = (int) STATE.getVolatile(this);      // acquire + more

one-way publication:
STATE.setRelease(this, 1);                  // publishes writes made before it
int r = (int) STATE.getAcquire(this);       // acquires them — same variable only
```

**Listing 1.** Volatile mode for full mutual ordering; acquire-release for cheaper one-way publication. In the JDK source itself `FutureTask` stores its terminal state with `STATE.setRelease(this, NORMAL)` and `get()` acquires it — release-acquire chosen deliberately over the more expensive volatile mode ([[What memory consistency does Future get guarantee in Java]]).

> [!warning] Acquire-release is not volatile, opaque is not acquire-release
> The release-acquire pair gives no promise across *different* variables and no sequential consistency for mixed read/write patterns — replacing a volatile with setRelease/getAcquire is only correct when the communication is genuinely one-way per variable ([[What is the difference between compareAndSet and weakCompareAndSet]]). Opaque guarantees neither: it only prevents a thread from reading a stale-to-it value forever on that one variable. Plain mode and fences are expert-level tools — the fence names (loadLoad, storeStore) map to hardware barriers, and misplacing them recreates the data races the ladder exists to avoid ([[What reads does the Java Memory Model allow in a data race]]).

> [!tip] Interview answer
> **VarHandle access modes are the JDK 9 way to choose ordering per access: volatile mode gives full happens-before semantics like a volatile field, acquire-release gives a weaker one-way publication pair on a single variable, opaque gives per-variable coherence only, and fences give raw ordering control. The atomic classes and much of j.u.c are implemented on these modes — for example FutureTask publishing its result state with setRelease.**
