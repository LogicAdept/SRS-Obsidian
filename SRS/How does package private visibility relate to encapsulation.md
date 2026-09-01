<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/OOP #SRS

# How does package private visibility relate to encapsulation?

> [!abstract] Short answer
> It is encapsulation at **package** scale. Access control exists so users of a **package or class** do not depend on unnecessary implementation details. **Package access** (no `public` / `protected` / `private`) keeps a type or member inside that package: sibling classes may collaborate; other packages cannot name it or inherit it. That is wider than **`private`** (one top-level type) and tighter than **`public`** / **`protected`** (a published or subclass contract). Encapsulation: [[What is encapsulation]]. When to use this level: [[When should you use package private visibility in Java]]. Four levels: [[How do Java access modifiers work]].

## Hide the package’s internals, not only the object’s fields

Data encapsulation is hiding internal state and requiring interaction through methods. Java’s access modifiers are how that hiding is written down. The language default for a class member or constructor, and for a top-level class or interface, is package access: visible throughout the declaring package, nowhere else. There is no `package-private` keyword.

A **package-access type** is not part of the package’s published surface. A **`public` type** may still encapsulate implementation with package-access fields, methods, and nested helpers: other packages use the public methods; they cannot call or override the package-access ones, and a subclass **outside** the package does **not** inherit them.

`private` is stricter and is the usual first choice for a member: the enclosing top-level type body (nested types included). Reach for package access when **separate top-level** types in the same package must share, without making that sharing `public` or `protected`. `protected` is not “package-private plus friends”: it also admits subclasses in **other** packages, which is a wider contract.

```java
package shop;

public class Store {
    private final Inventory stock = new Inventory();

    public int buy(String sku) {
        return stock.take(sku);
    }
}

class Inventory {
    int take(String sku) {
        return sku.isEmpty() ? 0 : 1;
    }
}
```

**Listing 1.** `Store` is the encapsulated API. `Inventory` and `take` are package implementation: same-package code may use them; another package cannot.

```java
package other;

import shop.Store;
// import shop.Inventory; // compile-time error: type is not public

class Client {
    void run() {
        new Store().buy("sku");
        // new Inventory(); // compile-time error
    }
}
```

**Listing 2.** Conceptual (second package). Clients depend on `Store.buy`, not on how stock is stored.

```d2
direction: down
api: "public Store.buy" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
pkg: "package-access Inventory" {
  width: 240
  height: 44
  style.fill: "#fff8e1"
}
priv: "private fields inside a type" {
  width: 240
  height: 44
  style.fill: "#ffcdd2"
}
world: "other packages" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
world -> api: "allowed"
world -> pkg: "forbidden"
api -> pkg: "same package"
pkg -> priv: "even tighter"
```

**Fig. 1.** Package access draws the boundary around the package. `private` draws it around one top-level type.

> [!warning] “Subclass: no” means **other package**
> Same-package subclasses **can** use package-access members. A subclass in **another** package cannot — unlike `protected`. Choosing `protected` “just in case” publishes a subclass API and weakens encapsulation.

> [!warning] `public` fields punch through the package
> A public instance field lets every client depend on representation. Prefer `private` (or package access for same-package helpers) and methods. The keyword `default` is not this access level.

> [!tip] Interview answer
> Package-private visibility is encapsulation for a whole package: types and members with no access modifier are visible to collaborating classes in that package and hidden from every other package. Use it for implementation types sitting beside a public facade, not for a published API. Private is still tighter, and protected is wider because foreign subclasses can see it.
