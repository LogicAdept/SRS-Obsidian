<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #Java/OOP/Interfaces #SRS

# Can a Java interface declare a constructor?

> [!abstract] Short answer
> **No.** An interface body may declare fields, methods, member classes, and member interfaces — not constructors. A constructor exists to initialize a **class** instance. An interface is implicitly `abstract`, has no instance fields, and cannot be the type instantiated by `new I(...)`. Put construction on implementing classes, or expose a `static` factory method on the interface.

## Class bodies declare constructors; interface bodies do not

A **class** body may declare members **and** instance initializers, static initializers, and constructors. An **interface** body may declare only members: constant fields, methods, and nested types. There is no constructor production in that list, so `I()` or `I(String s)` inside `interface I { ... }` is a compile-time error.

A constructor is used when creating an object that is an instance of a **class**. It is not a member, is never inherited, and is invoked by class instance creation, not by a method call. Constructor vs method: [[What is the difference between constructors and methods]]. What a constructor is: [[What is constructor]].

Interface fields are implicitly `public static final`. There is no instance state on the interface type for a constructor to initialize. Implied modifiers: [[How would you explain default modifiers for fields and methods inside interfaces]].

`new I(...)` without a class body is illegal: the type to instantiate must be a non-`abstract` class. `new AbstractType(...)` is likewise illegal for an abstract **class**, but that class may still declare constructors so a subclass can `super(...)`. Interface vs abstract class: [[What is the difference between a Java interface and an abstract class]].

```d2
direction: down
iface: "interface I { ... }" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
bad: "I() / I(args)\nnot a legal member" {
  width: 220
  height: 55
  style.fill: "#ffcdd2"
}
ok1: "class Impl implements I\nImpl(...) { ... }" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
ok2: "static I of(...)\nmethod, not a constructor" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
ok3: "new I() { ... }\nanonymous class of Object" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
iface -> bad: "illegal"
iface -> ok1
iface -> ok2
iface -> ok3
```

**Fig. 1.** The interface type has no constructor. Construction lives on a class, a `static` factory, or an anonymous class that implements the interface.

```java
interface Named {
    String name();

    static Named of(String n) {
        return new Person(n);
    }
}

class Person implements Named {
    private final String name;

    Person(String name) {
        this.name = name;
    }

    @Override
    public String name() {
        return name;
    }
}

class Demo {
    static void use() {
        Named a = Named.of("a");
        Named b = new Person("b");
    }
}
```

**Listing 1.** Legal construction: a class constructor, plus a `static` factory on the interface. `of` has a return type, so it is a method.

```java
// Conceptual: does not compile — constructor-shaped members
interface Named {
    Named();
    Named(String n);
}
```

**Listing 2.** Conceptual. No return type and the interface name make this constructor syntax. It is not an abstract method (`Named create();` would be).

## Nested types, anonymous classes, and abstract classes

Member classes (and records, enums) declared in an interface are implicitly `public` and `static`. Those **classes** may declare constructors. That constructor belongs to the nested class, not to the enclosing interface.

```java
interface Named {
    String name();

    class Holder {
        final String name;

        Holder(String name) {
            this.name = name;
        }
    }
}

class DemoHolder {
    static Named.Holder h = new Named.Holder("x");
}
```

**Listing 3.** `Holder(String)` is a class constructor. `new Named(...)` is still illegal.

`new Named() { public String name() { return "anon"; } }` does **not** invoke an interface constructor. The expression declares an anonymous **class** that implements `Named` (superclass `Object`) and instantiates that class. The anonymous constructor is implicit; you cannot write one in the class body. Anonymous classes: [[What are anonymous classes and where are they used]].

An abstract class **may** declare constructors even though `new Base(...)` is a compile-time error. Creating a concrete subclass runs that constructor and the abstract class’s instance initializers:

```java
abstract class Base {
    final int n;

    Base(int n) {
        this.n = n;
    }
}

class Impl extends Base {
    Impl() {
        super(1);
    }
}

class DemoBase {
    static Base x = new Impl();
    // Conceptual: new Base(1) does not compile
}
```

**Listing 4.** Uninstantiable as a class is not the same rule as “no constructor.” Interfaces take the stricter cut: no constructor declaration at all.

`default` methods are instance methods with a body. They run on an already constructed implementor, not as construction. `static` interface methods are the usual factory/helper slot: [[How would you explain static methods on Java interfaces]]. Method kinds: [[What kinds of methods can a Java interface declare]].

> [!warning] A constructor inside `interface I { class C { C() {} } }` is not `I`’s constructor
> Nested types in an interface are classes (or other types) of their own. Seeing `(` after a type name in an interface file does not mean the interface declared a constructor.

> [!warning] `new Runnable() { public void run() {} }` is not `new` on the interface
> The object’s runtime class is an anonymous implementor. `Runnable` still has no constructor. `new Runnable()` with no class body does not compile.

> [!warning] “Uninstantiable, therefore no constructor” fails for abstract classes
> Abstract classes are also incomplete and cannot be instantiated with `new`, yet they declare constructors for subclasses. Do not recycle that slogan for interfaces; the grammar simply omits constructors from the interface body.

> [!tip] Interview answer
> No. Interfaces do not declare constructors — only constants, methods, and nested types. There is no instance state on the interface to initialize, and `new I(...)` is illegal unless you supply an anonymous class body, which constructs that class, not the interface. Use a class constructor or a `static` factory method on the interface. Nested classes inside the interface may have constructors; those are not constructors of the interface.
