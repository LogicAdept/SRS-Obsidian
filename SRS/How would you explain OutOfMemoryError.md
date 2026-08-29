<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory #SRS

# How would you explain `OutOfMemoryError`?

> [!abstract] Short answer
> **It is an unchecked `Error` (`VirtualMachineError`) the JVM throws when it cannot satisfy an allocation.** The **detail message** names the pool that failed — Java heap, Metaspace, GC-overhead policy, native thread creation, and others. It is not one bug with one fix, and catching it is not recovery.

## Same type, different pools

`OutOfMemoryError` sits under `Error`, not under `Exception`. `catch (Exception)` does not catch it ([[What is java.lang.Error]], [[What is VirtualMachineError]], [[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]]).

The JVM throws it when an object (or other reserved resource) cannot be allocated and the collector cannot make enough room. Native code can throw the same type when a native allocation fails. `throw new OutOfMemoryError()` from Java does **not** exhaust a pool.

Read the text after the colon. Typical HotSpot messages:

- **`Java heap space`** — a Java object would not fit in the heap (`-Xms` / `-Xmx`). Often `-Xmx` is too small; it is **not** automatically a leak. A leak is a growing **live set after full GC**.
- **`GC overhead limit exceeded`** — GC ran almost all the time (about 98% of time, under 2% recovered, for several collections in a row). That policy is about the **Java heap**, not PermGen. Live data barely fits. `-XX:-UseGCOverheadLimit` only silences that policy.
- **`Metaspace`** — class metadata in native memory hit `MaxMetaspaceSize`. **`PermGen space`** is the pre-JDK 8 message (`-XX:MaxPermSize`). `-Xmx` does not size either ([[What is the difference between PermGen space and Metaspace OutOfMemoryError]]).
- **Native thread creation** — the JVM reports resource exhaustion that is **not** Java-heap exhaustion. Heap-dump-on-OOME flags do not apply. Older HotSpot text: `unable to create new native thread` ([[How do you diagnose memory pressure and OutOfMemoryError]]).
- **`Requested array size exceeds VM limit`** — length past this VM’s max array length, **even if the heap has free space** ([[What is OutOfMemoryError Requested array size exceeds VM limit]]).

`StackOverflowError` is a different `VirtualMachineError`: stack frames, not heap objects ([[How would you explain StackOverflowError OutOfMemoryError]], [[How do you produce a StackOverflowError]], [[How do you reproduce an OutOfMemoryError in Java]], [[How would you explain errors that surface at the JVM level]]).

```d2
direction: down
oom: "OutOfMemoryError" {
  width: 280
  height: 50
}
heap: "Java heap space\nGC overhead" {
  width: 280
  height: 70
}
meta: "Metaspace\n(PermGen before 8)" {
  width: 280
  height: 70
}
native: "native thread / swap\narray length limit" {
  width: 300
  height: 70
}
oom -> heap
oom -> meta
oom -> native
```

**Fig. 1.** One `Error` type; the detail string names which resource failed.

```java
class Demo {
    static void retain() {
        java.util.List<byte[]> hold = new java.util.ArrayList<>();
        while (true) {
            hold.add(new byte[1_000_000]);
        }
    }
}
```

**Listing 1.** Reachable allocations under a small `-Xmx` typically surface as `Java heap space`, not as Metaspace or an oversize-array message.

> [!warning] `OutOfMemoryError` is not always a leak
> Heap space and GC-overhead messages also fire when the heap is simply too small for a healthy live set. Confirm the live set after full GC before hunting leaks.

> [!warning] Do not catch and continue, and do not “fix” GC-overhead by turning it off
> After a true resource collapse the VM may already be unusable. `catch (Error)` / `catch (Throwable)` can swallow it without fixing the pool ([[Why should you not catch java.lang.Error]]). `-XX:-UseGCOverheadLimit` only hides the policy; the heap is still too full for progress.

> [!tip] Interview answer
> **`OutOfMemoryError` is a `VirtualMachineError`: the JVM could not complete an allocation.** The detail message tells you which pool failed — heap, Metaspace, GC overhead, native threads, or an oversize array. Raising `-Xmx` only helps heap-shaped messages, and catching the `Error` is not a fix.
