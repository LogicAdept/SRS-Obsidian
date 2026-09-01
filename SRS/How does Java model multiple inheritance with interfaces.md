<!--
reps: 0
priority: 0
-->
#Java/OOP/Inheritance #Java/OOP/Interfaces #SRS

# How does Java model multiple inheritance with interfaces?

> [!abstract] Short answer
> A class has **one** direct superclass and **any number of direct superinterfaces** (`implements A, B, C`). An interface may **`extends` many** interfaces. The class **implements** every superinterface, including those reached through other interfaces or through the superclass. That is **multiple inheritance of types** (and, since Java 8, of **default method bodies**), not of **instance fields** or **class** lineages. Classes: [[Does Java support multiple inheritance for classes]]. Why no class MI: [[Why does Java disallow multiple class inheritance]]. vs abstract class: [[What is the difference between a Java interface and an abstract class]].

## Many superinterfaces, one superclass

`implements` lists the **direct superinterface types**. The same interface named twice (even as `Cloneable` and `java.lang.Cloneable`) is a compile-time error. Superinterface-hood is **transitive**: `Paintable extends Colorable` and `PaintedPoint implements Paintable` means `PaintedPoint` implements `Colorable` too. A type can be a superinterface **in more than one way**; inheriting the **same** declaration along two paths is not an error.

Interfaces form a DAG. There is **no** interface analogue of `Object` that every interface extends.

**Abstract methods.** Two unrelated interfaces may both declare `int foo()`. A class that implements both **inherits both**; they are override-equivalent, so one concrete (or `abstract` class) method implements them. The class does not “pick” `I1.foo` vs `I2.foo` as separate members.

**Default methods.** A class inherits `default` methods from superinterfaces unless a **concrete** superclass method already overrides that signature (class body wins). Two **different** default bodies with the same signature **conflict** until the class (or a subinterface) **overrides** and, if needed, calls `I.super.m()`. If one superinterface **already overrides** the other, that override wins and there is no diamond. Defaults vs `static`: [[How do default interface methods differ from static interface methods]]. `I.super`: [[How do you invoke a default interface method from an implementing class]].

**Not modeled:** instance state (interface fields are constants), constructors, `protected` members. Two different **parameterizations** of the same generic interface (`List<String>` and `List<Integer>`) cannot both be superinterface types of one class.

```d2
direction: down
obj: "Object" {
  width: 100
  height: 36
  style.fill: "#e3f2fd"
}
cls: "class C extends Super\nimplements A, B" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
a: "interface A" {
  width: 120
  height: 36
}
b: "interface B extends A" {
  width: 160
  height: 36
}
obj -> cls
cls -> a
cls -> b
b -> a: "also a superinterface of C"
```

**Fig. 1.** One class parent. Many interface parents. The same interface may be reached twice.

```java
interface Colorable {
    void setColor(int color);
}

interface Paintable extends Colorable {
    void setFinish();
}

interface Left {
    default String name() {
        return "L";
    }
}

interface Right {
    default String name() {
        return "R";
    }
}

class Point {
    int x, y;
}

class ColoredPoint extends Point implements Colorable {
    int color;

    @Override
    public void setColor(int color) {
        this.color = color;
    }
}

class PaintedPoint extends ColoredPoint implements Paintable {
    @Override
    public void setFinish() {}
}

class Pick implements Left, Right {
    @Override
    public String name() {
        return Left.super.name();
    }
}
```

**Listing 1.** `PaintedPoint` implements `Colorable` through `Paintable` and through `ColoredPoint`. `Pick` must override the two default `name` methods.

> [!warning] Two default methods with the same signature do not merge
> `implements Left, Right` is a compile-time error until you declare `name()` in the class. Two **abstract** `foo()` declarations with the same signature **do** merge into one method to implement.

> [!warning] This is not C++ multiple inheritance of objects
> You do not get two copies of fields, and you cannot `extends` two classes. Mix in **types** and **default behavior**; put **state** on the class (or on the one abstract superclass). Design split: [[How does abstract class differ from interface in which cases should you use abstract class and in which interf]].

> [!warning] `List<String>` and `List<Integer>` cannot both be implemented
> Erasure would make both `List`. Name each generic interface at most once, with one parameterization (or the raw type, not both).

> [!tip] Interview answer
> Java models multiple inheritance with interfaces: a class extends one class and implements many interfaces, and an interface may extend many interfaces. The class is a subtype of every superinterface. Abstract methods with the same signature are implemented once; conflicting default methods must be overridden. There is no multiple inheritance of class state.
