<!--
reps: 0
priority: 0
-->
#Java/OOP #SRS

# How would you explain main concepts OOP class object interface?

> [!abstract] Short answer
> A **class** is a **type plus an implementation**: fields, methods, constructors, one superclass (except `Object`), any number of superinterfaces. An **object** is a **class instance or an array**; a **reference** points at it, or is **`null`**. An **`interface`** is a **type** a class **`implements`**: a contract of methods (abstract / `default` / `static` / `private`), **no constructor**, **no instances of its own**. A variable of interface type holds a reference to some **class** instance (or array, for `Cloneable`/`Serializable` on arrays). Java OOP: [[What does it mean that Java is object oriented]]. `Object`: [[How would you explain java.lang.Object as the root of the class hierarchy]]. vs abstract class: [[What is the difference between a Java interface and an abstract class]].

## Type, instance, contract type

**Class.** A class declaration **defines the class and how it is implemented**. It is a **reference type**. Members are fields, methods, nested types; constructors **initialize** instances but are **not members** ([[What is constructor]]). Instance fields are per object; `static` fields are per class ([[How would you explain kinds of variables in Java such as local and instance]]). One `extends`; many `implements` ([[Does Java support multiple inheritance for classes]]). `abstract` / `final` / `sealed` control whether you can `new` or subclass.

**Object.** “Object” in the language means **class instance or array**. You create a class instance with `new Point(...)` (or a few implicit cases). Several variables can refer to **one** object. `null` refers to **no** object. There are **no** instances of an interface type: `Drawable d = p` still points at a `Point`.

**Interface.** An interface declaration specifies an **interface type**. A class that `implements` it must provide the instance methods (or inherit a `default`). Fields are `public static final`. No `new Drawable()` unless an **anonymous class** supplies a body. Method kinds: [[What kinds of methods can a Java interface declare]]. No constructor: [[Can a Java interface declare a constructor]].

The dump’s “interface = all public methods of a class” is the class’s **API**, not the `interface` keyword. Public methods of `Point` are still **class** members.

```d2
direction: down
c: "class Point\ntype + implementation" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
o: "objects\nnew Point(...), also arrays" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
i: "interface Drawable\ntype, no instances" {
  width: 240
  height: 45
  style.fill: "#fff8e1"
}
c -> o: "instances of"
c -> i: "implements"
i -> o: "variable may refer to"
```

**Fig. 1.** Classes are instantiated. Interfaces are types implemented by classes. Objects are instances (or arrays).

```java
interface Drawable {
    void draw();
}

class Point implements Drawable {
    int x, y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public void draw() {}
}

class Use {
    static void go() {
        Point p = new Point(1, 2);
        Drawable d = p;
        int[] a = new int[2];
        d.draw();
        a[0] = 1;
    }
}
```

**Listing 1.** `Point` is the class. `p` and `d` refer to one object. `a` is an object that is an array. `Drawable` is only a type here.

> [!warning] `interface` in Java is not “the public methods of a class”
> `Point`’s public API can exist with **no** `interface` declaration. `implements Drawable` is an extra **type** `p` can be passed as. Do not call that API “an interface” in a Java interview unless you mean the keyword.

> [!warning] `new Drawable()` is not an object of the interface
> You cannot instantiate the interface. `new Drawable() { public void draw() {} }` creates an **anonymous class** instance. `null` is not an object.

> [!warning] Object ≠ variable
> `Point p` is a **reference**. Two references can denote the same instance. Assigning `p = q` copies the **pointer**, not the fields. Arrays are objects; `int` is not.

> [!tip] Interview answer
> A class is a type that describes fields, methods, and constructors and can be instantiated. An object is a class instance or an array, reached through a reference (or null). An interface is a type a class implements: a contract without its own instances or constructors. Do not confuse that with the informal idea of a class’s public API.
