<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/Language/Modifiers/Static #SRS

# Where may static and instance fields be initialized in Java?

> [!abstract] Short answer
> **Class variables (`static` fields):** on the **declaration**, in **`static { }`**, and by later **assignment** (static methods, or even instance `{ }` / constructors if the field is not a blank `static final`). **Instance fields:** on the **declaration**, in **instance `{ }`**, and in **constructors**. A **blank `static final`** is assigned only during **static** initialization. A **blank `final`** instance field must be assigned by the end of **every** constructor. Variables: [[How would you explain kinds of variables in Java such as local and instance]]. Blocks: [[How would you explain static and instance initializer blocks in Java]].

## Two timelines: class init vs `new`

**Static.** `static int s = 1;` and `static { s = 2; }` run once, in textual order, when the class is initialized ([[How would you explain static initializer blocks in Java]]; [[How would you explain static initialization order in Java]]). After that, any code that can see a non-`final` `s` may assign it again—including an instance `{ }` or a constructor. That reassignment is legal and usually a smell: every `new` mutates shared state.

**Blank `static final`.** `static final int C;` has no initializer on the declaration. Only a **static initializer** of this class may assign it. Instance `{ }`, constructors, and methods cannot.

**Instance.** `int n = 2;` and `{ n = 3; }` run after `super(...)`, before the rest of the constructor body, on every `new` ([[How would you explain instance initializer blocks versus constructors]]; [[What is the order of constructors and initializer blocks in a class hierarchy]]). The constructor body may assign again unless the field is `final` and already definitely assigned. Constructors: [[What is constructor]].

**Blank `final` instance field.** Assign it in instance `{ }` and/or in constructors so that **every** constructor completion has assigned it. A constructor that starts with `this(...)` does **not** run this class’s instance `{ }`; that constructor must assign the blank final itself or chain to one that does.

A field or `{ }` initializer may not read, by simple name, a field declared **later** in the same class.

```d2
direction: down
classInit: "class initialization\nstatic field = … and static { }" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
newInit: "each new\ninstance field = …, { }, constructor" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Static initialization is once per class. Instance initialization is once per object. `final` blanks shrink the legal sites.

```java
class Sites {
    static int s = 1;
    static final int C;
    int n = 2;
    final int f;

    static {
        C = 3;
        s = 4;
    }

    {
        n = 5;
        s = 6;
        f = 7;
    }

    Sites() {}
}
```

**Listing 1.** `C` is set only in `static { }`. `s` is set at declaration, in `static { }`, and again in the instance `{ }` on every `new`. `f` is set in `{ }`, so `Sites()` need not assign it. `C = …` in `{ }` would not compile.

> [!warning] Instance `{ }` is not a static-final initializer
> `s = 6` in `{ }` is allowed because `s` is a mutable class variable. `static final int C;` cannot be assigned there. Do not describe “static fields may be initialized in a non-static block” without that `final` caveat.

> [!warning] Locals are not fields
> A local is initialized in its declaration or by definite assignment before use. There are no `static` locals.

> [!warning] `=` on the declaration vs blank `final`
> `static final int C = 1;` is initialized at the declaration (not blank). `static final int C; static { C = 1; }` is the blank form. An instance `final` with `=` on the declaration is not blank; constructors must not assign it again.

> [!tip] Interview answer
> Static fields are initialized at the declaration and in `static { }` during class initialization. Instance fields are initialized at the declaration, in instance `{ }`, and in constructors during `new`. A blank `static final` belongs only to static initializers; a blank instance `final` must be set by construction. Assigning a non-final static from an instance block is legal and usually unwise.
