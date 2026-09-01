<!--
reps: 0
priority: 0
-->
#Java/Language/Object/Finalize #Java/JVM/GarbageCollector #Java/Legacy #SRS

# What happens to finalization if `finalize` runs slowly or throws an exception?

> [!abstract] Short answer
> **Slow `finalize` postpones that object’s finalization** (and, on HotSpot, every later finalizer on the same thread). The instance stays **finalizable** until the method returns; its storage is not reused yet. **A thrown exception ends finalization of that object immediately**: the exception is **ignored**, `finalize` is **not** called again, and other finalizers can still run. Neither case is specified to stop the GC. Non-finalizable garbage can still be collected.

## Two failure modes, two outcomes

An object is **unfinalized**, then **finalizable** (the VM may invoke `finalize`), then **finalized** after that automatic invocation. Storage is reclaimed only after the object is unreachable **and** that step has happened. `finalize` runs **at most once**.

**If it runs slowly or blocks.** Finalization of **that** instance is still in progress. Anything reachable only from it stays tied up. The language allows **several** finalizer threads and **any** order, even concurrent calls — a slow one need not stop a second thread. **JDK 21 HotSpot** uses **one** daemon `"Finalizer"` thread that `queue.remove()`s and runs `runFinalizer` **sequentially**, so a blocked `finalize` **stalls the drain**: later `Finalizer` refs sit on the queue, finalizable objects **accumulate**, native resources leak, the heap can fill. `System.runFinalization` / `Runtime.runFinalization` may start a short-lived `"Secondary finalizer"` thread **because** the main one can be deadlocked. Ordinary objects **without** a real `finalize` are not on this queue ([[How would you explain the finalize method in Java and why it is discouraged]]).

**If it throws.** Uncaught exceptions during finalization are **ignored**; finalization of **that** object **terminates**. HotSpot’s `runFinalizer` is `catch (Throwable x) { }`. The object is not finalized a second time. The Finalizer thread (if it got as far as the `catch`) continues with the **next** queue entry. The collector is **not** aborted and does **not** freeze: objects **without** a real `finalize` can still be reclaimed while a finalizer is stuck. What stalls is **finalizer draining**. Enough blocked finalizable objects still **fill the heap**.

```d2
direction: right
slow: "finalize blocks\nstill finalizable" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
thr: "HotSpot Finalizer\nthread stuck in call" {
  width: 220
  height: 80
  style.fill: "#ffebee"
}
ex: "finalize throws\ncatch Throwable" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
done: "that object done\n(no retry) · next queued" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
slow -> thr
ex -> done
```

**Fig. 1.** Slow = drain stuck, object still waiting. Throw = this object finished (badly), queue can move.

```java
try {
    jla.invokeFinalize(finalizee);
} catch (Throwable x) {
    // ignored — this instance will not be finalized again
}
```

**Listing 1.** Conceptual: JDK 21 `Finalizer.runFinalizer`. A throw does not unwind the VM or the GC.

```java
// Conceptual: JDK 21 FinalizerThread body (not a public API)
for (;;) {
    Finalizer f = (Finalizer) queue.remove();
    f.runFinalizer(jla);
}
```

**Listing 2.** Conceptual: one daemon thread, sequential `queue.remove()`. A `finalize` that blocks never returns to this loop.

`--finalization=disabled` skips scheduling entirely, so neither stall nor throw from `finalize` occurs.

> [!warning] Do not say “the GC hangs”
> The collector can still discover garbage and reclaim objects that **are not** waiting on `finalize`. What stalls is **finalizer draining**. Enough blocked finalizable objects still **fill the heap** (or leak native resources) as if the collector were “broken.”

> [!warning] Throw is not a retry
> People treat a failed `finalize` like a failed constructor. It is not: the method **already ran**. Resources it did not release stay leaked unless something else closes them. Logging inside `finalize` can disappear because the exception is discarded.

> [!warning] “Sequential Finalizer” is not in the JLS
> Interview answers that say “the Finalizer thread processes FIFO” describe **HotSpot**. The spec allows concurrent `finalize` on many threads. A slow finalizer **always** delays **that** object; it delays **others** when they share a thread.

> [!tip] Interview answer
> **A slow `finalize` keeps that object finalizable and, on HotSpot, blocks the single Finalizer thread so other finalizable objects queue up.** A throw is swallowed, that object’s finalization ends with no second call, and the collector keeps running. Do not use `finalize` for anything that must complete or must surface errors.
