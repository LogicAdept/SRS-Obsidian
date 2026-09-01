<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Abstract #Java/Versions/8 #Java/Versions/9 #Java/OOP/Interfaces #SRS

# What is the difference between a Java interface and an abstract class?

> [!abstract] Short answer
> An **abstract class** is a **class** you cannot `new`: it may have **instance fields, constructors, and any instance methods**, and a subclass uses **one** `extends`. An **interface** is a **type**: **no constructor**, **no instances of its own**, fields are **`public static final`**, a class may `implements` **many**. Java 8: `default` and `static` methods ([[How would you explain default interface methods since Java 8]]). Java 9: `private` methods ([[Can a Java interface declare private methods]]). When to pick which: [[When should you use an abstract class versus an interface]]. Ranking: [[Which has the highest abstraction level among class abstract class and interface]].

## Class shape vs contract type

**Abstract class.** `abstract` on the class, or forced by an `abstract` method. Incomplete **implementation**: protected state, a constructor that sets it, template methods. Single superclass ([[Does Java support multiple inheritance for classes]]). Methods may be `protected` / package-private. Constructors: yes, but you still cannot `new` the abstract type.

**Interface.** No constructor ([[Can a Java interface declare a constructor]]). No private instance fields ([[Can a Java interface declare private fields or variables]]). Instance methods are `public` abstract, `public default`, or `private`. `static` methods are **not** inherited ([[How do default interface methods differ from static interface methods]]). A variable of interface type still refers to a **class** instance ([[How would you explain main concepts OOP class object interface]]).

| | Abstract class | Interface |
| Superclass slot | A class `extends` **one** class | A class `implements` **many**; an interface `extends` **many** |
| Instance state | Ordinary fields | No instance fields; constants only |
| Construction | Constructors, `this`/`super` | None |
| Method bodies | Concrete instance methods; `abstract` methods force the type `abstract` | `default` / `static` / `private` bodies; implicit `abstract` otherwise |
| Access | `public` / `protected` / package / `private` | Instance API is `public`; `private` helpers since 9 |
| Purpose | Incomplete **implementation** to finish in subclasses | **Contract** (plus default mixin behavior since 8) |

**Both.** Neither is instantiable without a concrete (possibly anonymous) class. Both support polymorphism. A class can `extends` one abstract class **and** `implements` several interfaces. Abstraction ranking: [[Which has the highest abstraction level among class abstract class and interface]]. `implements List` is also is-a; the hard constraint is the **single** `extends` slot and **who owns the fields**.

**Since 8/9.** `default` methods give interfaces inherited **code**, not instance **fields**. Diamond conflicts must be resolved. That does not make an interface an abstract class. Template methods that read `this.x` still want a class.

```d2
direction: down
abs: "abstract class\nfields, ctor, one extends" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}
iface: "interface\nno ctor, many implements" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Abstract class = incomplete class. Interface = extra type (plus default method bodies if you write them).

```java
abstract class Shape {
    final String name;

    Shape(String name) {
        this.name = name;
    }

    abstract int area();
}

interface Named {
    String name();

    default String label() {
        return name();
    }
}

class Square extends Shape implements Named {
    final int side;

    Square(String name, int side) {
        super(name);
        this.side = side;
    }

    @Override
    int area() {
        return side * side;
    }

    @Override
    public String name() {
        return this.name;
    }
}
```

**Listing 1.** `Shape` owns `name` and a constructor. `Named` is a capability. `Square` takes both. `new Shape("x")` and `new Named()` would not compile.

> [!warning] `default` is not instance state
> You still cannot store per-object fields on the interface. Shared mutable state stays in a class. `static` interface methods are `I.m()`, not `this.m()`. Default methods do not replace abstract classes.

> [!warning] Access and fields
> Interface instance methods are `public` (except `private` helpers). An abstract class can hide methods in the package or protect them for subclasses. Interface fields are constants, not `protected int x`. Since Java 8, `static` methods exist; since Java 9, `private` methods exist. Do not describe interfaces as “no implementations” after default methods.

> [!warning] You cannot `new` either incomplete type
> `new Shape("x")` is illegal. `new Named() { public String name() { return "a"; } }` creates an **anonymous class**, not an instance of the interface type itself.

> [!warning] “Abstract class only for is-a; interface never is-a” is slogan, not a rule
> `implements List` is also is-a. Using an abstract class for a mere flag wastes the superclass slot; using an interface when you need `protected int x` will not compile.

> [!tip] Interview answer
> An abstract class is a class with optional fields and constructors and a single-inheritance slot; an interface is a type a class can implement alongside others, without constructors or instance fields. Since Java 8 interfaces may have default and static methods, and since Java 9 private ones, but they still have no object state. Use an abstract class to share implementation and construction; use an interface for the API you pass around.
