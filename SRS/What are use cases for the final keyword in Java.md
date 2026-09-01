<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Final #SRS

# What are use cases for the final keyword in Java?

> [!abstract] Short answer
> Write **`final`** when you want the compiler to **lock** something: a **class** that must not be subclassed, a **method** that must not be overridden (or a **static** method that must not be hidden), a **field or local** that must be assigned **once**, or a **compile-time constant**. The same keyword also **freezes** instance fields at the end of the constructor so other threads can treat an immutable object as fully initialized without extra locks. Meaning of the keyword: [[What does the final keyword mean in Java]]. Locals that need not be written `final`: [[How would you explain effectively final]]. Static methods: [[How would you explain the final modifier on a static method in Java]].

## Why you reach for it

**Lock a type.** A `final` class has no subclasses. That is the usual choice for a small immutable value type: no one can add mutable state or break the contract by extending it.

**Lock a method.** A `final` instance method cannot be overridden. Use it when the implementation is part of the object’s invariant, and especially when a **constructor calls the method**. A constructor that calls a non-`final` instance method lets a subclass override it and run against a half-built object.

**Lock a static method.** `final` on a class method forbids **hiding** in a subclass. That is a narrower, less common use: [[How would you explain the final modifier on a static method in Java]].

**Assign once.** A `final` field is a class or instance variable that each constructor (or initializer) must set and that later code cannot reassign. A **blank** `final` is declared without an initializer so different constructors can pick different values. `static final` primitives and `String`s initialized with a constant expression become **constant variables** (inlined at use sites).

**Publish an immutable object.** After the constructor finishes, another thread that only then sees the object is guaranteed to see the initialized `final` fields (and the objects those fields refer to, as of that freeze). The recipe is: assign the `final` fields in the constructor; do **not** let another thread observe `this` before the constructor returns.

**Document a local.** Writing `final` on a local or parameter states “this name will not be reassigned.” Lambdas and inner classes still require the captured variable to be final or effectively final; you need not write the keyword if the body never assigns it.

```java
final class Point {
    final int x;
    final int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    final int manhattan() {
        return Math.abs(x) + Math.abs(y);
    }
}
```

**Listing 1.** Typical trio: `final` class (no subclass), `final` fields (assign once, freeze at constructor end), `final` method (no override). The class is still only as immutable as the types of `x` and `y`.

```d2
direction: down
why: "Use final to lock..." {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
type: "a class\n(no subclasses)" {
  width: 160
  height: 48
  style.fill: "#e8f5e9"
}
method: "a method\n(no override / hide)" {
  width: 180
  height: 48
  style.fill: "#e3f2fd"
}
once: "a variable\n(assign once)" {
  width: 160
  height: 48
  style.fill: "#f3e5f5"
}
pub: "publication\n(freeze finals)" {
  width: 160
  height: 48
  style.fill: "#fff3e0"
}
why -> type
why -> method
why -> once
why -> pub
```

**Fig. 1.** Four reasons to write `final`: seal a type, seal a method, assign once, and freeze fields for other threads.

> [!warning] A `final` class with mutable fields is not an immutable type
> `final` stops **subclassing** and **reassignment**. A `final` field that holds a `List` still lets callers mutate the list. Immutability is a design, not a single keyword.

> [!warning] Leaking `this` from the constructor cancels the freeze
> If another thread can read the object before the constructor returns, it may see default values for `final` fields. Do not store `this` in a shared structure, start a thread with `this`, or call overridable methods from the constructor.

> [!tip] Interview answer
> Use `final` on a class when it must not be extended, on a method when subclasses must not replace it (especially if a constructor calls it), and on fields when the value is assigned once and other threads should see that value after construction. `static final` constants are a separate, compile-time use. Locals can be `final` for documentation; capture only needs effectively final.
