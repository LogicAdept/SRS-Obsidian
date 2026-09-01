<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/Language/Modifiers/Static #Java/Language/Modifiers/Final #Java/OOP/Interfaces #SRS

# How would you explain default modifiers for fields and methods inside interfaces?

> [!abstract] Short answer
> **Fields** are implicitly **`public static final`** constants (an initializer is required). **Methods** with no access modifier are implicitly **`public`**. A method that is not `private`, `default`, or `static` is also implicitly **`abstract`** (semicolon body). The keyword **`default`** is a *different* thing: it marks an instance method that **has** a body. Omitted access is **not** package-private. Access levels: [[How do Java access modifiers work]]. `default` methods: [[How would you explain default interface methods since Java 8]]. Interface `static`: [[How do you invoke a static method on a Java interface]].

## What the compiler inserts

An interface is not a class. Every interface is implicitly `abstract`; writing `abstract` on the interface itself is obsolete. Nested interfaces are implicitly `static`.

**Fields.** The only field modifiers are `public`, `static`, and `final` (plus annotations). All three are implied if you write none of them. `private`, `protected`, and package access are not in that set: there are no instance fields and no hidden fields. Each declarator must have an initializer. The initializer is not required to be a constant expression; it runs once when the interface is initialized. The field’s body is a static context (`this` / `super` illegal).

**Methods.** You may declare `public` or `private`. If you omit the access modifier, the method is `public`. `protected` and package access are illegal. A method lacking `private`, `default`, and `static` is implicitly `abstract`. `default` and `static` (and `private`) methods have a block body; you cannot combine `abstract` with `default` or `static`, or `private` with `abstract` or `default`. `private static` is allowed. Redundant `public` on a method is legal but discouraged as style. What an interface may declare: [[What kinds of methods can a Java interface declare]].

Member types declared in an interface are implicitly `public` and `static`.

```java
interface Limits {
    int MAX = 100;                 // public static final

    void check(int n);             // public abstract

    default boolean ok(int n) {    // public default (has a body)
        return n <= MAX;
    }

    static int cap(int n) {        // public static
        return Math.min(n, MAX);
    }

    private static int clamp(int n) {
        return n < 0 ? 0 : cap(n);
    }
}
```

**Listing 1.** Implicit vs explicit: `MAX` and `check` show the old interview answer. `ok`, `cap`, and `clamp` are the methods that are **not** abstract.

```java
interface Broken {
    // int UNSET;                 // illegal: interface field needs an initializer
    // private int hidden = 1;    // illegal: fields are public static final
    // void packageish();         // still public, not package access
    // protected void no();       // illegal
}
```

**Listing 2.** Conceptual. “No modifier” on an interface member never means package-private.

```d2
direction: down
iface: "interface member, no modifiers written" {
  width: 280
  height: 44
  style.fill: "#fff8e1"
}
field: "field → public static final\n(+ initializer)" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
method: "method → public\n(+ abstract unless default/static/private)" {
  width: 320
  height: 52
  style.fill: "#e3f2fd"
}
notPkg: "not package-private" {
  width: 200
  height: 40
  style.fill: "#ffcdd2"
}
iface -> field
iface -> method
iface -> notPkg
```

**Fig. 1.** “Default modifiers” means what is implied. It is not the `default` keyword.

> [!warning] `default` is not “the default modifiers”
> `default void m() { ... }` is a **public instance** method with a body. The interview phrase “default modifiers” means the **implied** `public static final` / `public abstract`. Mixing the two answers fails the question.

> [!warning] “All methods are public abstract” is the pre-`default` slogan
> It is true only for methods that are not `private`, `default`, or `static`. `private` methods exist and are not public. `default` / `static` methods are not abstract and are not “an interface cannot contain implementation.”

> [!tip] Interview answer
> Interface fields are public static final constants and must be initialized. Interface methods are public if you omit the access modifier, and abstract unless you mark them default, static, or private. That omitted modifier is not package-private. Do not confuse those implied modifiers with the default keyword, which gives an instance method a body.
