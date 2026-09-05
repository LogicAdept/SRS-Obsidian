<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/Bytecode #SRS

# What is the JVM class constant pool?

> [!abstract] Short answer
> Two related tables. The **`class` file `constant_pool`** is a tagged table of **symbolic** information (names, descriptors, numeric/string constants) that bytecodes index instead of using run-time layouts. When the class is **created**, the VM builds a per-class **run-time constant pool** in the **method area**: **static constants** (ready to use) and **symbolic references** (resolved later). A frame only **links** to that pool — [[What JVM runtime memory regions exist]], [[How would you explain the JVM stack and stack frames]].

## Class-file table, then a run-time copy

**`constant_pool` (class file).** Instructions do not depend on how classes or objects are laid out in memory. They name entries in this table. Each entry starts with a **tag** (Utf8, Integer, Class, String, Fieldref, Methodref, InvokeDynamic, … — 17 kinds). Indexes run from **1** to `constant_pool_count - 1` (index **0** is unused). `long` and `double` entries take **two** slots. The 16-bit count caps a class at **65535** entries.

**Run-time constant pool (method area).** Built from that table when the class or interface is **created**. It is a **symbol table**: compile-time numbers and interned **`String` references**, plus symbolic refs to classes, fields, methods, method handles, and dynamic constants/call sites. **Utf8**, **NameAndType**, **Module**, and **Package** structures are used **indirectly** while building it; they do **not** become run-time entries themselves.

Two kinds of run-time entry:

- **Static constants** — no further processing (`int`/`float`/`long`/`double`; a `CONSTANT_String` becomes a reference to an interned `String` instance).
- **Symbolic references** — resolved on use (§5.4.3): class/field/method names become real types and members.

**Loadable** entries can be pushed with `ldc` / `ldc_w` / `ldc2_w`. If constructing the run-time pool needs more **method-area** memory: `OutOfMemoryError`. HotSpot stores that metadata in **Metaspace**, not in `-Xmx` — [[What is Metaspace and how does it differ from PermGen]].

```java
public final class ConstPoolDemo {
    public static void main(String[] args) {
        System.out.println("hello");
    }
}
```

**Listing 1.** The string `"hello"` and the `println` method appear as **constant-pool** entries (`CONSTANT_String` / `CONSTANT_Methodref`). Bytecodes use **indexes**, not heap addresses. `javap -verbose ConstPoolDemo` prints the table.

```d2
direction: down
file: "class file\nconstant_pool (tags, index 1…n)" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
rt: "Run-time constant pool\n(method area)" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
use: "ldc / invoke* / new\nresolve on first use" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
file -> rt: "class creation"
rt -> use: "symbolic refs + static constants"
```

**Fig. 1.** The on-disk table is rewritten into a per-class run-time pool. The JVM stack only holds a **pointer** to that pool, not a copy of every Utf8 string.

> [!warning] The pool is not “the heap string pool”
> A `CONSTANT_String` becomes a **reference** to a `String` **object** (interned). Those objects live on the **Java heap**. The pool entry is metadata in the **method area**. Mixing “string pool” with “constant pool” conflates two structures.

> [!warning] The frame does not contain the pool
> Locals and the operand stack may hold **loadable** values **copied** by `ldc`. The run-time constant pool stays in the **method area**. Overflowing it is a **method-area** / Metaspace failure, not `-Xmx`.

> [!tip] Interview answer
> The class constant pool is the `class` file’s tagged symbol table; at load, the VM builds a run-time constant pool in the method area with literals and symbolic refs that bytecodes index. `ldc` pushes loadable constants; invokes and `new` resolve names later. It is not the Java heap and not the per-thread stack.
