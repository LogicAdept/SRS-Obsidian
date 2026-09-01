<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Polymorphism #SRS

# What mechanisms implement polymorphism in Java?

> [!abstract] Short answer
> Java implements **subtype polymorphism** with three language pieces: **(1)** a **supertype** (`class`/`interface`) so a variable can refer to a **subtype** instance, **(2)** **overriding** instance methods of the same signature, **(3)** **dynamic lookup** of that signature from the **run-time class**. Dispatch: [[How would you explain dynamic runtime polymorphism in Java]]. Override: [[How would you explain method overriding in Java]]. What polymorphism is: [[What is polymorphism]]. Binding: [[What is the difference between static and dynamic binding in Java]].

## Types, override, lookup

**1. Subtyping.** `extends` (one class) and `implements` (many interfaces) ([[What is inheritance]]; [[Does Java support multiple inheritance for classes]]). Assignment and argument passing allow a `Circle` where a `Shape` is declared. Without a shared type, there is nothing to be polymorphic *through*.

**2. Overriding.** A subclass or implementor declares an instance method whose signature is a **subsignature** of the inherited one. `@Override` is a check, not the mechanism. `default` methods are still instance methods and can be overridden ([[How would you explain default interface methods since Java 8]]). `static` methods **hide** ([[Can static methods be overridden in Java]]). `private` / `super` skip lookup.

**3. Dynamic method lookup.** After the compiler has fixed the **signature** (overloads are **not** this mechanism—[[How would you explain method overloading in Java]]; [[How would you explain Overload vs Override]]), a `virtual` or `interface` invocation searches from the target object’s class ([[What is polymorphism]]).

**Not the OOP mechanism.** Overloading (compile-time). Generics (parametric, erased). Casts/`instanceof` (tests). `final` methods can be invoked virtually but cannot supply a second body.

```d2
direction: down
t: "1. Shape s" {
  width: 140
  height: 32
  style.fill: "#e3f2fd"
}
o: "2. Square.area overrides" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
d: "3. lookup from run-time class" {
  width: 260
  height: 36
  style.fill: "#e8f5e9"
}
t -> o
o -> d: "s.area()"
```

**Fig. 1.** Polymorphism in Java is a type, an override, and a lookup—not a keyword `polymorphic`.

```java
interface Shape {
    int area();
}

class Square implements Shape {
    final int side;

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

**Listing 1.** `Shape` is the type. `Square.area` is the override. `s.area()` is the lookup. `total` does not name `Square`.

> [!warning] Overloading does not implement OOP polymorphism
> Extra `total(Square[] )` would be a second signature chosen from the **compile-time** type of the argument. `Shape[]` would still call `total(Shape[])`. You need an instance method on the element.

> [!warning] Inheritance without override is not enough
> If `Square` only inherits a concrete `area` from an abstract class and does not replace it, calls are still virtual, but there is only one body. The **mechanism** is still lookup; the **interesting** case is when subclasses differ.

> [!warning] No `virtual` keyword
> Instance methods are virtual by default. `final` / `private` / `static` are how you **opt out**. There is no `polymorphic` modifier.

> [!tip] Interview answer
> Polymorphism in Java is subtype types, method overriding, and dynamic dispatch. You declare a superclass or interface, implement or override the instance method, and call it on a supertype reference; the JVM uses the run-time class. Overloading and generics are other forms of polymorphism and are not that runtime lookup.
