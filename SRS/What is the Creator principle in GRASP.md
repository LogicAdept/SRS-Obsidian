<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the Creator principle in GRASP

> [!abstract] Short answer
> Creator is a GRASP principle that answers "who should create object A": pick class B when B contains, aggregates, records, closely uses, or holds the initializing data for A. Creation is a responsibility like any other, so it follows the same ownership logic.

## The Creator checklist

Class B is a good creator of object A when at least one of these holds - preferably more than one, because each matching condition makes the choice more defensible:

* B contains or compositely aggregates instances of A;
* B records instances of A;
* B closely uses instances of A;
* B has the initializing data for A and passes it on creation.

The classic point-of-sale reading: a register records sales, so the register creates each sale. An order aggregates its line items, so the order creates its own line items from a product and a quantity. In both cases creation stays next to the object that will actually track and use the new instance.

```java
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

record Product(String sku) {}

record SalesLineItem(Product product, int quantity) {}

class Sale {
    private final Instant startedAt;
    private final List<SalesLineItem> lines = new ArrayList<>();

    Sale(Instant startedAt) {
        this.startedAt = startedAt;
    }

    void addLine(Product product, int quantity) {
        lines.add(new SalesLineItem(product, quantity)); // Sale aggregates lines, so Sale creates them
    }
}

class Register {
    private final List<Sale> recordedSales = new ArrayList<>();

    Sale createSale() {
        Sale sale = new Sale(Instant.now()); // Register records sales, so Register creates them
        recordedSales.add(sale);
        return sale;
    }
}
```

**Listing 1.** Two Creator decisions in one snippet: the register creates the sale it records, and the sale creates the line items it aggregates.

```d2
direction: down
q: "Who should create A?" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
cond: "Does B contain, record, closely use A\nor hold A's initializing data?" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
yes: "B creates A" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
complex: "Creation complex or would couple B\nto concrete variants?" {
  width: 340
  height: 90
  style.fill: "#ffebee"
}
factory: "Escalate to a factory" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
q -> cond
cond -> yes: yes
cond -> complex: creation hurts
complex -> factory
```

**Fig. 1.** Creator is the default answer for creation; a factory appears only when plain creation would fight the evaluative principles.

## When creation gets complicated

Creator is a heuristic, not a law. If creating A inside B would couple B to concrete subclasses it should not know about - plugin implementations, config-selected variants - the low coupling goal wins and creation moves to a factory. That escalation path is what the GoF creational catalogue is for, and it is the bridge from this principle to [[What are examples of creational design patterns]].

> [!warning] Creator and factories are not rivals
> A common interview trap is answering "always use a factory for creation". Factories exist because direct creation would violate low coupling or need variant selection; when neither applies, a factory is extra machinery with no payoff. Start from the Creator checklist and escalate only when a real conflict shows up - see [[What is the Low Coupling principle in GRASP]] for the evaluative side of the argument.

> [!tip] Interview answer
> Creator says B creates A when B contains, records, or closely uses A, or holds its initializing data. A register creates a sale because it records sales; an order creates its line items because it aggregates them. When creation is complex or would couple the creator to concrete variants, hand the job to a factory instead.
