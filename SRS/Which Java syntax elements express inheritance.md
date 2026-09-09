<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP/Inheritance #SRS

# Which Java syntax elements express inheritance?

> [!abstract] Short answer
> **`extends`** and **`implements`**. A **class** (or enum/record) uses `extends` for **one** superclass and `implements` for **interfaces**. An **interface** uses `extends` for **one or more** superinterfaces — never `implements`. Omitting `extends` on a normal class still inherits **`Object`**. `super(...)` / `super.member` **use** the superclass; they do not declare the relationship. Meaning: [[What is inheritance]]. `Object`: [[Do Java classes inherit from Object explicitly or implicitly]]. Many types: [[How does Java model multiple inheritance with interfaces]].

## `extends`, `implements`, and the implicit superclass

**Class `extends C`.** Names the **direct superclass**. One only. `final` and (unless you are listed) `sealed` types cannot be subclassed. `enum` and `record` must **not** write `extends`; their superclasses are `Enum<E>` and `Record`.

**Class `implements I, J`.** Names **direct superinterfaces**. A class, enum, or record may list many. That is Java’s multiple **type** inheritance ([[Does Java support multiple inheritance for classes]]).

**Interface `extends I, J`.** An interface inherits from other **interfaces** only. There is no `implements` on an interface declaration.

**Omitted `extends`.** A normal class other than `Object` has direct superclass `Object`. Interfaces have no universal superinterface.

**Anonymous class.** `new Shape() { ... }` subclasses `Shape`. `new Drawable() { ... }` implements `Drawable` and subclasses `Object`.

**`super`.** `super(...)` is a **constructor invocation**; constructors are not inherited ([[Can you override a constructor the same way you override a method]]). `super.m()` / `super.f` refer to an accessible superclass member. Neither keyword creates the `extends` edge.

**`sealed` / `permits`.** Restrict **which** types may appear in `extends` / `implements`. They do not replace those clauses.

**is-a vs has-a.** A field is composition, not inheritance syntax ([[What do in OOP expressions is-a and has-a]]).

```d2
direction: down
c: "class Circle extends Shape\nimplements Fillable" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
i: "interface Fillable extends Drawable" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Classes `extend` one class and `implement` interfaces. Interfaces only `extend` interfaces.

```java
interface Drawable {
    void draw();
}

interface Fillable extends Drawable {
    void fill();
}

class Shape {
    void bounds() {}
}

class Circle extends Shape implements Fillable {
    public void draw() {}
    public void fill() {}
}
```

**Listing 1.** `Circle` inherits class members from `Shape` and interface contracts from `Fillable` (and thus `Drawable`). `Fillable extends Drawable` is interface-to-interface inheritance.

> [!warning] Generic `extends` is a bound, not a superclass clause
> `class Box<T extends Shape>` constrains the type argument. It does not make `Box` a subclass of `Shape`. Wildcard `? extends Shape` is the same idea ([[What is the difference between extends and super wildcards in Java generics]]).

> [!warning] `@Override` is not inheritance syntax
> It asks the compiler to check that a method overrides or implements a supertype method. The relationship still comes from `extends` / `implements`.

> [!warning] `import` does not inherit
> `import static` and type imports only affect names in source. They do not add members to a type.

> [!tip] Interview answer
> Inheritance is written with `extends` and `implements`. A class extends one superclass and may implement many interfaces; an interface extends other interfaces. If a normal class omits `extends`, its superclass is `Object`. `super` talks to that superclass; it does not declare it.
