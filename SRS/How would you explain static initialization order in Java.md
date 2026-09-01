<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/Language/Modifiers/Static #SRS

# How would you explain static initialization order in Java?

> [!abstract] Short answer
> A class initializes **at most once**. Before its own `static` field initializers and `static { }` blocks run **in textual order**, its **superclass** is initialized (up to `Object`), then **superinterfaces that declare default methods**. `static` fields that are **constant variables** get their values first. Using `Sub.field` initializes **only the class that declares** `field`, not `Sub`. Blocks: [[How would you explain static and instance initializer blocks in Java]]. When init runs at all: [[How would you explain static and instance initializer blocks in Java]].

## Superclass, then this class, left to right

**When.** Initialization is not loading. It happens before the first `new`, `static` method call, or use/assignment of a **non-constant** `static` field of that class (plus a few reflective entry points). A compile-time constant `static final` can be read **without** initializing the class.

**Order for class C.** Acquire C’s initialization lock. If this thread is **already** initializing C, return (recursive request). If C is already done, return. Then:

1. Assign C’s **constant variable** `static` fields.
2. Recursively initialize the **direct superclass**, then superinterfaces of C that declare at least one **default** method (left-to-right `implements` / `extends`).
3. Run remaining class-variable initializers and `static { }` blocks **as one sequence in source order**.

Interfaces run their field initializers in textual order. Initializing an interface does **not** by itself initialize its superinterfaces. `Object` is first in the class chain ([[Do Java classes inherit from Object explicitly or implicitly]]).

**Not the same as instance order.** Instance `{ }` and field initializers run later, per `new`, after `super(...)` ([[How would you explain instance initializer blocks versus constructors]]). Class variables vs instance: [[How would you explain kinds of variables in Java such as local and instance]].

```d2
direction: down
o: "Object" {
  width: 100
  height: 32
  style.fill: "#eceff1"
}
s: "Super\nstatic fields + static { }" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
c: "Child\ntextual order" {
  width: 180
  height: 45
  style.fill: "#e8f5e9"
}
o -> s
s -> c
```

**Fig. 1.** Superclass static initialization completes before the subclass’s static initializers run.

```java
class Super {
    static int taxi = 1729;

    static {
        taxi = 1730;
    }
}

class Sub extends Super {
    static int x = 1;

    static {
        x = 2;
    }
}

class Use {
    static void go() {
        int a = Sub.taxi;
        int b = Sub.x;
    }
}
```

**Listing 1.** `Sub.taxi` is `Super.taxi`: that read initializes `Super` only, so `Sub`’s `{ }` has not run. `Sub.x` then initializes `Sub` (`x` becomes `2`). `Super` is not initialized twice.

> [!warning] A subclass name in `Sub.foo` does not initialize `Sub`
> Only the class (or interface) that **declares** the `static` field is initialized. A `null` variable of type `One` does not initialize `One`. `new Two()` initializes `Two` and its superclasses, not unused siblings.

> [!warning] Recursion and failure
> If C’s initializer calls back into C, that nested request **does nothing**; fields still at default (`0` / `null`) are visible. If static initialization throws, it is wrapped in `ExceptionInInitializerError` when it is not already an `Error`. The class is then **erroneous**; later use throws `NoClassDefFoundError`.

> [!warning] Forward reference vs default values
> A simple-name **read** of a `static` field declared later in the same class is a compile-time error. Qualified names can still observe `0` before that field’s initializer runs. Constant variables are set **before** superclass initialization of C; other statics wait for step 3.

> [!tip] Interview answer
> Static initialization runs at most once per class: superclass first, then this class’s static field initializers and `static` blocks in source order. Accessing a static field through a subclass name initializes only the declaring class. A compile-time constant does not trigger class initialization, and a failed static initializer poisons the class for the rest of the run.
