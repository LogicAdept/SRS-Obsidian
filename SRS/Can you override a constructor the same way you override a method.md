<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #SRS

# Can you override a constructor the same way you override a method?

> [!abstract] Short answer
> **No.** Constructors are **not members**. They are **never inherited**, so they are not overridden and not hidden. A constructor in a subclass with the same parameter list is a **new** constructor of that class. It **chains** with `this(...)` or `super(...)`; it does not replace the superclass constructor for `new Super(...)`. Constructors: [[What is constructor]]. Versus methods: [[What is the difference between constructors and methods]]. Method override: [[How would you explain method overriding in Java]].

## Not a member; chain, don’t replace

A constructor initializes a **class** instance. It is invoked by `new`, by string conversion that creates a wrapper, or by another constructor. It is **never** invoked by a method call, so there is no `obj.CtorName(...)` dispatch and no `@Override` on a constructor.

The name must be the simple name of the class. There is no return type (`void` included). Unlike methods, a constructor cannot be `abstract`, `static`, `final`, `native`, `strictfp`, or `synchronized`. `final` is unnecessary because nothing inherits it; `abstract` could never be implemented.

A subclass constructor body may call `this(...)` (same class) or `super(...)` (direct superclass). If it writes neither, and the class is not `Object`, the body begins with implicit `super();`. That is initialization order, not override. Default constructor: [[How would you explain the default constructor synthesized by the Java compiler]]. What a constructor is: [[What is constructor]].

```d2
direction: down
sub: "new Sub(n)" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
ctor: "Sub(int) constructor" {
  width: 200
  height: 45
  style.fill: "#fff3e0"
}
sup: "super(n) → Super(int)" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
sub -> ctor
ctor -> sup: "chain"
```

**Fig. 1.** Subclass construction runs the subclass constructor and **then** (via `super`) the superclass constructor. The subclass constructor does not replace the superclass one.

```java
class Super {
    final int n;

    Super(int n) {
        this.n = n;
    }
}

class Sub extends Super {
    final String label;

    Sub(int n) {
        super(n);
        this.label = "sub";
    }

    Sub(int n, String label) {
        super(n);
        this.label = label;
    }
}

class Demo {
    static Super both() {
        Super a = new Super(1);
        Super b = new Sub(2);
        return b;
    }
}
```

**Listing 1.** `Sub(int)` does not override `Super(int)`. `new Super(1)` still runs only `Super`. `new Sub(2)` runs `Sub(int)` which chains to `Super(int)`. Two `Sub` constructors **overload** each other: [[What is constructor overloading in Java]].

```java
// Conceptual: does not compile
class Super {
    Super(int n) {}
}

class Sub extends Super {
    @Override
    Sub(int n) { super(n); }   // @Override is for methods that override

    void Super(int n) {}       // a method, not a constructor
}

class Also extends Super {
    // implicit Also() { super(); } — Super has no no-arg constructor
}
```

**Listing 2.** Conceptual. You cannot annotate a constructor with `@Override`. A method named `Super` is unrelated. If the subclass declares **no** constructor, the implicit default constructor still calls `super()` and fails when the superclass has only `Super(int)`.

Static methods are also not overridden (they hide). That is a different rule: class methods are members; constructors are not members at all: [[Can static methods be overridden in Java]].

> [!warning] Matching parameter lists is not an override
> `Sub(int n)` and `Super(int n)` are two constructors of two classes. `new Super(n)` never runs `Sub`. Forgetting `super(n)` when `Super` has no no-arg constructor is a compile-time error, not “the override failed at runtime.”

> [!warning] Constructors overload; they do not override each other
> Several constructors in **one** class with different parameter lists overload. Overload resolution happens at each `new`. That is the same idea as method overloading, not method overriding.

> [!warning] You cannot “call the constructor as a method” to get polymorphism
> `s.Sub(1)` is not how construction works. Reassigning a `Super` variable to a `Sub` instance does not rerun constructors. Constructors ran when `new` created the object.

> [!tip] Interview answer
> No. Constructors are not members, are not inherited, and cannot be overridden or hidden. A subclass constructor with the same parameters is a new constructor that must chain with super(...) or this(...). You can overload constructors in one class; you cannot replace a superclass constructor for new Super(...).
