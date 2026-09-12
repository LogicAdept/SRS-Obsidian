<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #Java/Language/Modifiers/Abstract #SRS

# What is abstraction?

> [!abstract] Short answer
> **Abstraction** is keeping the **essential operations and type** and omitting **how** they are stored or computed. In Java you program to a **supertype**—an **interface** or **`abstract` class**—and call methods; the run-time class supplies the body ([[What is polymorphism]]). That is not the same as encapsulation (hiding fields) ([[What is encapsulation]]; [[How would you explain encapsulation in object oriented design]]). vs encapsulation: [[What is the difference between abstraction and encapsulation]]. vs polymorphism: [[What is the difference between abstraction and polymorphism]]. Ranking of types: [[Which has the highest abstraction level among class abstract class and interface]]. Principles: [[What are the main oop principles]].

## Essential type, omitted details

The dump’s driver picture is the idea: you use **steering and pedals**, not paint chemistry. In code, callers depend on `Shape.area()`, not on whether the shape stores `side` or `radius`.

**Java tools (not a keyword `abstraction`).**

- **Interface:** a type with no instances of its own. Highest usual abstraction ([[What is the difference between a Java interface and an abstract class]]; [[What is the difference between a Java interface and an abstract class]]).
- **`abstract` class / `abstract` method:** a class you cannot `new`; some methods have no body yet. Still a **class**: fields and constructors are allowed.
- **Concrete class:** one implementation of that type.

Abstraction is the **type you publish**. Encapsulation is **what you do not publish** (private fields). You can have an interface (abstraction) whose only implementation leaks public fields (failed encapsulation). Types: [[How would you explain main concepts OOP class object interface]].

The dump’s `Animal` / `Pig` sample is only **`abstract` class + override**. An `interface Shape` with `Square` and `Circle` is the same principle and usually the better API.

```d2
direction: down
t: "abstract type\nShape.area()" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
s: "Square" {
  width: 100
  height: 32
  style.fill: "#e3f2fd"
}
c: "Circle" {
  width: 100
  height: 32
  style.fill: "#fff8e1"
}
t -> s
t -> c
```

**Fig. 1.** Callers see `area`. They do not see `side` or `radius`.

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

**Listing 1.** `Use` is written against `Shape`. Adding `Circle implements Shape` does not change `total`. That is abstraction. `side` staying private is encapsulation.

> [!warning] Abstraction ≠ the `abstract` keyword
> A fully concrete `List` API is still an abstraction. `abstract class` is one way to leave methods unimplemented. Prefer an **interface** for the type you pass around; use an abstract class when implementations share **state**.

> [!warning] Abstraction ≠ encapsulation
> Abstraction chooses **which operations exist**. Encapsulation chooses **what is hidden**. Public fields on a “shape” class give you a type name without an abstraction.

> [!warning] The car metaphor is not a Java rule
> The language does not rank “significant” vs “insignificant” characteristics. You do, by which methods and types you declare.

> [!tip] Interview answer
> Abstraction means depending on a type that names essential operations and hides implementation details. In Java that type is usually an interface or an abstract class, and the concrete class fills in the methods. Do not confuse it with encapsulation, which is access control, or with the `abstract` keyword alone.
