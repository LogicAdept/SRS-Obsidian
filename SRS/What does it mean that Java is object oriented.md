<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #SRS

# What does it mean that Java is object oriented?

> [!abstract] Short answer
> Java is specified as a **class-based, object-oriented** language: you declare **classes** (and interfaces); **objects** are class instances (and arrays); **instance methods** run with a current object **`this`**. A class has **one superclass** (except `Object`) and may **implement** many interfaces; a supertype variable can refer to a subtype instance and **dispatch** on the run-time class. It is also **concurrent** and **statically / strongly typed**—those are extra facts, not “OO.” Types: [[How would you explain main concepts OOP class object interface]]. Principles: [[What are the main oop principles]]. Typing: [[How would you explain static typing in Java]]. Paradigms: [[What are the main paradigms programming]].

## Class-based OO, with holes

**Classes and objects.** A class declaration defines a type and an implementation. `new C(...)` allocates an instance. Arrays are objects too. There are **no** instances of an interface type: an interface-typed variable still refers to a **class** instance (or array).

**`this` and instance methods.** Instance methods are invoked **on** an instance; during the call that instance is `this`. That is the OO style the spec calls out. **`static` methods** operate **without** a specific object—they are not instance polymorphism.

**Inheritance and polymorphism.** Each class except `Object` has a single direct superclass ([[Do Java classes inherit from Object explicitly or implicitly]]; [[Does Java support multiple inheritance for classes]]). Unrelated classes can share an interface type. Variables of a class or interface type can refer to subclass / implementing instances, and instance calls use the run-time class ([[What is polymorphism]]). The usual three/four principles: [[What are the three core principles of object oriented programming]].

**Not “everything is an object.”** Primitive types (`int`, `boolean`, …) are not references. `null` is not an object. Operators on primitives are not method calls. Encapsulation can still fail with public fields. Tradeoffs: [[What are the advantages and disadvantages of object oriented programming]].

```d2
direction: down
c: "class C\ntype + implementation" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
o: "instance\nthis, fields" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
i: "interface I\ntype only" {
  width: 180
  height: 40
  style.fill: "#fff8e1"
}
c -> o: "new"
c -> i: "implements"
i -> o: "variable may refer to"
```

**Fig. 1.** Object-oriented here means class-based types, instances, and interface types—not “no primitives.”

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

**Listing 1.** `User` is a class. `new User("a")` is an object. `label` is written against the interface type and dispatches to `User.name`. `int` counts would still be primitives.

> [!warning] Class-based is not Smalltalk and not JavaScript
> Objects do not invent methods at run time. The class (or array class) is fixed at creation. `static` and primitives sit outside instance dispatch.

> [!warning] “Java is OO” does not mean “no `static`, no `int`”
> A program of only `static` methods on one class is legal Java and barely object-oriented. Wrappers (`Integer`) are objects; `int` is not. `null` has no class.

> [!warning] Concurrent and garbage-collected are separate claims
> `synchronized` and GC are in the same intro paragraph as “object-oriented.” Do not bundle them as OOP principles.

> [!tip] Interview answer
> Java is object-oriented in the class-based sense: you define classes, create instances, and instance methods run with `this`. Types relate through one superclass and many interfaces, and instance calls use the run-time class. It is not purely OO: primitives, `static` members, and `null` are not objects. Encapsulation and polymorphism are how you use that model, not extra keywords.
