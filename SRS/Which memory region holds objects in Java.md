<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #SRS

# Which memory region holds objects in Java?

> [!abstract] Short answer
> **Class instances and arrays** are allocated from the **Java heap**, a **shared** run-time area created at VM start. A local variable or field holds a **reference**; the object itself is not stored in the JVM stack frame. Class metadata lives in the **method area** (HotSpot **Metaspace**), not as a Java object on `-Xmx` — [[How would you explain the Java stack and heap]], [[What JVM runtime memory regions exist]].

## Heap for instances; frames for pointers

JVMS: the heap is the run-time data area from which memory for **all class instances and arrays** is allocated. It is shared among threads, may grow and shrink, need not be contiguous, and is reclaimed by a **garbage collector**. Exhaustion: `OutOfMemoryError`. Size: `-Xms` / `-Xmx`.

`new` / `newarray` / `anewarray` / `multianewarray` obtain that storage, then constructors run. G1 still uses the **same heap**: Eden for ordinary objects, **humongous** objects as contiguous **old** regions — still Java heap, not Metaspace or a native stack.

A **frame** stores locals and an operand stack of **values** (`int`, `reference`, …). The `reference` names a heap object. Primitive **fields** sit **inside** the instance on the heap — [[How does object memory allocation work]], [[What JVM runtime memory regions exist]].

```java
public final class WhereObjectsLive {
    static String kept; // the *variable* is class data; the String is a heap object

    public static void main(String[] args) {
        byte[] buf = new byte[16];
        kept = new String("x");
        System.out.println(buf.length + kept.length());
    }
}
```

**Listing 1.** `buf` and `kept` in `main` are **references** in the current **frame**. The `byte[]` and `String` **instances** (and the string’s payload array) are on the **heap**.

```d2
direction: down
frame: "Frame: locals / operand stack\n(references, primitives)" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
heap: "Java heap: class instances and arrays" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
meta: "Method area / Metaspace\n(class metadata, not instances)" {
  width: 320
  height: 55
  style.fill: "#fff8e1"
}
frame -> heap: "reference"
```

**Fig. 1.** “Where is the object?” → heap. “Where is the variable that names it?” → frame, instance field, or class variable.

> [!warning] The stack does not hold the object
> Saying “local objects live on the stack” confuses the **reference** with the **instance**. Escape analysis may **scalar-replace** some allocations so no heap object appears; that is an optimization. The spec allocation site is still the **heap**.

> [!warning] Not every byte of a Java object is `-Xmx`
> The instance is on the heap. **Direct** buffers and other native memory are **off-heap**; the `ByteBuffer` **object** that owns them is still a heap instance. Classes themselves are **method-area** data — [[What is off-heap memory in the JVM]], [[What is Metaspace and how does it differ from PermGen]].

> [!tip] Interview answer
> Java objects — class instances and arrays — live on the shared heap, sized with -Xmx and reclaimed by GC. Stack frames hold references and primitives, not the objects. Class metadata is the method area, not another place to put `new` results.
