<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #Java/JVM/Memory/Stack #SRS

# Which memory region holds reference types in Java?

> [!abstract] Short answer
> A **reference type** is a **kind of type** (class, interface, array, type variable) — it is not itself stored in a heap or a stack. **Values** of those types are **references** (pointers, or `null`). The **object** a non-null reference names is a class instance or array on the **Java heap**. The **reference value** lives wherever that **variable** lives: a **frame** local/operand slot, an **instance field** (inside another heap object), or a **class variable** (method-area / Metaspace data) — [[Which memory region holds objects in Java]], [[How would you explain the Java stack and heap]].

## Type versus value versus object

JLS: an **object** is a class instance or an array. **Reference values** are **pointers** to those objects, plus **`null`**. JVMS: heap storage is for **all class instances and arrays**; a local variable can hold a `reference`. Creating an instance allocates heap memory and **pushes a `reference`** onto the operand stack.

So “where do reference types live?” splits:

| What people mix up | Where it actually is |
| --- | --- |
| The **type** `String`, `List<?>`, `int[]` | Compile-time / run-time **type** of a variable or object — not a heap blob |
| The **reference value** (`s`, `this`, array slots of objects) | The **variable**: frame, instance field, static, array component |
| The **referent** (`new Point()`, `new int[3]`) | **Heap** |

`java.lang.ref.SoftReference` and friends are ordinary **heap objects** that wrap another reference. They are not a fifth JVMS run-time area — [[What reference types exist in Java such as strong weak soft and phantom]], [[What JVM runtime memory regions exist]].

```java
public final class ReferenceWhere {
    static String classVar; // reference in class data; String on the heap

    public static void main(String[] args) {
        String local = new String("x"); // local: reference in the frame
        String[] arr = { local };       // array object on the heap; slot holds a reference
        classVar = arr[0];
        System.out.println(local == classVar);
    }
}
```

**Listing 1.** `local` is a `reference` in `main`’s **frame**. `arr` is a heap **array** whose component is another `reference`. Both point at the same `String` **instance** on the heap.

```d2
direction: down
t: "Reference type\n(class / interface / array)" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
v: "Reference value in a variable\n(frame, field, static, array slot)" {
  width: 340
  height: 55
  style.fill: "#e3f2fd"
}
o: "Object (instance or array) on the heap" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
t -> v: "type of the variable"
v -> o: "points to (or null)"
```

**Fig. 1.** Heap holds **objects**. Frames and fields hold **references**. The type is not a third region.

> [!warning] “Reference types live on the heap” is incomplete
> The **instance** does. The **pointer** in a local does **not** — it is in the **frame**. Primitive **fields** of that instance still sit **inside** the heap object. Saying “primitives on the stack, objects on the heap” skips fields, statics, and `null`.

> [!warning] Not `java.lang.ref` and not Metaspace
> Soft/weak/phantom are **reachability** wrappers. Class metadata for type `Point` is the **method area**; a `Point` **instance** is still heap. Mixing those three stories fails the cue.

> [!tip] Interview answer
> Reference types are class, interface, and array types; their values are pointers or null. The objects those pointers name live on the shared heap. The pointers themselves live in whatever variable holds them — a stack frame, a field, or a static — not in a special “reference-type region.”
