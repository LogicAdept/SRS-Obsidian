<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is GRASP

> [!abstract] Short answer
> GRASP (General Responsibility Assignment Software Patterns) is a set of nine fundamental principles for object design and responsibility assignment published by Craig Larman in "Applying UML and Patterns". Unlike GoF, GRASP does not catalogue ready-made structures - it answers the question "which object should own this responsibility?".

## The nine principles

* **Information Expert** - assign a responsibility to the class that holds the information needed to fulfill it.
* **Creator** - class B should create object A when B contains, records, closely uses, or holds the initializing data for A.
* **Controller** - a non-UI object that receives and coordinates system events: one use-case controller per use case, or a facade controller for the whole system; it delegates work instead of doing it.
* **Low Coupling** - assign responsibilities so classes depend on each other less; a change in one class then has a smaller impact, and reuse potential rises.
* **High Cohesion** - keep each class focused on strongly related responsibilities; low cohesion makes subsystems hard to understand, reuse, and maintain.
* **Polymorphism** - when behavior varies by type, put the variation into polymorphic operations of those types instead of type checks in client code.
* **Protected Variations** - identify points of predicted instability and wrap them behind a stable interface so variations do not affect other elements.
* **Indirection** - insert an intermediate object to mediate between two elements so they do not couple directly; MVC mediates model and view this way.
* **Pure Fabrication** - invent a class that does not represent a domain concept, purely to keep coupling low and cohesion high; domain-driven design calls such classes Services.

```d2
direction: right
assign: "Who owns the work" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
eval: "How to keep the design healthy" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
vary: "How to absorb change" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
expert: "Information Expert\nCreator\nController" {
  width: 220
  height: 100
  style.fill: "#e3f2fd"
}
coupling: "Low Coupling\nHigh Cohesion" {
  width: 220
  height: 100
  style.fill: "#fff3e0"
}
variation: "Polymorphism\nProtected Variations\nIndirection\nPure Fabrication" {
  width: 230
  height: 110
  style.fill: "#e8f5e9"
}
assign -> expert
eval -> coupling
vary -> variation
```

**Fig. 1.** The nine principles fall into three practical groups: assigning responsibilities, evaluating the result, and protecting against foreseeable change.

## Expert in action

```java
class Order {
    private final List<OrderLine> lines;

    // Information Expert: Order holds the lines, so Order computes the total
    Money total() {
        Money sum = Money.zero();
        for (OrderLine line : lines) {
            sum = sum.plus(line.subtotal());
        }
        return sum;
    }
}
```

**Listing 1.** The alternative - an `OrderService` that pulls every line out through getters and sums them - leaves the data in one class and the knowledge in another.

Low Coupling and High Cohesion are measurable, not vibes: [[What are coupling and cohesion and how do they affect maintainability]] shows the maintainability effect, and [[What are afferent coupling and efferent coupling]] gives the direction of dependency you are minimizing. When the variation is behavioral, Polymorphism in GRASP is exactly the ground the GoF pair in [[What is the difference between the Strategy and State design patterns]] stands on. Frameworks lean on the same principles: [[What design patterns does the Spring Framework use]] shows a front controller and handlers that are GRASP Controller applied.

Larman stresses that these are a mental toolset, not new ways of working: they document and standardize tried-and-tested object-oriented design practice. Low Coupling and High Cohesion are explicitly evaluative - you use them to judge candidate designs made with the other seven.

> [!warning] Two common interview traps
> First, GRASP is not GoF: there is no factory, observer, or strategy here - those catalogue collaboration structures, while GRASP assigns responsibilities. Second, a "controller" in GRASP must delegate; a class that receives a system event and then executes domain logic itself is a fat controller, which violates the principle it is named after.

> [!tip] Interview answer
> GRASP is Larman's set of nine responsibility-assignment principles: Information Expert, Creator, Controller, Low Coupling, High Cohesion, Polymorphism, Protected Variations, Indirection, and Pure Fabrication. I use Expert, Creator, and Controller to decide which object owns a responsibility, Low Coupling and High Cohesion to evaluate the design, and the rest to handle variation safely. It differs from GoF in that it assigns responsibilities rather than cataloguing object structures, which is why I reach for it at design time before any GoF pattern.
