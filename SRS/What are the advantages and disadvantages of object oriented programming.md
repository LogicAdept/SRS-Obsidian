<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #SystemDesign/Tradeoffs #SRS

# What are the advantages and disadvantages of object oriented programming?

> [!abstract] Short answer
> In Java, OOP pays off when you **hide state**, **share contracts** (`implements`), and **dispatch on the run-time class**. It costs you when **`extends` couples** subclasses to a parent’s fields and constructors, when **public mutable fields** leak representation, and when **virtual calls during construction** see half-built objects. Java definition: [[What does it mean that Java is object oriented]]. Trio: [[What are the three core principles of object oriented programming]]. Inheritance cost: [[How would you explain class inheritance in Java and tradeoffs]].

## What the language actually gives you

**Advantages (mechanisms, not slogans).**

- **Encapsulation.** Access modifiers keep fields out of the published API. Callers depend on methods; you can change representation ([[How would you explain encapsulation in object oriented design]]). Contrast public mutable fields ([[How would you explain problems with public mutable fields in Java]]).
- **Subtype polymorphism.** A `Shape` variable can refer to a `Circle`. Instance methods use dynamic lookup ([[What is polymorphism]]). New implementations of an **interface** need not share a superclass ([[Does Java support multiple inheritance for classes]]).
- **Overriding with a contract.** Access, `throws`, and return type are checked ([[How would you explain Overload vs Override]]). `@Override` catches signature drift.
- **Reuse of types.** `List`, `AutoCloseable`, `java.time` types are used through abstractions, not copy-paste of field layouts.

**Disadvantages (the same mechanisms).**

- **Fragile `extends`.** One superclass. Subclasses compile against protected state and constructor order. Changing a parent method or field initializer can break children without a compile error at the call site. Prefer `implements` plus composition when you only needed a capability.
- **Construction vs dispatch.** Instance methods are virtual even before the subclass constructor body runs. Overrides can read unset fields.
- **Identity and aliasing.** Objects are references. Mutable objects in maps, leaked internals, and “same instance” vs `equals` are recurring bugs.
- **Not the whole language.** Primitives, `static` methods, and `static` nested types are not instance polymorphism. Overloading is compile-time, not OOP reuse.
- **Weight.** Deep hierarchies and “a class for every noun” cost indirection without buying a better type.

There is no JLS chapter titled “advantages of OOP.” Answer with **these Java rules**, not a generic bullet list from a methodology slide.

```d2
direction: down
pro: "interface type + private state\nindependent implementations" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
con: "deep extends + protected fields\nparent change breaks children" {
  width: 300
  height: 50
  style.fill: "#ffebee"
}
```

**Fig. 1.** The gain is programming to a type. The loss is coupling through class inheritance and exposed state.

```java
interface Shape {
    int area();
}

class Square implements Shape {
    private final int side;

    Square(int side) {
        this.side = side;
    }

    @Override
    public int area() {
        return side * side;
    }
}

class Use {
    static int total(Shape[] shapes) {
        int n = 0;
        for (Shape s : shapes) {
            n += s.area();
        }
        return n;
    }
}
```

**Listing 1.** Advantage: `total` does not know `Square`. A new `Circle implements Shape` does not change `Use`. The disadvantage appears if `Square` had instead `extends` a fat `AbstractShape` with protected mutable fields.

> [!warning] “OOP is more modular” is not automatic
> A public field, a setter that breaks invariants, or a 15-class `extends` chain is worse than a package of functions. Encapsulation is **access plus discipline**, not the `class` keyword.

> [!warning] Inheritance is not the only reuse
> Copying a parent to get two methods is the expensive kind. An interface plus a private helper (or a `final` class you compose) is usually cheaper. Java forbids multiple class inheritance on purpose.

> [!warning] Interview lists without Java
> “Modeling the real world” and “easy maintenance” are not observable. Say **private fields**, **interface types**, **one `extends`**, **virtual dispatch**, **constructor-time override**.

> [!tip] Interview answer
> Advantages in Java are encapsulation behind access modifiers, interface types, and runtime dispatch so callers depend on contracts. Disadvantages are coupling from class inheritance, virtual methods during construction, and mutable objects leaking through references. Prefer interfaces and composition when you do not need shared state; use `extends` when you truly share a class implementation.
