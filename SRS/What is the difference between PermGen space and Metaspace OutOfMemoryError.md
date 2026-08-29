<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #Java/JVM/Memory #SRS

# What is the difference between PermGen space and Metaspace `OutOfMemoryError`?

> [!abstract] Short answer
> **`OutOfMemoryError: PermGen space` is the pre-JDK 8 message: the permanent generation (class metadata on the Java heap, sized with `-XX:MaxPermSize`) is full.** **From JDK 8, PermGen is gone.** Class metadata lives in native **Metaspace**. Exhausting it (when a cap is set) is **`OutOfMemoryError: Metaspace`**. Raising `-Xmx` does not size either pool.

## Two eras, two metadata pools

`OutOfMemoryError` is an unchecked `Error`. The **detail message** names which pool failed ([[What is java.lang.Error]], [[What is VirtualMachineError]], [[Are Error subclasses checked or unchecked]]).

**PermGen (JDK 7 and earlier):** `PermGen space` means the permanent generation is full — the heap area that stored class and method metadata. Tune with `-XX:PermSize` / `-XX:MaxPermSize`. A very large number of loaded classes is the usual cause. `-Xmx` sizes the object heap, not MaxPermSize.

**Metaspace (JDK 8+):** The permanent generation was **removed**. Class metadata is allocated in **native memory**. By default that native use is **unlimited**. `-XX:MaxMetaspaceSize` sets a cap. When native memory needed for metadata exceeds that cap, the VM throws `OutOfMemoryError` with detail **`Metaspace`**. `-XX:MetaspaceSize` is a GC high-water mark, not the old PermSize replacement in the “hard ceiling” sense. On JDK 9+, leftover `-XX:MaxPermSize` is **ignored** with a warning ([[How do you reproduce an OutOfMemoryError in Java]], [[How do you diagnose memory pressure and OutOfMemoryError]], [[How would you explain OutOfMemoryError]]).

`Java heap space` is still a different message: objects, not class metadata ([[What is OutOfMemoryError Requested array size exceeds VM limit]], [[Does catch Exception also catch Error]]).

```d2
direction: right
perm: "JDK 7: PermGen space\n(-XX:MaxPermSize)" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
meta: "JDK 8+: Metaspace\n(-XX:MaxMetaspaceSize)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
heap: "Java heap space\n(-Xmx)" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
perm -> meta: "removed in JDK 8"
```

**Fig. 1.** Metadata OOM versus object-heap OOM.

```java
class Demo {
    // Conceptual: exhaust class metadata, not the object heap.
    // Pre-8:  java -XX:MaxPermSize=64m …
    // 8+:     java -XX:MaxMetaspaceSize=8m …
    static Class<?> loadOne() throws ClassNotFoundException {
        return Class.forName("com.example.Generated0");
    }
}
```

**Listing 1.** One `Class.forName` is not enough to OOM. Dumps generate `Metaspace` by defining or loading **many** classes under a tiny `MaxMetaspaceSize`. The same idea with `MaxPermSize` produced `PermGen space` on older JDKs.

> [!warning] `-Xmx` does not fix metadata OOM
> Heap OOM (`Java heap space`) and PermGen/Metaspace OOM are different pools. A larger object heap does not raise `MaxPermSize` or `MaxMetaspaceSize`.

> [!warning] `PermGen space` is obsolete on modern JDKs
> You will not see that message on JDK 8+. The current class-metadata message is `Metaspace`. `Compressed class space` is a third, related detail when compressed class pointers run out of their own region.

> [!tip] Interview answer
> **`PermGen space` is the old, pre-8 class-metadata `OutOfMemoryError`, tuned with `MaxPermSize`.** **From JDK 8, PermGen is gone and metadata is in native Metaspace; a cap is `MaxMetaspaceSize`, and the message is `Metaspace`.** Neither is fixed by raising `-Xmx`.
