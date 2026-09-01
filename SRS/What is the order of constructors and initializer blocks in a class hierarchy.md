<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/OOP/Constructors #SRS

# What is the order of constructors and initializer blocks in a class hierarchy?

> [!abstract] Short answer
> **Statics first, once, superclass to subclass:** each class’s `static` field initializers and `static { }` in **textual order** ([[How would you explain static initialization order in Java]]). Then **`new`**: constructors **chain to `Object`**; after **`super(...)` returns**, that class’s **instance field initializers and `{ }`** run, then the **constructor body**. Parent `{ }` → Parent ctor → Child `{ }` → Child ctor. `{ }` vs ctor: [[How would you explain instance initializer blocks versus constructors]]. Both blocks: [[How would you explain static and instance initializer blocks in Java]].

## Class init, then unwind from `Object`

**Class initialization** happens before the first `new`, `static` method, or non-constant `static` field of that class. Superclasses (from `Object` down) initialize first ([[Do Java classes inherit from Object explicitly or implicitly]]). Interfaces with default methods can initialize too. A compile-time constant `static final` can be used without initializing the class.

**Instance creation.** Allocate; default fields to `0`/`null`/`false`. The chosen constructor assigns parameters, then `super(...)` or `this(...)`. `this(...)` **does not** run this class’s instance `{ }` in that constructor; they run on the constructor that calls `super`. After `super` returns: instance initializers in **source order**, then the rest of the constructor ([[What is constructor]]). A missing constructor is `C() { super(); }` ([[How would you explain the default constructor synthesized by the Java compiler]]). Failures: [[How would you explain what happens if in block initialization occurs exceptional situation]]. Static `{ }`: [[How would you explain static initializer blocks in Java]].

```d2
direction: down
st: "P static → C static" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
in: "P { } → P ctor → C { } → C ctor" {
  width: 300
  height: 36
  style.fill: "#e8f5e9"
}
st -> in: "new Child"
```

**Fig. 1.** One class-init of the chain, then per-class `{ }` immediately before that class’s constructor body.

```java
class Log {
    static final java.util.List<String> lines = new java.util.ArrayList<>();
}

class P {
    static {
        Log.lines.add("P static");
    }

    {
        Log.lines.add("P instance");
    }

    P() {
        Log.lines.add("P ctor");
    }
}

class C extends P {
    static {
        Log.lines.add("C static");
    }

    {
        Log.lines.add("C instance");
    }

    C() {
        Log.lines.add("C ctor");
    }
}

class Use {
    static java.util.List<String> go() {
        Log.lines.clear();
        new C();
        return Log.lines;
    }
}
```

**Listing 1.** First `go()`: `P static`, `C static`, `P instance`, `P ctor`, `C instance`, `C ctor`. A later `new C()` repeats only the four instance/ctor strings.

> [!warning] Instance `{ }` are not postponed until `new` returns
> They run when **that class’s** `super(...)` has finished, **before** that class’s constructor statements. Child `{ }` never runs before Parent’s constructor body.

> [!warning] Static **fields** are part of the static sequence
> `static int x = 1; static { … }` is left-to-right with blocks. Accessing `C.f` initializes only the class that **declares** `f` if `f` is inherited as a static field of `P`.

> [!warning] `this()` and a second instance
> Chaining constructors does not double `{ }`. Class initialization does not rerun. `Object` still sits at the top of both chains.

> [!tip] Interview answer
> Superclass static initializers run first, once, then the subclass’s. On `new`, constructors chain up to `Object`; coming down, each class runs its instance initializers and then the rest of its constructor. So parent `{ }` and parent constructor complete before child `{ }` and child constructor. Field initializers belong in those same static or instance sequences.
