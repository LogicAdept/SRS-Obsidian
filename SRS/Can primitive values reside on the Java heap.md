<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/Language/Primitives #SRS

# Can primitive values reside on the Java heap?

> [!abstract] Short answer
> **Yes.** The heap holds **class instances and arrays**. A primitive **instance field** is created as part of the object; a primitive **array component** is created as part of the array. Those values sit in heap storage. A local `int` lives in a stack **frame**, not because “primitives cannot be on the heap.”

## Where the variable lives, not “primitive vs object”

The language has eight kinds of variables. The ones that are born with an object are the ones on the heap:

- **Instance variable** — a non-`static` field. A new one is created, with a default, as part of each new object, and it dies with that object.
- **Array component** — unnamed, defaulted when the array object is created. Arrays **are** objects ([[What is the difference between primitive and reference types in Java]]). `new int[10]` allocates one array on the heap whose components are ten `int`s.

The heap is the run-time area from which memory for **all class instances and arrays** is allocated. Garbage collection reclaims that storage. So `new Point()` with `int x, y` puts those `int`s in the heap object; `new byte[1024]` puts 1024 `byte`s in a heap array. [[Is it true that primitives live on the stack and reference instances live on the heap]] is the slogan this fact kills.

Locals, parameters, and the operand stack are in a **frame** on the Java Virtual Machine stack of the current thread. A method-local `int n = 1;` is that kind of variable. Copying it into a field or an array **copies the bits** onto the heap; it does not move the local ([[Can wrapping a primitive let a Java method change the caller value]]). Primitives are still not objects and still cannot be `null` ([[Why cannot a Java primitive variable be null]]).

**Class variables** (`static` fields) are created when the class is prepared. The VM stores per-class field data in the **method area**, which is *logically* part of the heap, though the spec does not mandate its physical location. Do not treat “static `int`” as a stack local, and do not treat it as an instance field either.

```d2
direction: down
heap: "Heap\ninstances and arrays" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
obj: "Point.x, Point.y\nint instance fields" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
arr: "int[] components" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}

heap -> obj
heap -> arr
```

**Fig. 1.** Primitive *values* follow the variable. Instance fields and array components are heap; locals are frames.

```java
public final class PrimitiveOnHeap {
    static int shared;          // class variable (method area / class data)

    int field;                  // instance variable — part of the object

    public static void main(String[] args) {
        int local = 1;          // local variable — frame
        PrimitiveOnHeap p = new PrimitiveOnHeap();
        p.field = local;        // copy of 1 now in the heap object
        int[] cells = new int[] { 2, 3 }; // array object; 2 and 3 are components
        shared = 4;

        System.out.println(p.field);
        System.out.println(cells[0]);
        System.out.println(local);
        System.out.println(shared);
    }
}
```

**Listing 1.** `field` and `cells[0]` are primitive values in heap-allocated objects. `local` is not. `shared` is a class variable.

> [!warning] “Primitives on the stack” is a local-variable slogan
> It is false for `new int[]{ … }` and for every primitive field of an object. Boxing (`Integer.valueOf(1)`) puts a **wrapper object** on the heap that *contains* an `int`; that is not the primitive becoming an object. The heap question is about the **variable** (field, component, local), not about the primitive type itself.

> [!tip] Interview answer
> **Yes — whenever the primitive is an instance field or an array element.** The heap is where instances and arrays are allocated, and those objects carry their primitive slots with them. A local `int` lives in a stack frame. The intern-board line “primitives stack, objects heap” ignores `int[]` and fields.
