<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Inheritance #SRS

# How would you explain class inheritance in Java and tradeoffs?

> [!abstract] Short answer
> A class **`extends` at most one** superclass. The subclass is a **subtype** of that class and **derives its implementation** from it: non-`private` members are inherited, constructors **chain** with `super(...)`, instance methods are **virtual**. That is powerful for a true **is-a** hierarchy with shared state. The costs: you spend the **only** superclass slot, you inherit **coupling** to concrete superclass methods, and overrides run even **during construction**. Use **`final` / `sealed`** when the hierarchy models **kinds**, not reuse. Extra capabilities belong on **interfaces**. What inheritance is: [[What is inheritance]]. One superclass: [[Does Java support multiple inheritance for classes]]. `Object`: [[Do Java classes inherit from Object explicitly or implicitly]].

## Implementation along a single class line

The `extends` clause names the **direct superclass type** (implicitly `Object` if omitted, except `Object` itself). The superclass relation is **transitive**. A `final` class cannot be extended; a `sealed` class lists permitted direct subclasses. The JLS contrast: `sealed` is for **domain kinds**, not as a general **code-reuse** mechanism. Sealed: [[How would you explain Sealed classes]].

**Inherited.** Members of the superclass except `private` ones (and package-access ones from another package). Constructors, static initializers, and instance initializers are **not** members and are **not** inherited; the subclass still **runs** a superclass constructor. Overriding: [[How would you explain method overriding in Java]]. `super.m()`: [[How do you call superclass methods from a subclass in Java]].

**Not inherited as a second class parent.** Multiple class inheritance is illegal. Multiple **types** go through `implements` ([[How does Java model multiple inheritance with interfaces]], [[Why does Java disallow multiple class inheritance]]). Abstract vs interface: [[How does abstract class differ from interface in which cases should you use abstract class and in which interf]].

**Tradeoffs (language consequences)**

- **Scarce `extends`.** One parent class. Using it for “I needed a bit of `Point`’s code” means you cannot later `extend` a real domain parent.
- **Wide inheritance.** You get every accessible method and field, not a menu. Unwanted API and invariants come along.
- **Virtual `this`.** `Point.move` calling `clearIfOut()` hits the **subclass** override. Same rule **while the subclass constructor has not finished**: uninitialized subclass fields are visible. Superclass constructors that call overridable methods are the classic leak.
- **Construction order.** Superclass prologue/`super`, then subclass field initializers, then subclass epilogue. Subclass code cannot assume its own fields are set until after `super(...)` returns.
- **Reuse without subtyping.** A **field** of type `Point` reuses behavior by **delegation**. `HasPoint` is not a `Point`; `instanceof` and substitution do not apply. That is the composition side of the same language: has-a vs is-a.

```d2
direction: down
goal: "need Point's behavior" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
isa: "is-a Point\nextends Point" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
has: "has-a Point\nprivate final Point p" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
cap: "extra role\nimplements Colorable" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
goal -> isa: "subtype + inherited impl"
goal -> has: "reuse, not a subtype"
isa -> cap: "keep extends free for the class"
```

**Fig. 1.** Class inheritance is is-a plus implementation. Composition reuses without subtyping. Interfaces add types.

```java
class Point {
    int x, y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    void move(int dx, int dy) {
        x += dx;
        y += dy;
        clearIfOut(); // virtual — subclass override
    }

    void clearIfOut() {
        if (x < 0) {
            x = 0;
            y = 0;
        }
    }
}

class ColoredPoint extends Point {
    int color;

    ColoredPoint(int x, int y, int color) {
        super(x, y);
        this.color = color;
    }

    @Override
    void clearIfOut() {
        super.clearIfOut();
        color = 0;
    }
}

final class HasPoint {
    private final Point p;

    HasPoint(int x, int y) {
        this.p = new Point(x, y);
    }

    void move(int dx, int dy) {
        p.move(dx, dy);
    }
}
```

**Listing 1.** `ColoredPoint` is-a `Point` and inherits `move`. `HasPoint` reuses `Point` without being one. `clearIfOut` in `move` is dispatched on the run-time class.

> [!warning] Superclass methods that call `this.m()` are subclass methods
> That is how template methods work and how construction surprises happen. Do not invoke overridable instance methods from a constructor if the subclass override reads its own fields. Assign in the constructor **prologue** if you must close that window.

> [!warning] `extends` for reuse alone paints you into a corner
> After `class Worker extends Thread`, you cannot also `extend` `WorkerPool`. `implements Runnable` plus a `Thread` **field** keeps the slot. `final` when the type is complete; `sealed` when the kinds are a closed set.

> [!warning] Inheritance is not a copy-paste of source
> Changing a concrete method in the superclass changes every subclass that did not override it. That coupling is the reuse you asked for. If you cannot accept it, do not `extend`.

> [!tip] Interview answer
> Java class inheritance is single: extends names one superclass, the subclass is a subtype, and it inherits implementation except private members, with constructors chained by super. Use it when the subclass truly is-a that class and should share its state and methods. The tradeoffs are the single extends slot, tight coupling to inherited concrete code, and virtual calls including during construction; for extra types use interfaces, and for reuse without subtyping keep a field and delegate.
