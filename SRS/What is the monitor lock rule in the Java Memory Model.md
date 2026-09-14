<!--
reps: 0
priority: 0
-->

#Java/JMM #Java/Concurrency/Synchronization #SRS

# What is the monitor lock rule in the Java Memory Model

> [!abstract] Short answer
> **An unlock of a monitor synchronizes-with every subsequent lock of the same monitor (JLS 17.4.4), so an unlock happens-before the next lock (JLS 17.4.5).** Everything the releasing thread wrote before leaving the critical section becomes visible to whichever thread enters it next — this is the classic guard-and-publish idiom.

The edge is pairwise but its effect is transitive: because program order links all of a thread's earlier actions to its unlock, and the unlock links to the next thread's lock, *all* writes the first thread performed before unlocking — not only writes to fields "protected" by that lock — become visible after the corresponding lock. That is why a single shared monitor is enough to publish an arbitrarily large object graph ([[How would you explain the happens-before guarantee in the Java Memory Model]]). The JLS also notes that `Object.wait` has lock and unlock actions associated with it: releasing the monitor on `wait` and reacquiring it on wake-up weave the same edges, which is one reason wait/notify only works while holding the monitor ([[Why must wait and notify run inside synchronized blocks]]).

```d2
direction: right
t1: "Thread 1" {
  w: "data = 42" { style.fill: "#e3f2fd" }
  u: "unlock(m)\n(exit synchronized)" { style.fill: "#fff3e0" }
  w -> u: "program order"
}
t2: "Thread 2" {
  l: "lock(m)\n(enter synchronized)" { style.fill: "#fff3e0" }
  r: "reads data -> 42" { style.fill: "#e8f5e9" }
  l -> r: "program order"
}
u -> l: "synchronizes-with\n(release -> acquire)"
```

**Fig. 1.** The unlock→lock edge closes the chain, so the plain write `data = 42` is visible in Thread 2. The source of the edge is a *release*, the destination an *acquire*.

```java
class Box {
    private int data;
    private final Object monitor = new Object();

    void put(int v) {
        synchronized (monitor) {   // release of the previous holder happens-before this lock
            data = v;
        }                          // unlock: release
    }

    int get() {
        synchronized (monitor) {   // lock: acquire
            return data;           // guaranteed to see the latest completed put
        }
    }
}
```

**Listing 1.** Two synchronized blocks on the same monitor. The write `data = v` by the previous writer is visible to every later reader because unlock happens-before the next lock of that monitor.

> [!warning] The edge exists only for the same monitor
> Unlocking monitor A and locking monitor B produces no edge — "synchronized on different objects" is the classic way to break this rule, and it silently degrades to a data race ([[What is monitor in Java]]). Two more traps. One: mutual exclusion and visibility are bundled for monitors but conceptually different — the visibility guarantee is what the memory model adds on top of the "one thread at a time" property. Two: with explicit `Lock` objects the same guarantee comes from the j.u.c synchronizer property, and forgetting `unlock` in a `finally` does not just deadlock — it also publishes nothing ([[What memory consistency do synchronizer release and acquire guarantee in Java]]).

> [!tip] Interview answer
> **An unlock on a monitor happens-before every subsequent lock of that same monitor. Since happens-before is transitive, all writes made before the unlock are visible after the matching lock — this is how synchronized blocks safely publish data. The rule is per-monitor: different monitors give no edge, and wait/notify participate through their associated lock and unlock actions.**
