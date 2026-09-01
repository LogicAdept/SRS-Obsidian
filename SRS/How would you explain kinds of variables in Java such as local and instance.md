<!--
reps: 0
priority: 0
-->
#Java/Language #Java/OOP #SRS

# How would you explain kinds of variables in Java such as local and instance?

> [!abstract] Short answer
> A **variable** is a **storage location** with a compile-time type. Java has **eight** kinds. An **instance variable** is a non-`static` field: one per object, **default-initialized** (`0` / `false` / `null`). A **local variable** is declared by a **statement** or a **pattern**: it lives in a block / `for` / `try`, has **no** default, and must be **definitely assigned** before use. The others are **class** (`static`) fields, **array components**, **method / constructor / lambda parameters**, and **`catch` exception parameters**. Defaults: [[How would you explain what values initialized variable by default]]. Locals: [[Why must a local primitive variable be initialized before use in Java]]. Instance vs `static`: [[What is the difference between an instance member and a static member in Java]].

## Eight kinds, different lifetimes

**Instance vs local (the usual interview pair).** `int x;` on a class is an instance field created with **each** `new` (and in subclasses). `int oldx = this.x;` inside a method is local: created when control enters the enclosing **block**, gone when that declaration is out of **scope**. You may use `p.x` after `new Point()` without writing `x = 0`. You may **not** use `int n; System.out.print(n);`.

**Class variable.** `static` field in a class, or a field of an interface. One per class, created when the class is **prepared**, default-initialized. `static`: [[What does the static keyword mean in Java]].

**Array component.** Unnamed slot `w[i]`, default-initialized when the array is created. `final w` still lets you write `w[0]`.

**Parameters.** Method, constructor ([[What is constructor]]), and lambda parameters are new variables **per invocation**, filled with the argument. Exception parameters are filled with the thrown object for the `catch` block. Lambda capture: [[Which variables can a Java lambda expression capture]].

**Pattern variables.** `if (o instanceof Point p)` — `p` is a local created when the pattern **matches**.

```d2
direction: down
v: "variable = storage + type" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
def: "defaulted\nclass, instance, array slot" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
arg: "from the caller\nmethod / ctor / lambda / catch" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
da: "definite assignment\nlocal (statement)" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
v -> def
v -> arg
v -> da
```

**Fig. 1.** Fields and array slots get defaults. Parameters get arguments. Statement locals must be assigned before use.

```java
class Point {
    static int numPoints;
    int x, y;
    int[] w = new int[10];

    int setX(int x) {
        int oldx = this.x;
        this.x = x;
        return oldx;
    }

    boolean equalAtX(Object o) {
        if (o instanceof Point p) {
            return this.x == p.x;
        }
        return false;
    }
}
```

**Listing 1.** `numPoints` class variable; `x`,`y` instance; `w[0]` array component; `setX`’s `x` parameter; `oldx` local; `p` pattern variable.

| Kind | Created | Initial value |
| Class | class prepared | default |
| Instance | each `new` | default |
| Array component | `new T[n]` | default |
| Method / ctor / lambda parameter | each call | the argument |
| Exception parameter | each `catch` | the thrown object |
| Local (statement) | enter block / `for` / try-with-resources | must assign |
| Local (pattern) | pattern matches | the matched value |

> [!warning] Locals do not start at `0`
> `int n;` as a field is `0`. As a local it is unusable until assigned. That is definite assignment, not a runtime “uninitialized memory” read.

> [!warning] A parameter named `x` hides the instance field `x`
> `this.x` is the field. Bare `x` in `setX` is the parameter. Forgetting `this.` assigns the parameter to itself.

> [!warning] Eight kinds, not two
> Interview “local vs instance” is the pair. The language also counts `static` fields, array slots, and every flavor of parameter. `catch (Exception e)` is not a local-variable declaration statement; `e` is an **exception parameter**.

> [!tip] Interview answer
> Instance variables are non-static fields: one per object, default-initialized. Local variables are declared in a block or by a pattern and must be definitely assigned before use. Class variables are static fields, one per class. Parameters and array components are variables too; they get the argument or a default slot, not definite-assignment rules like a bare local int.
