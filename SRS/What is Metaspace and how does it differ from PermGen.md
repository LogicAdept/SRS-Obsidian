<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/Versions/8 #SRS

# What is Metaspace and how does it differ from PermGen?

> [!abstract] Short answer
> **Metaspace** is HotSpot’s **native** store for **class metadata** (the VM’s representation of loaded classes). **PermGen** was a **Java-heap generation** that held that metadata **plus interned Strings and class statics**. JDK **8** **removed** PermGen: metadata went **off-heap**; interned Strings and statics moved to the **ordinary Java heap**. Metaspace is **unlimited** unless you set `-XX:MaxMetaspaceSize` — [[What JVM runtime memory regions exist]], [[What is the difference between PermGen space and Metaspace OutOfMemoryError]].

## Native metadata versus a heap generation

**PermGen (pre-8).** Class metadata lived in a **permanent generation** of the **Java heap**, sized with `-XX:MaxPermSize`. That same generation also held **interned Strings** and **class static variables**. Load a class → allocate there; unload the class → collect it with that generation. The pool had to be **tuned**; too small → `OutOfMemoryError` naming PermGen.

**Metaspace (8+).** Class metadata is allocated in **native memory** (`mmap` chunks bound to a **class loader**, not `malloc`). HotSpot **explicitly** allocates and frees it; chunks are recycled or returned to the OS when the loader’s classes unload. **Default cap: none** — limited by available native memory. `-XX:MaxMetaspaceSize` is the analogue of `MaxPermSize`. `-XX:MetaspaceSize` is **not** a max: it is the **initial high-water mark** that can **induce a GC** to unload classes (platform default about **12–20 MB**). Raise it to avoid **early** metadata GCs.

With compressed oops / compressed class pointers, metadata uses **two** native regions: ordinary Metaspace plus **compressed class space** (`-XX:CompressedClassSpaceSize`, default **1 GB** reserved). `MaxMetaspaceSize` applies to the **sum** of **committed** class space and other class metadata.

What did **not** stay in Metaspace: JEP 122 moved **interned Strings** and **class statics** onto the **Java heap**, so `-Xmx` may need a bump after the change. Object **instances** were never PermGen/Metaspace; they stay on the object heap — [[How does object memory allocation work]]. Young/old generations are still **object-heap** pools, not Metaspace — [[What are garbage collector generations]].

```text
java -XX:MaxMetaspaceSize=256m \
  -XX:MetaspaceSize=64m \
  YourApp
```

**Listing 1.** Cap native class metadata (`MaxMetaspaceSize`). `MetaspaceSize` only sets when metadata first **triggers GC**, not the ceiling. Pre-8 `MaxPermSize` is obsolete.

```d2
direction: down
perm: "PermGen (≤ JDK 7)\nheap generation" {
  width: 320
  height: 70
  style.fill: "#ffe0b2"
  p1: "class metadata" { width: 140; height: 36 }
  p2: "interned Strings, statics" { width: 200; height: 36 }
}
split: "JDK 8" {
  width: 120
  height: 36
}
meta: "Metaspace (native)" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
heap: "Java object heap" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
perm -> split
split -> meta: "class metadata"
split -> heap: "Strings, statics"
```

**Fig. 1.** PermGen mixed metadata with heap-resident Strings and statics. Metaspace is native metadata only.

> [!warning] `MetaspaceSize` is not `MaxMetaspaceSize`
> The first is a **GC watermark** (default tens of MB). The second is the **native cap** (off by default = unbounded). A class-loader leak with no max will grow **process RSS**, not `-Xmx`.

> [!warning] Interned strings are not “in Metaspace”
> They **were** in PermGen. After 8 they are **Java-heap** objects. Putting “methods, constants, annotations” all in Metaspace as a slogan mixes **class metadata** with **heap objects** (`String`, static fields).

> [!tip] Interview answer
> PermGen was a sized heap generation for class metadata, interned strings, and statics. From Java 8, metadata lives in native Metaspace with no default max (`MaxMetaspaceSize`), and strings/statics sit on the ordinary heap. Instances were never there; a Metaspace OOME is a metadata/native limit, not “increase `-Xmx`.”
