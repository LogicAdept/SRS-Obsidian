<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #SRS

# How do default copy and parameterized constructors differ?

> [!abstract] Short answer
> A **default constructor** is **implicit**: if you declare **none**, the compiler adds a **no-arg** constructor (same access as the class, `super()`, no `throws`). A **parameterized constructor** is one **you write** with a **formal parameter list** — any arity, including a single `Point other`. A **copy constructor** is **not** a Java language form; it is a **parameterized constructor** whose job is to copy state from another instance. Declaring **any** constructor **suppresses** the default. Default: [[How would you explain the default constructor synthesized by the Java compiler]]. Constructors: [[What is constructor]]. Copy as a pattern: [[How would you explain copy constructors or defensive copying in Java]].

## Implicit no-arg vs written signatures vs a copy convention

Constructors are **not members**; they are not inherited or overridden ([[Can you override a constructor the same way you override a method]]). Overloads are distinct signatures in **one** class ([[What is constructor overloading in Java]]). What a constructor *is*: [[What is constructor]].

**Default.** Only when the class contains **no** constructor declarations. For a normal class it has **no** programmer-visible parameters (a non-`private` inner member class still gets a hidden enclosing-instance parameter), **no** `throws`, and a body that is `super()` — empty only for `Object`. Access matches the class (`public` class → `public` default). If the superclass has no accessible no-arg constructor without `throws`, the implicit default is a **compile-time error**. A no-arg constructor **you** write is **not** the default constructor.

**Parameterized.** Any declared constructor whose declarator lists formal parameters (same syntax as a method). Typical use: `Point(int x, int y)`. This is the JLS constructor, not a separate kind. It **replaces** the default: `new Point()` does not compile unless you also declare a no-arg overload.

**Copy.** Java **does not** synthesize a constructor `Point(Point)`. You write `Point(Point other)` (often `this(other.x, other.y)`). It is just another parameterized overload. It copies **what you code**: field assignment is a **shallow** share of mutable objects unless you copy those too.

```d2
direction: down
need: "how is the new object filled?" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
def: "default (implicit)\nno declared ctor → C() { super(); }" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
par: "parameterized (you write)\nC(int x, int y) { ... }" {
  width: 320
  height: 50
  style.fill: "#fff8e1"
}
cpy: "copy (convention)\nC(C other) — still parameterized" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}
need -> def
need -> par
need -> cpy
```

**Fig. 1.** Default is synthesized. Parameterized is declared. Copy is a parameterized constructor with a same-type argument.

```java
class Implicit {
    int x;
    // Implicit.this() { super(); }  — default; x == 0
}

class Point {
    final int x, y;

    Point(int x, int y) { // parameterized — default is gone
        this.x = x;
        this.y = y;
    }

    Point(Point other) { // copy convention; overload
        this(other.x, other.y);
    }
}

class Box {
    final int[] data;

    Box(int[] data) {
        this.data = data; // shares the array
    }

    Box(Box other) {
        this.data = other.data.clone(); // defensive copy of the payload
    }
}
```

**Listing 1.** `Implicit` still has a default constructor. `Point` has parameterized and copy overloads only. `Box(Box)` copies the array; `Box(int[])` does not.

| | Default | Parameterized | Copy (idiom) |
| Who writes it | Compiler, if none exist | You | You |
| Parameters | None (plus hidden outer, if inner) | Your list | Typically one same-type argument |
| After you add another ctor | Disappears | Stays as that overload | Stays as that overload |
| Language status | Specified implicit form | Ordinary constructor | Ordinary constructor |

> [!warning] Any explicit constructor kills the default
> `class C { C(int n) {} }` has **no** `C()`. Callers who wrote `new C()` break. If you still want no-arg creation, **declare** `C() { }`.

> [!warning] A handwritten `C() { }` is not the default constructor
> The default is only the **implicit** one. Interviews that say “default constructor” for every no-arg are using the word loosely. The implicit form also **cannot** have a `throws` clause.

> [!warning] `C(C other)` is shallow unless you copy mutables
> `this.buf = other.buf` aliases the same array or list. A later mutation through either object is visible to both. Java will not emit a deep copy constructor the way some C++ compilers emit a memberwise copy constructor.

> [!tip] Interview answer
> The default constructor is added only when a class declares none: no-arg, same access as the class, body super(). A parameterized constructor is any constructor you declare with arguments; writing one suppresses the default. A copy constructor is not a Java feature — it is a parameterized constructor that takes another instance and copies fields, shallow unless you copy nested state yourself.
