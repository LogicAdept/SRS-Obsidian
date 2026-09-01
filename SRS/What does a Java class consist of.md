<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP #SRS

# What does a Java class consist of?

> [!abstract] Short answer
> A **class declaration** has a **header** (name, modifiers, optional type parameters, `extends`, `implements`, `permits`) and a **body**. The body may declare **members**—**fields**, **methods**, **member classes**, **member interfaces**—plus **constructors** and **instance / static initializers**, which are **not members** and are **not inherited**. Members also include what is **inherited** from the superclass and superinterfaces. Constructors: [[What is constructor]]. Nested types: [[How would you explain nested classes in Java and when to use each kind]]. Fields: [[How would you explain kinds of variables in Java such as local and instance]]. Class vs object: [[How would you explain main concepts OOP class object interface]].

## Header, members, and non-members

**Header.** `public` / package / (`protected`/`private` if nested), `abstract`, `final` / `sealed` / `non-sealed`, `static` (nested or local). Normal classes, **enum** classes, and **record** classes are the three declaration kinds. No `extends` means the direct superclass is `Object` (except `Object` itself) ([[Do Java classes inherit from Object explicitly or implicitly]]).

**Members (declared in the body or inherited).** Fields, methods, nested classes, nested interfaces. `private` members are not inherited. Constructors of the parent are never inherited; if you declare none, a **default constructor** is synthesized ([[How would you explain the default constructor synthesized by the Java compiler]]).

**In the body but not members.** Constructors; `{ }` instance initializers; `static { }` ([[How would you explain static and instance initializer blocks in Java]]). Locals inside methods are not class members.

A field and a method may share a name (discouraged). Compact compilation units and anonymous classes still have a class with the same kinds of members.

```d2
direction: down
h: "header\nname, modifiers, extends, implements" {
  width: 320
  height: 45
  style.fill: "#e3f2fd"
}
m: "members\nfields, methods, nested types" {
  width: 300
  height: 45
  style.fill: "#e8f5e9"
}
n: "not members\nconstructors, { }, static { }" {
  width: 300
  height: 45
  style.fill: "#fff8e1"
}
h -> m
h -> n
```

**Fig. 1.** Inherited members come from the superclass and superinterfaces. Constructors and initializers do not.

```java
class Point {
    int x, y;

    static int count;

    static {
        count = 0;
    }

    {
        count++;
    }

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    int sum() {
        return x + y;
    }

    static class Origin {
        static final Point ZERO = new Point(0, 0);
    }
}
```

**Listing 1.** Members: `x`, `y`, `count`, `sum`, `Origin`. Not members: the constructor, `static { }`, `{ }`. `Origin` is a nested class member.

> [!warning] Constructors are not members
> Subclasses do not inherit them. `new Child()` never silently calls a parent’s `Parent(int)` unless `Child` writes `super(int)`. Initializers are not inherited either.

> [!warning] “Consists of fields and methods” is incomplete
> Nested types are members. Inherited public/protected (and package-private same package) members count. Locals and parameters do not.

> [!warning] Enum and record are still classes
> An enum constant is an instance; a record has canonical constructor and accessors. The same member vs constructor split applies, with extra rules.

> [!tip] Interview answer
> A Java class is a declaration with a header and a body. The body holds fields, methods, and nested types—those are members, including inherited ones—and also constructors and initializer blocks, which are not members and are not inherited. If you declare no constructor, the compiler supplies a default one. Locals inside methods are not part of the class.
