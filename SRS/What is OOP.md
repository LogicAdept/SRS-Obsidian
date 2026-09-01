<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #SRS

# What is OOP?

> [!abstract] Short answer
> **Object-oriented programming** organizes a program as **objects**—**instances of classes**—that **collaborate**. Classes form a **type hierarchy** (`extends` / `implements`). Java is specified as **class-based, object-oriented**: instance methods run with **`this`** ([[What does it mean that Java is object oriented]]). Usual principles: encapsulation, inheritance, polymorphism, often abstraction ([[What are the main oop principles]]; [[What are the three core principles of object oriented programming]]). Class / object / interface: [[How would you explain main concepts OOP class object interface]]. Paradigms: [[What are the main paradigms programming]].

## Objects, classes, hierarchy

The dump’s three bullets are the textbook test:

1. **Objects** are the main building blocks (not only free-standing procedures).
2. Every object is an **instance of a class** (in Java: class instance or array).
3. Classes sit in an **inheritance hierarchy**.

Java meets (3) by construction: every class but `Object` has a superclass ([[What is inheritance]]). Interfaces add extra types. **Is-a** vs **has-a**: [[What do in OOP expressions is-a and has-a]].

**Collaboration.** Textbooks say objects **exchange messages**. In Java that is **method invocation**; instance methods then **dispatch** on the run-time class ([[What is message passing in object oriented programming]]; [[What is polymorphism]]). Encapsulation is **choosing** methods as the API, not a language lock ([[What is encapsulation]]). Public fields and `static` helpers still compile. Abstraction: [[What is abstraction]].

**“Not OOP without inheritance.”** That is one school (ADT vs OO). In Java you always inherit from `Object`. A program of only `static` methods on one class is legal and barely uses the model. Tradeoffs: [[What are the advantages and disadvantages of object oriented programming]].

```d2
direction: down
cls: "class\ntype + implementation" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
obj: "objects\ninstances, this" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
h: "hierarchy\nextends / implements" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
cls -> obj: "new"
cls -> h
```

**Fig. 1.** OOP in Java: classes, instances, a type hierarchy. Methods are how objects are asked to work.

```java
interface Named {
    String name();
}

class User implements Named {
    private final String name;

    User(String name) {
        this.name = name;
    }

    @Override
    public String name() {
        return this.name;
    }
}

class Use {
    static String label(Named n) {
        return n.name();
    }
}
```

**Listing 1.** Objects (`new User`), a class, an interface in the type hierarchy, a message (`name()`). `int` counters would still be primitives—Java is OO, not “everything is an object.”

> [!warning] State is not only changed by messages
> The dump’s “sole way to change state is send a message” is a **discipline**. `p.x = 1`, same-class field writes, and reflection also mutate. Encapsulation is how you **opt in**.

> [!warning] OOP is not a Java keyword
> The language is class-based OO **and** imperative, concurrent, and statically typed. Lambdas/streams are extra style. Saying “Java is OOP” does not forbid `static` or `int`.

> [!warning] Hierarchy is not the same as a deep `extends` chain
> Interface types count. Prefer a shallow class tree plus `implements`. Programming with abstract data types (modules + data, no subtype polymorphism) is a different style, even if you still use the `class` keyword.

> [!tip] Interview answer
> OOP is programming with objects that are instances of classes in a type hierarchy, collaborating through method calls. Java is class-based: `this`, one superclass, many interfaces, virtual dispatch. Encapsulation, inheritance, and polymorphism are the usual principles. It is not “everything is an object,” and fields can still be mutated without a method if you expose them.
