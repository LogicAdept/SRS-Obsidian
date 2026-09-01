<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# Can wrapping a primitive let a Java method change the caller value?

> [!abstract] Short answer
> **No.** Boxing an `int` into an `Integer` (or any other boxing wrapper) does not give the method an out-parameter. Java still copies the argument into a new parameter variable: a copy of the primitive bits, or a copy of the wrapper reference. Reassigning that parameter cannot retarget the caller’s variable, and the boxing wrappers are immutable, so there is no wrapped field to write through the copied reference.

## Pass-by-value still applies after boxing

When a method is invoked, the argument values initialize **newly created** parameter variables of the declared types. Those variables are not aliases of the caller’s locals.

A primitive parameter therefore receives a copy of the numeric value. Assigning to the parameter is lost when the method returns — the caller’s variable is unchanged.

A wrapper parameter receives a copy of a **reference**. Boxing conversion (`int` → `Integer`, and the other seven primitive-to-wrapper pairs) may allocate or cache a wrapper object, but the value stored in the parameter is still only that reference. Pointing the parameter at a different `Integer` does not rebind the caller’s variable, for the same reason that assigning `circle = new Circle(0, 0)` inside a method does not replace the caller’s `Circle` variable. See [[What does pass by value mean for Java parameters]].

```d2
direction: down
caller: "Caller\nint x = 3\nInteger w = valueOf(3)" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
copy: "New parameter variable\nint n  /  Integer n" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
obj: "Integer instance\nprivate final int value = 3" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
rebind: "n = valueOf(4)\nor n++" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}

caller -> copy: "copy bits or copy reference"
copy -> obj: "wrapper parameter points here"
copy -> rebind: "only the copy is rebound"
obj -> obj: "value stays 3"
```

**Fig. 1.** Boxing does not share the caller’s variable. The method owns a new slot; the wrapper object has no writable payload.

```java
static void bumpPrimitive(int n) {
    n = n + 1;
}

static void bumpWrapper(Integer n) {
    n = Integer.valueOf(n.intValue() + 1);
}

int x = 1;
bumpPrimitive(x);                 // x is still 1

Integer w = Integer.valueOf(1);
bumpWrapper(w);                   // w.intValue() is still 1

int y = 1;
bumpWrapper(y);                   // autoboxes a copy; y is still 1
```

**Listing 1.** Conceptual call-site demo: neither a primitive copy nor a boxed copy updates the caller’s variable.

## Why a copied `Integer` still cannot be mutated

`Integer` wraps a single `int`. It is a value-based class: `final`, with only `final` instance fields, and no API that mutates the payload after construction. OpenJDK stores that payload as `private final int value` and exposes readers such as `intValue()`, not a setter. The same design holds for `Boolean`, `Byte`, `Character`, `Short`, `Long`, `Float`, and `Double`. Changing a “value” means naming a different wrapper object, which is exactly what [[Are Java wrapper types immutable]] already covers.

So even the *other* half of pass-by-value — “you may mutate the object the copied reference points at, if it has accessible mutable state” — does not apply to boxing wrappers. There is no `setInt` to call.

`n++` on an `Integer` parameter is legal only because the language unboxes, adds one, and boxes the result back into **that parameter**. The original instance is left alone; the caller’s variable still names it. That expansion is the same story as [[What happens when you increment an Integer with plus plus in Java]].

```java
static void bumpPlusPlus(Integer n) {
    n++; // unbox, add, box; rebinds local n only
}
```

**Listing 2.** Conceptual: postfix `++` on a wrapper parameter is reassignment of the copy, not in-place mutation.

## What actually lets the caller observe a new number

Return the new primitive or wrapper and assign it at the call site (`x = bump(x)`).

If you truly need an out-parameter, pass a **mutable** object whose fields (or array components) the method can write. Arrays are reference types; assigning `cell[0] = …` changes the same array the caller still holds. That works because the *array* is mutable, not because a primitive was boxed.

```java
static void bumpCell(int[] cell) {
    cell[0] = cell[0] + 1;
}

int[] cell = { 1 };
bumpCell(cell); // cell[0] is 2
```

**Listing 3.** Conceptual: a mutable holder can share updates; `Integer` cannot.

> [!warning] Boxing is not an out-parameter
> Wrappers exist so a primitive can be treated as an object (collections, generics, `null`), not so a method can overwrite the caller’s local. Java has no by-reference parameter mode, and `Integer` has no setter. Autoboxing an `int` argument into `Integer n` still copies a reference to an immutable object.

> [!warning] Do not confuse holders with boxing wrappers
> A one-element `int[]`, a small mutable class with an `int` field, or `AtomicInteger` can expose updates to the caller because those objects are mutable. They are not the eight boxing wrappers. If the method only reassigns its parameter (`n = …`), even a mutable object’s *identity* in the caller is unchanged.

> [!tip] Interview answer
> **No — wrapping does not let a method overwrite the caller’s primitive.** Java copies every argument into a new parameter variable, so reassigning `Integer n` cannot retarget the caller’s variable. The boxing wrappers are immutable, so you also cannot write a new `int` into the object that reference points at. Return the new value, or pass a mutable holder if you need an out-parameter.
