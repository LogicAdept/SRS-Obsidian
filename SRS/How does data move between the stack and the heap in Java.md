<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #Java/JVM/Memory/Stack #SRS

# How does data move between the stack and the heap in Java?

> [!abstract] Short answer
> Strictly, nothing *moves* — values are **copied**. A variable or a parameter in a frame holds either a primitive value or a **reference** (JLS 4.3.1: references are pointers to objects). Assigning a variable or passing an argument copies that value: primitives are copied by content, references by pointer. The object itself stays on the heap the whole time; the frame only ever holds the pointer. On `return`, the result is pushed onto the **caller's** operand stack — again a copy — [[How would you explain the JVM stack and stack frames]], [[How would you explain the Java stack and heap]].

## Copy semantics, not transfer semantics

When `make()` returns a `Box`, the heap object is *not* handed over. The called frame's return value is pushed onto the caller's operand stack; the caller's local then points at the same heap instance. Two locals can point at one object, and changes through one are visible through the other — there is exactly one instance, with two copied pointers.

```java
final class Move {
    record Box(int n) {}

    static Box make() {
        Box b = new Box(1);   // object on the heap, b in this frame
        return b;             // the reference value is copied to the caller
    }

    public static void main(String[] args) {
        Box a = make();       // 'a' in main's frame points at the same Box
        Box c = a;            // copy of the pointer; still one object
        System.out.println(a == c);
    }
}
```

**Listing 1.** `make` and `main` both hold a copied reference to the *same* heap instance. The object never crosses frames; only the 4- or 8-byte pointer value does.

```d2
direction: right
caller: "caller frame" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
  a: "local a = ptr" {
    width: 150
    height: 40
  }
}
callee: "callee frame" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
  b: "local b = ptr" {
    width: 150
    height: 40
  }
}
heap: "heap" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
  box: "Box(1)" {
    width: 130
    height: 36
  }
}
callee.b -> heap.box: "reference"
caller.a -> heap.box: "returned copy"
```

**Fig. 1.** Two frames, one heap object. The "return" copies the pointer into the caller's operand stack; the instance never moves.

> [!warning] "Primitives live on the stack, objects on the heap" is a lie
> A primitive **field** of an object lives in the heap, inside that object; only **locals** live in the frame. Whether a local primitive or reference ends up somewhere else entirely (registers, eliminated allocation) is the JIT's business — [[Is it true that primitives live on the stack and reference instances live on the heap]]. Escape analysis can also keep a small non-escaping object **off the heap entirely** by scalar-replacing its fields — [[How would you explain Escape analysis]].

> [!tip] Interview answer
> Nothing physically moves between stack and heap: assignment and parameter passing **copy values**. Locals and parameters live in the frame; a reference local is a pointer copied into the frame, while the object it points to stays on the shared heap. Return copies the result into the caller's operand stack, so two variables can point at one instance. And the JIT may eliminate the heap object altogether when it does not escape.
