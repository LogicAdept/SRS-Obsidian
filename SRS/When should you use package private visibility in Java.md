<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/Modifiers/Access #SRS

# When should you use package private visibility in Java?

> [!abstract] Short answer
> Use **package access** (no `public`/`protected`/`private`) when the name should be visible to **other types in the same package** and **not** to the rest of the program — including subclasses in other packages. Typical cases: a **top-level helper class** (the tightest you can make a top-level type), and members that cooperating classes in that package share as implementation. Prefer **`private`** for nested types that only the enclosing class needs. What the level *is*: [[How does package private visibility relate to encapsulation]]. All four levels: [[How do Java access modifiers work]]. Narrower: [[How would you explain private]]. Wider for subclasses: [[How does protected]].

## When it is the right width

**Top-level types.** A top-level class or interface may be `public` or package-private only. If the type is not part of the published API, omit `public`. That is the usual home for package-local helpers, DTOs, and exceptions that other classes in the package throw internally.

**Members of a public type.** Leave a field or method package-private when classes in the **same package** must use it and you do **not** want foreign subclasses to inherit that access. `protected` would leak to those subclasses. `private` would hide it from package peers.

**Package as the unit of collaboration.** Several types designed together can share package-private members without making them `public`. Clients outside the package are forced through the `public` types you actually mean to support.

**Do not use it when a nested type would do.** A `static` nested class or inner class can be `private`. That is tighter than package-private and is the right default if nothing else in the package should see the type.

**Do not treat “default” as a forgotten keyword.** Writing no access modifier is a deliberate package boundary. On **interface** members, omitting the modifier means **`public`**, not package-private: [[How would you explain default modifiers for fields and methods inside interfaces]].

```java
// package com.example.stats
public final class Mean {
    public static double of(double[] xs) {
        return Acc.of(xs).mean();
    }
}

final class Acc {                    // package-private top-level type
    final double sum;
    final int n;
    static Acc of(double[] xs) { /* ... */ return new Acc(0, 0); }
    private Acc(double sum, int n) { this.sum = sum; this.n = n; }
    double mean() { return sum / n; } // package-private method
}
```

**Listing 1.** Callers outside the package see `Mean`. `Acc` and `mean()` stay inside the package. `Acc`’s constructor is `private` because only `Acc` itself should build instances.

```d2
direction: down
q: "Who must see this name?" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
enc: "only enclosing class\n→ private (nested)" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
pkg: "same package only\n→ package-private" {
  width: 220
  height: 48
  style.fill: "#e3f2fd"
}
sub: "package + subclasses\n→ protected" {
  width: 220
  height: 48
  style.fill: "#fff3e0"
}
all: "any client\n→ public" {
  width: 180
  height: 48
  style.fill: "#f3e5f5"
}
q -> enc
q -> pkg
q -> sub
q -> all
```

**Fig. 1.** Choose package-private when the audience is “this package, not the world, not foreign subclasses.”

> [!warning] Package-private is not “almost private”
> Every class in the package can read and assign those members — including later classes you did not have in mind. If only one type should see the name, use `private` (and nest the helper if it is a type).

> [!warning] Subclass in another package is still outside
> `protected` is for “package **or** subclass.” If a subclass in a different package must not touch the member, package-private is the level that **refuses** that subclass. Mixing them up is the usual interview miss.

> [!tip] Interview answer
> Use package-private for implementation that the package shares and the public API must not. Top-level helpers cannot be `private`, so package-private is as tight as they get. Prefer `private` nested types when the enclosing class is the only client. It is narrower than `protected` (no foreign subclasses) and is not what you get by omitting modifiers on interface members.
