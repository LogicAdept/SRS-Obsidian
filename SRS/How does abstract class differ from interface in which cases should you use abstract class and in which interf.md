<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Abstract #Java/OOP/Interfaces #SRS

# How does abstract class differ from interface in which cases should you use abstract class and in which interf?

> [!abstract] Short answer
> An **abstract class is an incomplete class**: it may have **instance fields**, **constructors**, `protected` members, and a mix of abstract and concrete instance methods; a class **`extends` at most one** of them. An **interface is a type**: fields are **`public static final`**, there is **no constructor**, methods are `public` `abstract` / `default` / `static` or `private` helpers, and a class may **`implements` many**. Use an **abstract class** when subclasses share **state and construction**. Use an **interface** when you need a **capability** many unrelated classes can mix in without spending the superclass slot. Sibling: [[What is the difference between a Java interface and an abstract class]]. When: [[When should you use an abstract class versus an interface]]. `abstract`: [[How would you explain the abstract keyword in Java]].

## Incomplete class vs type-without-an-instance

Neither can be created with `new Abstract()` / `new Interface()` as a naked type. An abstract class still **has constructors**; instantiating a concrete subclass **runs** those constructors and field initializers. An interface **cannot declare a constructor** ([[Can a Java interface declare a constructor]]).

| | Abstract class | Interface |
| Superclass slot | A class `extends` **one** class ([[Does Java support multiple inheritance for classes]]) | A class `implements` **many**; an interface `extends` **many** |
| Instance state | Ordinary fields | No instance fields; constants only ([[Can a Java interface declare private fields or variables]]) |
| Construction | Constructors, `this`/`super` | None |
| Method bodies | Concrete instance methods; `abstract` methods force the type `abstract` | `default` / `static` / `private` bodies; implicit `abstract` otherwise |
| Access | `public`/`protected`/package/`private` | Instance API is `public`; `private` helpers since 9 ([[Can a Java interface declare private methods]]) |
| Purpose in the language | Incomplete **implementation** to finish in subclasses | **Contract** (plus default mixin behavior since 8) |

Defaults share *behavior* without sharing *fields* ([[How would you explain default interface methods since Java 8]]). Template methods that read `this.x` still want a class.

**Use an abstract class** when the types are a **single hierarchy** that should share mutable (or otherwise instance) state, a constructor protocol, or `protected` hooks — the JLS `Point` / `alert()` pattern: `move` updates fields, subclasses only implement `alert`.

**Use an interface** when the important fact is “can do X”: `Closeable`, `List`, `Paper.show()`. Unrelated classes can implement it. You keep `extends` free for a real superclass. Several capabilities compose with several `implements`.

Prefer **both**: `class Circle extends Shape implements Drawable, Closeable`. The class is-a `Shape` (state); it is-a `Drawable` (role).

```d2
direction: down
need: "shared what?" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
ac: "state + ctor + protected\n→ abstract class" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
it: "capability / many mixins\n→ interface" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
need -> ac
need -> it
```

**Fig. 1.** Shared fields and construction → abstract class. Shared role without a superclass → interface.

```java
abstract class Shape {
    int x, y;

    Shape(int x, int y) {
        this.x = x;
        this.y = y;
    }

    void move(int dx, int dy) {
        x += dx;
        y += dy;
    }

    abstract void draw();
}

interface Drawable {
    void draw();

    default void preview() {
        draw();
    }
}

interface Closeable {
    void close();
}

class Circle extends Shape implements Drawable, Closeable {
    Circle(int x, int y) {
        super(x, y);
    }

    @Override
    public void draw() {}

    @Override
    public void close() {}
}
```

**Listing 1.** `Shape` owns coordinates and `move`. `Drawable` and `Closeable` are extra types; `Circle` keeps one superclass.

> [!warning] “Interface methods are all `public abstract` or `default`” is stale
> Since Java 8, `static` methods exist; since Java 9, `private` methods exist. Fields are still `public static final`. Do not describe interfaces as “no implementations” after default methods.

> [!warning] “Abstract class only for is-a; interface never is-a” is slogan, not a rule
> `implements List` is also is-a. The hard constraint is the **single** `extends` slot and **who owns the fields**. Using an abstract class for a mere flag wastes that slot; using an interface when you need `protected int x` will not compile.

> [!warning] Default methods do not replace abstract classes
> A `default` method has `this` of the interface type but **no instance fields of the interface**. Shared counters, buffers, and constructor invariants still belong on a class.

> [!tip] Interview answer
> An abstract class is a class you cannot instantiate: it can hold instance state, constructors, and mixed abstract and concrete methods, and a type extends only one class. An interface is a type with public constants, no constructor, and abstract, default, static, or private methods; a class may implement many. Use an abstract class to share state and construction in one hierarchy; use an interface for a capability that many unrelated classes should mix in.
