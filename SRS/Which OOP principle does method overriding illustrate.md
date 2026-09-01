<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Polymorphism #SRS

# Which OOP principle does method overriding illustrate?

> [!abstract] Short answer
> **Polymorphism** — specifically **subtype / run-time** polymorphism. An **instance** method in a subclass **overrides** a supertype instance method; a call on a **supertype** variable runs the version for the **actual** class. Inheritance **enables** that relationship; overriding is what makes the **same call** mean **different code**. Override: [[How would you explain method overriding in Java]]. Principle: [[What is polymorphism]]. Dispatch: [[What mechanisms implement polymorphism in Java]].

## Same call, receiver’s method

Overriding requires an **instance** method whose signature is override-equivalent to an instance method inherited from a superclass or superinterface. Invocation looks up the method using the **run-time class** of the object, not the compile-time type of the variable ([[How would you explain dynamic runtime polymorphism in Java]]; [[What is polymorphism]]).

That is the OOP slogan “one interface, many implementations” at the call site: `Shape s = new Circle(); s.area();` is legal because of the type, and it runs `Circle.area()` because of overriding.

**Inheritance** supplies the members and the is-a relation ([[What is the difference between inheritance and polymorphism]]). Without an override, a subclass still inherits; the call does not change behavior. **Encapsulation** and **abstraction** are other pillars ([[What are the main oop principles]]); they are not what overriding demonstrates.

**Overloading** is a different compile-time choice of signature. It is not overriding and is not this run-time principle ([[How would you explain Overload vs Override]]).

```d2
direction: down
var: "Shape s = new Circle()" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
call: "s.area()" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
run: "Circle.area()" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
var -> call: "compile-time type Shape"
call -> run: "run-time class Circle"
```

**Fig. 1.** Overriding is polymorphism at the call: the variable’s type checks the name; the object’s class picks the body.

```java
class Shape {
    String kind() {
        return "shape";
    }
}

class Circle extends Shape {
    @Override
    String kind() {
        return "circle";
    }
}

class Demo {
    static String label(Shape s) {
        return s.kind();
    }
}
```

**Listing 1.** `label(new Circle())` returns `"circle"`. The parameter type is `Shape`; the method that runs is `Circle.kind()`. That is overriding as polymorphism.

> [!warning] Static methods do not illustrate this
> A `static` method with the same signature **hides**; the compile-time type chooses it. That is not overriding and not run-time polymorphism ([[Can static methods be overridden in Java]]).

> [!warning] “Inheritance” is a common incomplete answer
> You need a supertype to override, but inheriting `kind()` unchanged is inheritance without this principle. The principle shown is that **the receiver can change which body runs**.

> [!warning] Liskov is a design rule, not the name of the mechanism
> Substituting a subclass should preserve the supertype’s contract. Breaking that is still overriding in the language. Interview one-word answer remains **polymorphism**.

> [!tip] Interview answer
> Method overriding illustrates polymorphism: a subclass instance method replaces a supertype instance method, and calls dispatch on the run-time class. Inheritance is the relationship that makes the method available to override. Overloading and static hiding are compile-time and do not count.
