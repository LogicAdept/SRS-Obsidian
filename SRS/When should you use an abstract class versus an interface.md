<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/Language/Modifiers/Abstract #Java/OOP/Interfaces #SRS

# When should you use an abstract class versus an interface?

> [!abstract] Short answer
> Use an **interface** for the **type you pass around** and for a **capability** unrelated classes can share (`implements` many). Use an **abstract class** when subclasses must share **instance state, a constructor, or protected helpers**—you have only **one** `extends` slot ([[Does Java support multiple inheritance for classes]]). Often **both**: interface as API, abstract class as a skeletal implementation. Differences: [[What is the difference between a Java interface and an abstract class]]. Garbled twin: [[How does abstract class differ from interface in which cases should you use abstract class and in which interf]].

## Decide by state, construction, and how many types

**Interface when:**

- Callers should depend on a **contract**, not a class lineage ([[Which has the highest abstraction level among class abstract class and interface]]).
- Several existing classes, already in different superclasses, must share a method set.
- You need **only** abstract/`default`/`static`/`private` methods, no per-object fields ([[What kinds of methods can a Java interface declare]]; [[How would you explain default interface methods since Java 8]]).
- No constructor is required ([[Can a Java interface declare a constructor]]).

**Abstract class when:**

- You must **construct** shared fields (`super(name)`).
- You want **protected** methods or package-private hooks, not only `public` API.
- Template-method: concrete methods in the parent call `abstract` steps ([[What is the difference between an abstract class with an abstract method and an interface with an abstract method in Java]]).
- There is a true **is-a class** family with shared representation.

**Default methods do not flip the rule.** They add **code** on the interface, not **instance fields**. If you find yourself stuffing mutable state into `default` methods via static maps, you wanted a class.

**JDK-style split.** Publish `List`; offer `AbstractList` for people who extend a class. New code usually implements the interface and composes helpers instead of burning `extends`.

```d2
direction: down
need: "shared fields or ctor?" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
abs: "abstract class" {
  width: 160
  height: 32
  style.fill: "#e3f2fd"
}
iface: "interface" {
  width: 140
  height: 32
  style.fill: "#e8f5e9"
}
need -> abs: "yes"
need -> iface: "no, capability / API"
```

**Fig. 1.** State and construction point to a class. A type others must implement points to an interface. Combining both is normal.

```java
interface Shape {
    int area();
}

abstract class NamedShape implements Shape {
    final String name;

    NamedShape(String name) {
        this.name = name;
    }
}

class Square extends NamedShape {
    final int side;

    Square(String name, int side) {
        super(name);
        this.side = side;
    }

    @Override
    public int area() {
        return side * side;
    }
}
```

**Listing 1.** `Shape` is what `total(Shape[])` should take. `NamedShape` exists only because `name` is constructed once for every named shape. `Circle` could `implements Shape` without extending `NamedShape`.

> [!warning] Do not burn `extends` for two methods
> If you do not need fields or `super(...)`, an interface (maybe with `default`) leaves the superclass free. An abstract class of only public abstract methods is usually an interface that wasted the inheritance slot.

> [!warning] “Interface cannot have implementation” is outdated
> Since Java 8 it can (`default` / `static`). The remaining hard line is **no instance state and no constructor**. That is still why you pick an abstract class.

> [!warning] You can use both on one class
> `class Square extends NamedShape implements Comparable<Square>` is the usual design. The question is not “only one forever”; it is which **role** each type plays.

> [!tip] Interview answer
> Use an interface for the API and for mix-in capabilities; a class can implement many. Use an abstract class when you must share fields, constructors, or protected implementation, knowing you get only one superclass. Default methods do not replace that. Prefer interface plus a skeletal abstract class when both a contract and a reusable implementation exist.
