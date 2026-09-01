<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# What is the difference between `int` and `Integer` in Java?

> [!abstract] Short answer
> `int` is the **32-bit signed primitive**. `Integer` is the **immutable wrapper class** for that value: a heap object with methods, able to be `null`, and usable as a generic type argument. Assignment and arithmetic convert between them by **autoboxing** / **unboxing**. Prefer `int` for numbers; use `Integer` when you need an object (`List<Integer>`, an absent value).

## Primitive value vs wrapper object

| | `int` | `Integer` |
| --- | --- | --- |
| Kind | primitive | reference (`java.lang.Integer`) |
| Size of the value | 32-bit two’s-complement | object on the heap (payload still 32-bit `int`) |
| Field default | `0` | `null` |
| `null` | impossible | allowed |
| Methods | none (`Integer.parseInt`, … live on the class) | instance + static API |
| Generics / collections | `List<int>` is illegal | `List<Integer>` |
| `==` | value | identity (cache makes small values look equal) |

```d2
direction: down
prim: "int n = 10\n32-bit value" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
wrap: "Integer n = 10\nheap object (valueOf)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Same number `10`; different kinds of variable.

```java
int primitiveInt = 10;
Integer objInt = Integer.valueOf(20);
Integer autoBoxed = primitiveInt;   // int → Integer (valueOf)
int unboxed = objInt;               // Integer → int (intValue)

// List<int> bad = new ArrayList<>();        // does not compile
List<Integer> nums = new ArrayList<>();
nums.add(primitiveInt);             // autobox into the collection
```

**Listing 1.** Conceptual: boxing at assignment and at `List.add`.

Field defaults follow the kind: an `int` field is `0`; an `Integer` field is `null` ([[What default values do wrapper-typed fields receive in Java]], [[Why cannot a Java primitive variable be null]]). **Locals of either type have no default** — an uninitialized local `Integer` does not print as `null`; it does not compile.

Unboxing `null` (`int x = objInt` when `objInt` is `null`) throws `NullPointerException`. `Integer` is immutable: `n++` boxes a new value into the variable ([[Are Java wrapper types immutable]], [[What happens when you increment an Integer with plus plus in Java]]).

The object costs more memory than four bytes ([[How much memory does an Integer object use compared with int]]) and `+=` / `++` in a loop boxes every trip. Arithmetic belongs on `int` (or `long`).

> [!warning] `List<int>` is not a thing
> Type arguments are reference types. You write `List<Integer>` and let autoboxing insert `valueOf`. That is why wrappers exist for collections — not because `int` lacks 32 bits ([[What are the wrapper types for Java primitives]], [[How does adding an int to an ArrayList of Integer autobox]]).

> [!tip] Interview answer
> **`int` is the primitive 32-bit number; `Integer` is the object that wraps it.** Fields default to `0` vs `null`; only `Integer` can be absent and only `Integer` can be a type argument. Boxing converts either way; unboxing `null` throws. Use `int` unless you need an object.
