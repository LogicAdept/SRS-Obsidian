<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #DataAndState/ValueSemantics #DataAndState/ReferenceSemantics #Java/Language/Primitives #SRS

# Is it true that primitives live on the stack and reference instances live on the heap?

> [!abstract] Short answer
> **No.** That slogan mixes up **type** with **where the variable lives**. Locals and operand-stack slots sit in a JVM **frame**. The heap holds **class instances and arrays** — including their primitive fields and primitive array components. A local `int` is on the stack; `new int[]{1}` puts an `int` on the heap.

## Frames vs objects, not “primitive vs object”

The heap is the run-time area from which memory for **all class instances and arrays** is allocated. An instance variable is created as part of the object; an array component is created as part of the array ([[Can primitive values reside on the Java heap]]). Those slots can be `int` or `boolean`. Arrays themselves are objects ([[Is a Java array a primitive or an object]]).

A method’s locals, parameters, and operand stack live in a **frame** on that thread’s Java Virtual Machine stack. A local `int n` is there. A local `Point p` is also there: the frame stores the **reference**. The `Point` instance (and its fields) is on the heap. Copying `p` copies the pointer ([[How would you explain Java data types primitives and references]]).

**Class variables** (`static` fields) are per-class data in the method area, which is logically part of the heap; the spec does not pin a physical location. They are not stack locals.

So:

| Variable | Typical home |
| --- | --- |
| Local / parameter primitive | Frame |
| Local / parameter reference | Frame (the pointer) |
| Instance field (any type) | Heap object |
| Array component (any type) | Heap array |
| `static` field | Method area / class data |

```d2
direction: down
myth: "primitives → stack\nobjects → heap" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
real: "locals → frame\ninstances/arrays → heap" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

myth -> real: "replace with"
```

**Fig. 1.** Storage follows the *variable*, not the primitive-vs-reference slogan.

```java
public final class StackHeapSlogan {
    int field;                     // primitive on the heap object

    public static void main(String[] args) {
        int local = 1;             // primitive in the frame
        StackHeapSlogan p = new StackHeapSlogan();
        p.field = local;           // copy of 1 now in the heap object
        int[] cells = { 2 };       // array object; 2 is a heap component
        Integer boxed = Integer.valueOf(3); // wrapper object on the heap

        System.out.println(local);
        System.out.println(p.field);
        System.out.println(cells[0]);
        System.out.println(boxed);
    }
}
```

**Listing 1.** `local` is a frame slot. `field` and `cells[0]` are primitive values in heap objects. `p` in the frame is only a reference.

> [!warning] A local reference is not “the object on the stack”
> `Point p` in a method stores a pointer in the frame. The instance is on the heap. Boxing and array creation still produce heap objects; they do not turn the primitive type into an object. `static int` is not a stack local.

> [!tip] Interview answer
> **False as a universal rule.** Locals live in stack frames — both `int` and object references. Instances and arrays live on the heap, and they carry primitive fields and `int[]` cells with them. The slogan is a rough picture of *locals vs objects*, not of primitive vs reference types.
