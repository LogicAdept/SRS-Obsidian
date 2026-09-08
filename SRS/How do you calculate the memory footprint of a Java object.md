<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #SRS

# How do you calculate the memory footprint of a Java object?

> [!abstract] Short answer
> The language fixes no sizes; on 64-bit HotSpot with compressed oops an object is a **12-byte header** (8-byte mark word + 4-byte class pointer), its **non-static fields**, and padding to the **8-byte** alignment boundary. So `new Integer(7)` is 12 + 4 = **16 bytes**, a `Long` is 12 + 8 = **24 bytes** (padding), an `int[N]` array is 16 + 4·N, and an empty `String` object is **24 bytes** plus its backing `byte[]`. Measure, don't guess: `Instrumentation.getObjectSize`, the JOL library, or `jcmd <pid> GC.class_histogram` — [[How much memory does an Integer object use compared with int]], [[How do you find the cause of a memory leak in Java]].

## The layout arithmetic

With `UseCompressedOops` on (the default up to ~32 GB heaps; the flag exists since JDK 7 — check `java -XX:+PrintFlagsFinal -version`):

- **Header** — mark word 8 bytes (identity hash, lock state, GC age) + compressed class pointer 4 bytes = 12 bytes.
- **Fields** — references 4 bytes each when compressed; `long`/`double` 8; `int`/`float` 4; `short`/`char` 2; `byte`/`boolean` 1.
- **Arrays** — header + a 4-byte **length** slot + elements: `byte[N]` = 16 + N, `int[N]` = 16 + 4·N, `Integer[N]` = 16 + 4·N **plus each element object** (16 bytes or `null`).
- **Padding** — total rounded up to 8 bytes.
- JDK 24 (JEP 450, compact object headers) can shrink the header to **8 bytes** when enabled.

A `String` object holds 4-byte `value` reference + `int hash` + `byte coder` + `boolean hashIsZero` + padding = 24 bytes, *in addition to* the separate `byte[] value` array (16 + n bytes for Latin-1).

```java
import java.lang.instrument.Instrumentation;

public class Sizer {
    static Instrumentation inst; // injected via a -javaagent premain

    public static void main(String[] args) {
        Object o = new Object();
        Integer i = 7;
        long[] a = new long[3];
        System.out.printf("Object=%d Integer=%d long[3]=%d%n",
                inst.getObjectSize(o), inst.getObjectSize(i), inst.getObjectSize(a));
        // typical 64-bit HotSpot, compressed oops: 16 / 16 / 40
    }
}
```

**Listing 1.** `getObjectSize` reports the **shallow** size of one object — the agent must be attached as `-javaagent` at launch, and the result is an implementation-specific estimate, valid for comparison within one JVM.

```d2
direction: down
hdr: "Header 12 B\nmark 8 + klass 4" {
  width: 260
  height: 60
  style.fill: "#fff8e1"
}
fields: "fields\n(refs 4 B compressed)" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
pad: "padding → multiple of 8 B" {
  width: 260
  height: 44
  style.fill: "#e8f5e9"
}
arr: "array: +4 B length slot\nthen element values" {
  width: 260
  height: 56
  style.fill: "#fce4ec"
}
hdr -> fields -> pad
fields -> arr: "only for arrays"
```

**Fig. 1.** HotSpot object layout with compressed oops: 12-byte header, fields, 8-byte alignment; arrays add a length slot before the elements.

> [!warning] Shallow size is not the memory the object costs
> A `HashMap` object itself is small; the buckets array and every entry and key/value it points at make up its **retained** size. Histograms and `getObjectSize` answer the shallow question; retention math is what heap-dump analyzers (dominator tree) do. Quoting "a HashMap is 48 bytes" in an interview is the classic trap — [[How do you diagnose memory pressure and OutOfMemoryError]].

> [!tip] Interview answer
> There is no `sizeof` in Java. On 64-bit HotSpot with compressed oops: 12-byte header (mark word + class pointer), fields, padding to 8 bytes — `Integer` 16, `Long` 24, `int[N]` 16 + 4N, an empty `String` 24 plus its byte array. For real numbers I measure: `Instrumentation.getObjectSize` via an agent, JOL for layout, or `jcmd GC.class_histogram` on a live process — and I separate shallow size from retained size.
