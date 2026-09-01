<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #SRS

# What does the static keyword mean in Java?

> [!abstract] Short answer
> **`static` means there is no current instance of the enclosing class.** A **class variable** has one incarnation for the class; a **class method** is invoked without `this`; a **`static` nested type** has no enclosing instance; a **static initializer** runs when the class is **initialized**, not merely loaded. The body of those declarations is a **static context** (`this` / `super` illegal). `import static` brings accessible class members in under their simple names. Methods: [[How would you explain static methods in Java]]. Constructs: [[How would you explain which Java language constructs can be marked static]]. Instance vs class: [[What is the difference between an instance member and a static member in Java]].

## One class, not one object

A `static` field is a class variable: incarnated when the class is initialized, shared by every instance (including zero instances). A non-`static` field is created per `new`. Class variable initializers and static initializers (`static { ... }`) run at class initialization, in textual order, on first active use — loading alone does not run them. A static initializer cannot complete abruptly by `return`, and it cannot complete normally if the compiler can prove it doesn’t.

A `static` method is a class method: no target object as `this`. It may still use instance members of an object it is **passed**. `main` is the usual JVM entry of this kind: [[Why is the main method static in Java]]. Subclass `static` methods **hide**, they do not override: [[Can static method be override or]].

A `static` member class has no immediately enclosing instance. An **inner** class is the opposite: not `static`, so it does have an enclosing instance. Nested interfaces, nested enums, and nested records are implicitly `static`. Constructors **cannot** be `static`: a constructor always runs with respect to the object being built. Interface fields are already `public static final`; an interface may also declare `static` methods, which implementing classes do **not** inherit: [[How would you explain static methods on Java interfaces]].

`import static Type.Name;` (or `Type.*`) imports accessible `static` members so the compilation unit can use the simple name.

```java
class Point {
    int x, y;
    static final Point origin = new Point(0, 0);
    static int created;

    static {
        created = 0;
    }

    Point(int x, int y) {
        this.x = x;
        this.y = y;
        created++;
    }

    static Point originCopy() {
        return origin;
    }

    static class Holder {
        static int n = created;
    }
}
```

**Listing 1.** One `origin` and one `created` for the class. `Holder` is a `static` nested class. The constructor is not `static`.

```java
import static java.lang.Math.max;

class Use {
    static int clip(int n) {
        return max(n, 0);
    }
}
```

**Listing 2.** Single-static-import makes the class method `max` available as a simple name.

```d2
direction: down
kw: "static" {
  width: 120
  height: 36
  style.fill: "#fff8e1"
}
field: "field → one class variable" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
meth: "method → no this" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
nest: "nested type → no enclosing instance" {
  width: 280
  height: 44
  style.fill: "#f3e5f5"
}
init: "static { } → class initialization" {
  width: 280
  height: 44
  style.fill: "#fff8e1"
}
imp: "import static → simple name" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
kw -> field
kw -> meth
kw -> nest
kw -> init
kw -> imp
```

**Fig. 1.** Every use of `static` drops the current instance of the enclosing class. Constructors are the exception that cannot take the keyword.

> [!warning] `static` is not “constant”
> A non-`final` class variable is one **mutable** location. Every instance and every thread reads and writes that same field. `static` only means shared, not frozen.

> [!warning] `p.origin` is still the class variable
> `Point.origin` and `p.origin` are the same incarnation. A `null` qualifier does **not** throw NPE for a `static` field or a **class** `static` method; the expression is evaluated for side effects and discarded. Interface `static` methods cannot be invoked that way.

> [!warning] “At class load” is the wrong moment
> Static initializers and class-variable initializers run when the class is **initialized**, not merely loaded. They run in textual order with those field initializers. There is still no `this`.

> [!tip] Interview answer
> Static means class-level: one field for the class, methods without this, nested types without an enclosing instance, and blocks that run at class initialization. Call them as ClassName.member. It is not a synonym for immutable. Constructors cannot be static because they always construct an object.
