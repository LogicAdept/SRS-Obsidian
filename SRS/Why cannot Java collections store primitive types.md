<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #Java/Collections #SRS

# Why cannot Java collections store primitive types?

> [!abstract] Short answer
> Generic collections are parameterized types. A type argument must be a **reference type**, so `List<int>` does not compile. At run time erasure turns `List<E>` into a list of **object references** (raw `List` / `Object[]` slots). Wrappers fill that hole: `List<Integer>` plus autoboxing (`add(i)` → `add(Integer.valueOf(i))`). Arrays are different: `int[]` is legal.

## Generics take references, not `int`

`Collection<E>`, `List<E>`, `Map<K,V>` are generic. You cannot instantiate a generic type with a primitive (`Pair<int, char>` is the textbook compile error). Substitute `Integer` and `Character`; the compiler boxes the primitive arguments.

Erasure removes the type parameter. A `List<Integer>` is a `List` of references at run time. There is no slot that holds a raw 32-bit `int` inside that structure — only a pointer to an `Integer` (or `null`).

```d2
direction: down
bad: "List<int>\ncompile error" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
ok: "List<Integer>\nreferences + autobox" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
arr: "int[]\nnot a generic collection" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Collections need wrappers; primitive arrays are a separate mechanism.

```java
// List<int> broken = new ArrayList<>();     // does not compile

int i = 3;
List<Integer> list = new ArrayList<>();
list.add(i);                                 // add(Integer.valueOf(i))

int[] ints = { 3, 4, 5 };                    // primitive array — fine
```

**Listing 1.** Conceptual: `List<Integer>` plus boxing vs `int[]` ([[How does adding an int to an ArrayList of Integer autobox]], [[What method does the compiler insert when autoboxing an int]]).

That is a main reason wrappers exist ([[Why are wrapper classes needed in Java]], [[What is the difference between int and Integer in Java]]). `add`/`get` still pay boxing and can NPE on unbox of a `null` element ([[When does autoboxing occur in Java]]).

Pre-generics `Vector.addElement(Object)` had the same object requirement. `addElement(3)` was illegal before autoboxing; `addElement("3")` stored a **string**, not the number three.

> [!warning] `List<int>` is still illegal
> Autoboxing does not create `List<int>`. It only converts an `int` **argument** into an `Integer` when the element type is already `Integer`. You always write `List<Integer>` (or `int[]` when you truly want primitives).

> [!tip] Interview answer
> **Collections are generic: type arguments must be references, and erasure stores objects, not `int` bits.** Use `List<Integer>` and let autoboxing call `valueOf`. `int[]` can hold primitives because arrays are not generics. Wrappers exist largely for this API gap.
