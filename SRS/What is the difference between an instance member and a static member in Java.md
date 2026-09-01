<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/Modifiers/Static #SRS

# What is the difference between an instance member and a static member in Java?

> [!abstract] Short answer
> An **instance** field or method belongs to **one object**: each instance has its own field values, and an instance method runs with a `this` (it can use instance state). A **`static`** field or method belongs to the **class**: there is one class variable, and a class method runs in a **static context** (no `this` / `super`) and can be called as `ClassName.m()` without an instance. Meaning of the keyword: [[What does the static keyword mean in Java]]. Methods: [[How would you explain static methods in Java]]. Nested types and other targets: [[How would you explain which Java language constructs can be marked static]].

## Per-object vs per-class

| | Instance member | `static` member |
| --- | --- | --- |
| Field | one variable per object | one variable per class |
| Method | needs a receiver; has `this` | no `this`; call `TypeName.m()` |
| Nested class | inner: enclosing instance | no enclosing instance |
| When initialized | with the object (field / instance initializer / constructor) | during **class** initialization |
| Inheritance | instance methods **override** | `static` methods **hide** |

A `static` method is **not** limited to other `static` names. It may call instance methods and read instance fields **of an object it is given**. What it cannot do is use `this` or `super`, or name instance members of its own class as if they were in scope.

Instance methods may use both instance members and `static` members. Creating an object is required to **invoke** an instance method (a `null` receiver throws). A class method does not need an instance; `expr.m()` on a **class** method still evaluates `expr` and then ignores it.

```java
class Cell {
    static int created = 0;
    int id;

    Cell() { id = ++created; }

    void show() { System.out.println(id + " of " + created); }

    static int total() { return created; }
}
```

**Listing 1.** Two `new Cell()` values have different `id`s and share `created`. `show()` needs an instance; `Cell.total()` does not.

```d2
direction: down
type: "class Cell\nstatic created, total()" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}
c1: "cell 1\nid" {
  width: 100
  height: 40
  style.fill: "#e8f5e9"
}
c2: "cell 2\nid" {
  width: 100
  height: 40
  style.fill: "#e8f5e9"
}
type -> c1
type -> c2
```

**Fig. 1.** Instance members live on the objects. Static members live on the class.

> [!warning] The “static methods may only use static stuff” rule is false
> They may not use `this`. They **may** use `cell.show()` or `cell.id` when `cell` is a reference. The dump that lists three absolute bans (only static methods, only static fields, no `this`) conflates “no implicit instance” with “no instances at all.”

> [!warning] Override vs hide
> Two instance methods with the same signature form an override. Two `static` methods with the same signature in a subclass **hide**. Call site uses the **compile-time** type. Instance and `static` methods do not override or hide each other: [[Can static method be override or]].

> [!tip] Interview answer
> Instance members are per object: fields can differ, methods run with `this`. Static members are per class: one field, a method you can call on the type name with no instance. A static method cannot use `this`, but it can use instance members through a reference. Static methods hide; instance methods override.
