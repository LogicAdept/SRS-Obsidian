<!--
reps: 0
priority: 0
-->
#Java/Concurrency/VirtualThreads #SRS

# How would you explain Virtual Threads synchronized?

> [!abstract] Short answer
> In **Java 21**, a virtual thread that is **inside a `synchronized` method or block** (or blocked on that monitor, including **`Object.wait`**) is **pinned** to its **carrier**: it **cannot unmount**, so blocking I/O there also blocks the **platform** thread. Frequent long pinning **starves** the scheduler (carrier cap, default **256**). The 21-era fix is **`ReentrantLock`** (and other `java.util.concurrent.locks`), which **do not pin**. **Java 24** makes **`synchronized` release the carrier**; you then pick `synchronized` vs `Lock` for API reasons, not pinning. Native frames still pin. Overview: [[How would you explain Virtual Threads]]. Monitors: [[How would you explain monitor locks and intrinsic locks in Java]]. Locks: [[How would you explain synchronization with synchronized and locks in Java]].

## Pinning is a carrier, not a deadlock of your lock

The JVM used to record the **platform carrier** as the monitor owner. Unmounting inside `synchronized` would let another virtual thread on that carrier look like it held the monitor — so the VM **forbade unmount**. `synchronized` itself still works; the app is not “wrong.” Scalability dies when many VTs **block while pinned** (socket `read` inside `synchronized getData()`).

**Java 21** (and 22–23): two pin cases — **`synchronized`**, and a **`native` method / foreign function**. Diagnostics: JFR **`jdk.VirtualThreadPinned`** (default threshold 20 ms); **`-Djdk.tracePinnedThreads=full|short`**. Do **not** rewrite rare or **in-memory** `synchronized`; change the ones that **often** wrap **long I/O**. **`java.io`** streams were reworked in 21 so typical I/O does not pin via their own monitors.

**Java 24:** monitors are owned by the **virtual thread**. Blocking to enter, or `wait`/`notify` re-acquire, **unmounts**. `jdk.tracePinnedThreads` is **gone** (ignored). JFR remains for **leftover** pins: native code that calls back into Java and blocks, and a few **class-load / initializer** cases.

```java
synchronized byte[] getData() {          // Java 21: pin for the whole body
    return in.readAllBytes();            // blocking I/O holds the carrier
}

final ReentrantLock lock = new ReentrantLock();
byte[] getData21() {
    lock.lock();
    try {
        return in.readAllBytes();        // 21: can unmount; still exclusive
    } finally {
        lock.unlock();
    }
}
```

**Listing 1.** The classic 21 interview pair. From 24, the `synchronized` version also unmounts; keep `ReentrantLock` if you already migrated or need timed/interruptible acquire.

```d2
direction: down
s: "inside synchronized" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
p21: "Java 21: pinned to carrier" {
  width: 220
  height: 40
  style.fill: "#ffebee"
}
p24: "Java 24: unmount OK" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
n: "native / FFM on stack" {
  width: 200
  height: 36
  style.fill: "#f3e5f5"
}
s -> p21
s -> p24
n -> p21: "still pinned"
```

**Fig. 1.** `synchronized` pinning is a **21–23** carrier rule. Native pinning remains.

> [!warning] Pinning is not “synchronized is broken”
> Mutual exclusion still holds. The failure mode is **too few carriers** (deadlock/starvation of *other* virtual threads), not a lost monitor.

> [!warning] Native still pins after 24
> JNI or FFM frames on the stack still keep the carrier. Do not promise “no pinning ever” on a current JDK.

> [!tip] Interview answer
> In Java 21 a virtual thread inside synchronized is pinned to its carrier, so blocking I/O there blocks a platform thread; we used ReentrantLock for those hot I/O sections. From Java 24 synchronized unmounts like other blocking, so I do not rewrite every monitor for virtual threads. Native code can still pin.
