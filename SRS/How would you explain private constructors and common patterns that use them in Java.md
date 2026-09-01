<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #Java/Language/Modifiers/Access #SRS

# How would you explain private constructors and common patterns that use them in Java?

> [!abstract] Short answer
> A **`private` constructor** is callable only from code that may use **`private` members of that class** (the nest: the class and its nested types). Declaring **any** constructor suppresses the implicit default one; declaring **all** constructors `private` stops **`new` and subclassing from outside the class**. That is how you write a **utility** type, a **static factory**, a **hand-rolled singleton**, and why **enum** constructors are `private` ([[How does an enum provide a Singleton]]). Constructors in general: [[What is constructor]]. Singleton: [[How would you explain the Singleton design pattern]].

## Who may call `new`

Constructors take `public`, `protected`, `private`, or package access. They are **not** inherited and cannot be `static` / `abstract` / `final`. Access is the same `private` rule as fields: another top-level class cannot call `new C()` if `C()` is `private` ([[Can one object access another class private fields in Java]]). Nested types in the nest **can** ([[How can a nested class access fields of its enclosing class]]).

**Prevent instantiation.** Declare at least one constructor (so no default `public`/`package` constructor appears) and make **every** constructor `private`. Outside the class you cannot `new` it, and you cannot `extends` it (a subclass constructor must invoke an accessible `super(...)`). A `public` class that only wants package-local construction uses package-private constructors instead.

**Patterns that use that knob.**

- **Utility class.** Only `static` members. Private constructor so nobody allocates a dummy instance. Same idea as `Collections` versus the `Collection` interface ([[What is the difference between the Collection interface and the Collections utility class]]).
- **Static factory.** The class calls `new` itself (`of`, `valueOf`, `getInstance`) and chooses instances, caching, or subtypes. Callers never see `new`.
- **Singleton.** One `private` constructor plus a `static` instance (or holder class). Not unique under serialization/reflection; the language’s unique instances are **enum constants** ([[What are the two common singleton implementation patterns]]).
- **Enum.** You must not declare an enum constructor `public` or `protected`; a no-modifier constructor is `private`. `new MyEnum()` is a compile-time error; constants are the only instances.

Interfaces have **no** constructors ([[Can a Java interface declare a constructor]]).

```d2
direction: down
ctor: "private C(...)" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
ok: "same nest\nstatic factory, nested type" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
no: "other top-level class\nnew C() / extends C" {
  width: 260
  height: 45
  style.fill: "#ffebee"
}
ctor -> ok: "allowed"
ctor -> no: "compile-time error"
```

**Fig. 1.** `private` construction is nest-local. That is the whole language rule; factories and singletons are how you use it.

```java
class Utils {
    private Utils() {}

    static int twice(int n) {
        return n * 2;
    }
}

class Box {
    final int n;

    private Box(int n) {
        this.n = n;
    }

    static Box of(int n) {
        return new Box(n);
    }
}

enum Unit {
    INSTANCE
}

class Use {
    static void go() {
        int x = Utils.twice(3);
        Box b = Box.of(1);
        Unit u = Unit.INSTANCE;
    }
}
```

**Listing 1.** `Utils` cannot be constructed from `Use`. `Box.of` is the only way `Use` obtains a `Box`. `Unit` already has a private constructor; `INSTANCE` is the sole value.

> [!warning] A public class with no constructor still has a public default constructor
> If you want “no instances”, you must **write** a `private` constructor. An empty `public final class Utils {}` is instantiable. `final` only blocks subclasses; it does not block `new`.

> [!warning] Nested classes and the class itself can still allocate
> `private` is not “no objects ever”. A static factory, a nested builder, or a test nested in the nest can call `new`. Reflection may also invoke a private constructor if the module allows it; that is why enum uniqueness has extra serialization/`clone` rules.

> [!warning] Hand-rolled singleton ≠ enum
> `private` constructor plus `public static final C INSTANCE = new C();` is a pattern, not a language guarantee of one instance. Prefer an enum when you need a true unique instance ([[How does an enum provide a Singleton]]).

> [!tip] Interview answer
> A private constructor is only usable inside the class nest, so it is the way to forbid `new` and external subclasses. Utility classes declare one empty private constructor so the default public constructor never appears. Static factories and singletons keep `new` inside the class; enum constructors are private by rule and you cannot instantiate the enum yourself.
