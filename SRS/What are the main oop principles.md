<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #SRS

# What are the main oop principles?

> [!abstract] Short answer
> In Java interviews the **main** principles are **encapsulation**, **inheritance**, and **polymorphism**; many lists add **abstraction**. They are **design words** for mechanisms the language actually has: access control, `extends`/`implements`, virtual dispatch, `abstract`/interface types. Java: [[What does it mean that Java is object oriented]]. Paradigm compare: [[What are the pros and cons of OOP versus procedural and functional programming]]. History: [[Why was object oriented programming favored by the industry for so long]]. Encapsulation: [[How would you explain encapsulation in object oriented design]]. Inheritance: [[How would you explain class inheritance in Java and tradeoffs]]. Polymorphism: [[What is polymorphism]]. Abstraction: [[Which has the highest abstraction level among class abstract class and interface]].

## Four names, four Java mechanisms

**Encapsulation.** Fields and helper methods stay behind access modifiers. Callers use a published API. Not “all fields `private`” as a slogan—`public` mutable fields break it. The invariants hiding protects: [[What is a representation invariant and abstraction function]].

**Inheritance.** A class has **one** superclass (`extends`) and any number of superinterfaces (`implements`) ([[Does Java support multiple inheritance for classes]]). Subclasses reuse and specialize. It is coupling, not a free lunch.

**Polymorphism.** A variable of a supertype refers to a subtype instance; an instance method uses the **run-time class**. Overloading is compile-time and is **not** this principle ([[How would you explain Overload vs Override]]).

**Abstraction.** You program to a **type** (`interface`, `abstract class`) that omits details. Highest-abstraction interview ranking is the interface; that is still a type, not a fourth JVM feature.

**Dump extras.** **Message passing** is Smalltalk talk; in Java it is **method invocation** (and does not need a fifth bullet). **Reuse** is a **goal** of the four, not a separate principle. There is **no** “only correct order of paradigms.” Encapsulation does not have to precede inheritance in a program, and polymorphism does not “use” inheritance only—interfaces suffice.

Tradeoffs of the whole approach: [[What are the advantages and disadvantages of object oriented programming]].

```d2
direction: down
abs: "abstraction\nShape type" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
enc: "encapsulation\nprivate fields" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
inh: "inheritance\nextends / implements" {
  width: 240
  height: 36
  style.fill: "#fff8e1"
}
pol: "polymorphism\nrun-time dispatch" {
  width: 220
  height: 36
  style.fill: "#f3e5f5"
}
abs -> enc
enc -> inh
inh -> pol
```

**Fig. 1.** A teaching order, not a language law. You can have polymorphism through interfaces with no class `extends`.

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

class Use {
    static int total(Shape[] shapes) {
        int n = 0;
        for (Shape s : shapes) {
            n += s.area();
        }
        return n;
    }
}
```

**Listing 1.** Abstraction: `Shape`. Encapsulation: `side`. Inheritance: `implements Shape`. Polymorphism: `s.area()`.

> [!warning] Three, four, or six — say which list
> **EIP** (encapsulation, inheritance, polymorphism) is the short answer. **A-PIE** adds abstraction. “Message passing” and “reuse” are not Java syllabus principles. Do not claim a unique official order.

> [!warning] Inheritance is not required for polymorphism
> `Shape s = new Square(3); s.area();` needs a **subtype**, which can be `implements` only. `static` methods and overloads do not count as OOP polymorphism.

> [!warning] Encapsulation is not the `class` keyword
> A class full of public fields is not encapsulated. Abstraction without access control still leaks representation.

> [!tip] Interview answer
> The main OOP principles in Java are encapsulation, inheritance, and polymorphism; abstraction is the usual fourth. Encapsulation is access control, inheritance is `extends`/`implements`, polymorphism is virtual dispatch on a supertype, abstraction is depending on interface or abstract types. Message passing is just method calls here, and reuse is a benefit rather than a fifth principle.
