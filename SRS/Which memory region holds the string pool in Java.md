<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #Java/String #SRS

# Which memory region holds the string pool in Java?

> [!abstract] Short answer
> There is **no JVMS region** named “string pool.” `String` keeps a private **intern pool** of unique **`String` instances**. Those instances (and their payload arrays) live on the **Java heap** — HotSpot moved interned strings **off the permanent generation** onto the heap (JEP 122). A **native intern table** (`StringTable`) only stores **buckets of references** into that heap. The per-class **run-time constant pool** stores **more references** to the same objects, in the **method area** — [[Which memory region holds strings in Java]], [[What is the JVM class constant pool]].

## A table of heap pointers, not a third heap

`String.intern()`: “A pool of strings, initially empty, is maintained privately by the class `String`.” If an equal string is already pooled, that instance is returned; otherwise **this** object is added. Literals and string-valued constant expressions are interned as if by that method.

Those pooled values **are** `String` objects → they are allocated like any other class instance: the **shared Java heap**. After PermGen removal, interned strings are **not** class metadata and **not** Metaspace; JEP 122 moved interned strings (and class statics) **to the Java heap**, leaving class metadata in native memory. Filling the intern set can therefore contribute to a **heap** `OutOfMemoryError` and to extra GCs; `-Xmx` may need to grow — [[What is Metaspace and how does it differ from PermGen]], [[Which memory region holds objects in Java]].

HotSpot lookup: `-XX:StringTableSize` is the number of **buckets in the interned String table** (rounded up to a power of two). That is a **VM hashtable**, not a place that stores characters. G1 **string deduplication** (`UseStringDeduplication`) is a **different** mechanism: it may share **payload arrays** of equal heap strings; it is **not** the intern pool.

```java
public final class StringPoolWhere {
    public static void main(String[] args) {
        String a = "pool";
        String b = new String("pool");
        String c = b.intern();
        System.out.println(a == c);
        System.out.println(System.identityHashCode(a));
        System.out.println(System.identityHashCode(b));
    }
}
```

**Listing 1.** `a` and `c` are the **same pooled heap instance**. `b` is a **second** heap `String` until `intern()` finds `a`. The pool did not copy characters into Metaspace; it returned a **heap** reference.

```d2
direction: down
table: "Intern table (native StringTable)\nbuckets of oops" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
rcp: "Class run-time constant pool\n(method area): CONSTANT_String refs" {
  width: 340
  height: 55
  style.fill: "#fff8e1"
}
heap: "Java heap: interned String + byte[]" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
table -> heap
rcp -> heap
```

**Fig. 1.** Ask “where is the pool?” → **heap objects**, found through a **native table** and through **constant-pool refs**. Ask “where are the UTF-8 bytes in the `class` file?” → `CONSTANT_Utf8`, used to **build** the interned instance, not a live character store.

> [!warning] The pool is not PermGen, Metaspace, or the constant pool
> PermGen used to hold interned strings; **Metaspace does not**. The **class** constant pool holds **symbolic** `CONSTANT_String` / `Utf8` data, then a **reference** to the interned heap object. Saying “the string pool lives in the constant pool” collapses two structures.

> [!warning] Intern ≠ deduplication
> `intern()` canonicalizes **`String` identity** (`==`). Deduplication may merge **arrays** of strings that are still **distinct objects**. Tuning `StringTableSize` changes **lookup buckets**, not `-Xmx` as a substitute for the heap that stores the strings.

> [!tip] Interview answer
> The string pool is String’s private intern table of unique heap instances, not a JVMS memory region. Since PermGen went away those interned strings live on the Java heap; HotSpot’s StringTable is just native buckets of pointers. The class constant pool only stores references to the same objects.
