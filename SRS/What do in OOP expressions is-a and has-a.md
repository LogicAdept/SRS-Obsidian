<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Java/OOP/Inheritance #SRS

# What do in OOP expressions is-a and has-a?

> [!abstract] Short answer
> **Is-a** is **subtyping**: `SportsCar` **is a** `Car` (`extends`) or `Square` **is a** `Shape` (`implements`). The subtype may be used where the supertype is expected (`instanceof`, polymorphism). **Has-a** is **a field** (or a collection of fields): `Car` **has an** `Engine`. In Java that is just another reference type stored in the object, not a second inheritance mechanism. Inheritance: [[How would you explain class inheritance in Java and tradeoffs]]. Types: [[How would you explain main concepts OOP class object interface]]. Prefer has-a when you do not need a subtype: [[What are the advantages and disadvantages of object oriented programming]].

## Subtype vs a part

**Is-a (`extends` / `implements`).** The subclass relationship is the transitive closure of `extends`. `implements` is the same idea for **interface types**: the class’s instances are values of that type. One class superclass; many superinterfaces ([[Does Java support multiple inheritance for classes]]). `car instanceof Vehicle` tests the **run-time class** against a type. This is how polymorphism is written ([[What is polymorphism]]).

Use is-a only when every instance of the subtype **really is** usable as the supertype (same contract). `Square extends Rectangle` with independently settable width and height is the usual counterexample.

**Has-a (a field).** A class declares an instance variable whose type is another class or interface. That is **association** in UML talk. **Composition** usually means “the part is owned and does not outlive the whole”; **aggregation** means “shared part.” The language does **not** distinguish them: both are fields. `private final Engine engine` plus constructing the engine inside `Car` is the Java convention for exclusive ownership. GC does not delete `Engine` when `Car` becomes unreachable if another reference still exists. Public fields that expose the part break encapsulation ([[How would you explain problems with public mutable fields in Java]]).

**Dump.** “Является” → inheritance (and `implements`). “Имеет” → a field, called association / aggregation / composition in modeling. Not three different Java keywords.

```d2
direction: down
isa: "is-a\nextends / implements" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
has: "has-a\ninstance field" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Is-a is a type relationship. Has-a is storage of another object.

```java
interface Shape {
    int area();
}

class Square implements Shape {
    private final int side;

    Square(int side) {
        this.side = side;
    }

    @Override
    public int area() {
        return side * side;
    }
}

class Window {
    private final Shape shape;

    Window(Shape shape) {
        this.shape = shape;
    }

    int area() {
        return shape.area();
    }
}
```

**Listing 1.** `Square` **is a** `Shape`. `Window` **has a** `Shape`. `Window` does not `extend Square`.

> [!warning] `implements` is is-a, not has-a
> `class ArrayList implements List` means an `ArrayList` **is a** `List`. A `List` field on `Order` means the order **has** a list. Mixing the two is the usual design bug (extending `ArrayList` to make a `Stack`).

> [!warning] Aggregation vs composition is not a Java construct
> You will not find `aggregate` in the language. Lifetime and sharing are how you **write** constructors and who keeps the reference. `final` does not mean composition; it only freezes that field’s reference.

> [!warning] Is-a is not “reuse a couple of methods”
> If you only need behavior, a field plus forwarding (has-a) avoids the fragile superclass. Use `extends` when callers must pass the new type where the old type is required.

> [!tip] Interview answer
> Is-a means subtyping: `extends` or `implements`, checked with `instanceof` and used for polymorphism. Has-a means the class holds a reference to another object as a field. UML aggregation versus composition is ownership, not a keyword. Prefer has-a unless you truly need a subtype.
