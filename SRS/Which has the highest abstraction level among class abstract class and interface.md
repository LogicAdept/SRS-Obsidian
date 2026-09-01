<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/Language/Modifiers/Abstract #Java/OOP/Interfaces #SRS

# Which has the highest abstraction level among class abstract class and interface?

> [!abstract] Short answer
> **Interface**, then **abstract class**, then a **concrete class** — as a ranking of **how little implementation you lock in**, not as a language “abstraction score.” An interface is a **type**: no instance fields, no constructors, `new I(...)` is illegal. An `abstract` class is an **incomplete class**: it may hold state and constructors, but `new Abstract(...)` is illegal. A normal class can be instantiated (if a constructor is accessible). Abstraction as a principle: [[What is abstraction]]. Type contrast: [[What is the difference between a Java interface and an abstract class]]. When to pick which: [[When should you use an abstract class versus an interface]].

## Commitment, not a keyword ranking

**Interface.** You commit to a **contract** other types `implement`. The body may declare constants, methods, and nested types — not instance state, not constructors ([[Can a Java interface declare a constructor]]). Instance methods there are `abstract`, `default`, `private`, or (implicitly) the `Object` methods the interface redeclares. Several interfaces may be implemented at once. That is the **least** implementation commitment of the three.

**Abstract class.** The class is **incomplete**. It may declare fields, constructors, and mixed concrete / `abstract` methods. Subclasses `extend` it (one class slot) and run those constructors. You still cannot write `new` of the abstract type itself. Use it when shared **state or constructor policy** belongs in the supertype ([[When should you use an abstract class versus an interface]]).

**Concrete class.** Not `abstract`, no leftover `abstract` methods. `new` is allowed if some constructor is accessible. It is still an abstraction of a domain idea; it is the **most** complete of the three **types** in this comparison.

```d2
direction: down
iface: "interface\ntype / contract" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
abs: "abstract class\nincomplete class + optional state" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
cls: "concrete class\ninstantiable" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
iface -> abs: "more implementation"
abs -> cls: "complete enough to new"
```

**Fig. 1.** Usual interview order: interface (highest type-level abstraction), abstract class, concrete class.

```java
interface Named {
    String name();
}

abstract class Animal implements Named {
    private final String name;

    Animal(String name) {
        this.name = name;
    }

    public String name() {
        return name;
    }

    abstract void speak();
}

class Dog extends Animal {
    Dog(String name) {
        super(name);
    }

    void speak() {}
}
```

**Listing 1.** `Named` is only a type. `Animal` adds state and a constructor but stays uninstantiable. `Dog` is the concrete class you `new`.

> [!warning] The language does not assign “abstraction levels”
> There is no keyword rank. A fat interface of `default` methods can contain more code than a thin `abstract` class of `abstract` methods. Rank **commitment** (state, constructors, `new`), not line count ([[What kinds of methods can a Java interface declare]]).

> [!warning] Abstract method on both sides is not a tie
> `abstract void m();` in an abstract class and in an interface looks alike. The **types** still differ: one `extends`, instance fields, constructors, and access on the class side; many `implements` and no instance state on the interface side ([[What is the difference between an abstract class with an abstract method and an interface with an abstract method in Java]]).

> [!warning] Concrete is still an abstraction
> `Dog` abstracts a domain object. “Highest abstraction” here means **the supertype that says the least about how instances are built**, not “classes are not abstract.”

> [!tip] Interview answer
> Interface is the highest of the three as a type: contract only, no instance state, no `new`. Abstract class is next: incomplete class that may already own fields and constructors. A concrete class is instantiable. Pick interface for API and multiple types; pick abstract class when shared state or construction belongs in the parent.
