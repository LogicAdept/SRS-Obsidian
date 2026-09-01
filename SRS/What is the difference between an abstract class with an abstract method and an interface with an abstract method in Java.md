<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Abstract #Java/OOP/Interfaces #SRS

# What is the difference between an abstract class with an abstract method and an interface with an abstract method in Java?

> [!abstract] Short answer
> The **method** is the same idea: a signature **without a body**; a **concrete** class must **implement** it. The **types** differ. An `abstract` method in a **class** must live in an **`abstract` class** (or enum); it may be `public`, `protected`, or package-private; the class still has **fields, constructors, and one `extends` slot**. An interface method without `default`/`static`/`private` is **implicitly `public abstract`**; you cannot make it `protected`. Full type comparison: [[What is the difference between a Java interface and an abstract class]]. When to use which: [[When should you use an abstract class versus an interface]].

## Same missing body, different home

**Class `abstract` method.** Introduces signature, return type, `throws`; no implementation. The enclosing class must be `abstract` (unless it is an enum). Concrete subclasses must implement it, or stay `abstract`. It cannot be `private`, `static`, `final`, `native`, or `synchronized` ([[Can a method be abstract and static at the same time]]). You may **override** an abstract method with another abstract method (narrow `throws`, covariant return). Access: [[Can you use a weaker access modifier when overriding a method]].

**Interface abstract method.** No `default`, `static`, or `private` → implicitly `abstract`, body `;`. `abstract` and `public` may be written but are redundant. Not `protected`, not package-private. `private` interface methods **have a body** and are not abstract ([[Can a Java interface declare private methods]]). `default` is a different kind ([[How would you explain default interface methods since Java 8]]).

**Why interviewers still ask.** “Both are just abstract methods” ignores **inheritance and state**. Implementing `I` uses **one of many** `implements`. Extending `AbstractA` **consumes** the single superclass ([[Does Java support multiple inheritance for classes]]). The abstract class can still construct shared fields; the interface cannot ([[Can a Java interface declare a constructor]]). A class may do **both**: `extends AbstractA implements I`—then one concrete method can satisfy both abstract `n()` if signatures match and access is at least `public`.

```d2
direction: down
am: "abstract int n();\nin abstract class" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
im: "int n();\nin interface (public abstract)" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
c: "concrete class\nmust implement n()" {
  width: 240
  height: 45
  style.fill: "#fff8e1"
}
am -> c: "extends (one)"
im -> c: "implements (many)"
```

**Fig. 1.** The missing body is alike. The subtype relationship and the rest of the type are not.

```java
abstract class Base {
    abstract int n();
}

interface I {
    int n();
}

class C extends Base implements I {
    @Override
    public int n() {
        return 1;
    }
}
```

**Listing 1.** `Base.n()` could have been package-private; `I.n()` is `public`. `C.n()` must be `public` to implement `I`. `new Base()` and `new I()` do not compile.

> [!warning] `void m();` in an interface is already abstract
> You do not need `abstract`. In a class you **must** write `abstract` and the class must be `abstract`. Forgetting `abstract` on a class method that has no body is a compile-time error (`missing method body`).

> [!warning] Access is not the same
> A package-private abstract method on a class is legal. The same declaration in an interface is `public`. A subclass in another package cannot implement a package-private abstract method by a `public` method from a different package’s view of inheritance—the method would not be inherited. Implementing an interface always requires a **public** method.

> [!warning] An abstract class of only abstract methods is still a class
> It still uses the `extends` slot and can still declare constructors and fields. Prefer an interface if that is all you needed ([[What is the difference between a Java interface and an abstract class]]).

> [!tip] Interview answer
> Both declare a method with no body that a concrete class must implement. In a class that method can have restricted access and sits in an abstract class that may hold state and constructors; you get only one such superclass. In an interface the abstract method is public, there is no constructor, and a class may implement many interfaces. One public method can satisfy both if you extend and implement together.
