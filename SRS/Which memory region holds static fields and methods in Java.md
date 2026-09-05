<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #SRS

# Which memory region holds static fields and methods in Java?

> [!abstract] Short answer
> **Class variables** (`static` fields) and **method bytecode** belong to the **method area**: per-class **field and method data** plus the **code** for methods and constructors. There is **one** incarnation of each class variable, created at **preparation** (defaults) and filled by **initialization**. Objects a static **reference** names still live on the **Java heap**. HotSpot implements that metadata in **Metaspace**, not `-Xmx` — [[What is Metaspace and how does it differ from PermGen]], [[What JVM runtime memory regions exist]].

## One class-level slot; bytecode next to it

JVMS: the **method area** is shared, created at VM start, and holds per-class structures: the **run-time constant pool**, **field and method data**, and **code** for methods and constructors (including `<clinit>` / `<init>`). **Preparation** **creates** the static fields and sets them to default values (`0`, `null`, …) with no Java code. **Initialization** (`<clinit>`) then runs explicit static initializers.

JLS: a `static` field is a **class variable** — exactly **one** incarnation no matter how many instances (including zero). A `static` method is a **class method**: invoked **without** a particular object (`this` / `super` are illegal in that static context).

Access: `getstatic` / `putstatic` for class variables; `invokestatic` for class methods (arguments start at local **0** — there is no `this`). Running the method still allocates a **frame** on that thread’s **JVM stack** — [[How would you explain the JVM stack and stack frames]], [[What is the JVM class constant pool]].

Instance methods use the **same** method-area code copy; they are not stored “inside” each object. Instance **fields** are in the heap instance.

```java
public final class StaticsWhere {
    static int count;
    static byte[] payload = new byte[8];

    static int bump() {
        return ++count;
    }

    public static void main(String[] args) {
        System.out.println(bump() + payload.length);
    }
}
```

**Listing 1.** `count` is one class variable (method-area **field data**). `payload` is a **reference** there; the `byte[8]` **array** is on the **heap**. `bump` and `main` bytecode live with the class; each call still gets a **stack frame**.

```d2
direction: down
ma: "Method area (HotSpot Metaspace)\nclass vars, method data, bytecode, RCP" {
  width: 400
  height: 55
  style.fill: "#fff8e1"
}
heap: "Java heap: objects named by static refs\n(+ java.lang.Class instance)" {
  width: 380
  height: 55
  style.fill: "#e8f5e9"
}
stack: "JVM stack: frames while a static method runs" {
  width: 360
  height: 50
  style.fill: "#e3f2fd"
}
ma -> heap: "reference fields"
ma -> stack: "invoke"
```

**Fig. 1.** Static **does not** mean “on the heap” or “in the object.” It means **one per class**, stored with class metadata. JIT machine code, if any, sits in the **code cache**, still outside `-Xmx`.

> [!warning] Static objects are not in Metaspace
> `static byte[] payload` stores a **pointer** with the class. The array bytes are **heap**. A large static cache can still throw a **heap** `OutOfMemoryError`. Metaspace OOME is **class metadata** (many loaders/classes), not “too many static `String`s” by itself.

> [!warning] Methods are not heap objects
> There is no `new` for a method. Bytecode lives in the **method area**; a call pushes a **frame**. `static` only changes **dispatch** (no receiver). PermGen is gone; do not answer “statics live in PermGen” on a modern JVM — [[Which memory region holds objects in Java]].

> [!tip] Interview answer
> Static fields and method bytecode live in the method area — Metaspace on HotSpot — one slot per class variable, shared code per method. Values of static references are still heap objects. While a static method runs, its locals sit in a stack frame, not in Metaspace.
