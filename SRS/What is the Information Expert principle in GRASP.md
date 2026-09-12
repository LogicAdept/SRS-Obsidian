<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the Information Expert principle in GRASP

> [!abstract] Short answer
> Information Expert is a GRASP principle for assigning responsibilities: give the work to the class that holds the information needed to do it. When you wonder where a method belongs, find the data the method depends on and put the method next to that data.

## How Expert assigns a responsibility

The principle turns "where does this method go" into a short procedure. You state the responsibility, list the information it needs, find which class already holds that information, and assign the responsibility there. This is the default GRASP heuristic for the nine principles: it is the first tool you reach for, and the other principles judge or override its result.

The canonical point-of-sale example: a sale knows its line items, so the sale computes its own total. A cashier object or a checkout service should not pull the lines out through getters and sum them somewhere else, because then the data lives in one class and the knowledge lives in another.

```java
import java.util.List;

record Money(int cents) {
    Money plus(Money other) {
        return new Money(cents + other.cents);
    }
}

record SalesLineItem(int quantity, Money unitPrice) {
    Money subtotal() {
        return new Money(quantity * unitPrice.cents());
    }
}

class Sale {
    private final List<SalesLineItem> lines;

    Sale(List<SalesLineItem> lines) {
        this.lines = List.copyOf(lines);
    }

    Money total() {
        Money sum = new Money(0);
        for (SalesLineItem line : lines) {
            sum = sum.plus(line.subtotal());
        }
        return sum;
    }
}
```

**Listing 1.** The sale holds the line items, so the total lives on the sale, and each line computes its own subtotal because it holds quantity and price.

```d2
direction: down
resp: "1. State the responsibility\ne.g. compute the sale total" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
info: "2. List the information it needs\nline items, quantities, prices" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
holder: "3. Find the class that\nalready holds that information" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
assign: "4. Assign the method there" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
check: "5. Re-check Low Coupling\nand High Cohesion" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
resp -> info -> holder -> assign -> check
```

**Fig. 1.** Expert is a loop, not a one-shot rule: after assigning the responsibility to the information holder, you re-evaluate the design with the evaluative principles.

## Why the result stays healthy

Data and behavior land in one place, so a change to pricing rules touches a single class instead of every service that re-implements the sum. Encapsulation also survives: callers ask the sale for its total instead of walking through its state, which is the same instinct captured in [[What is tell don't ask in object oriented design]].

Ignoring Expert produces the opposite shape: domain objects turn into getter bags while free-floating services do all the computation. That decomposition is exactly how [[What is an anemic domain model and is it useful]] gets started, and it is the failure mode this principle exists to prevent.

> [!warning] Expert is a direction, not a license
> Following Expert blindly can pile unrelated computations onto one data-heavy class until its cohesion collapses. If the information holder would end up doing several unrelated jobs, re-evaluate with [[What is the High Cohesion principle in GRASP]] or move the job into an invented helper - [[What is the Pure Fabrication principle in GRASP]]. Expert also answers "who owns the work", not "how many reasons may a class have to change" - that separate question is [[How would you explain the single responsibility principle in SOLID]].

> [!tip] Interview answer
> Information Expert says: assign a responsibility to the class that has the information required to fulfill it. I find the data the computation depends on and put the method next to it - a sale computes its own total because the sale holds the line items. It is the default GRASP heuristic, and Low Coupling, High Cohesion, or Pure Fabrication override it when the information holder would get overloaded.
