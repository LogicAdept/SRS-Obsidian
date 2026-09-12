<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the Low Coupling principle in GRASP

> [!abstract] Short answer
> Low Coupling is an evaluative GRASP principle: assign responsibilities so that classes know about and depend on as few other elements as possible. Lower dependency means a change in one class has a smaller impact on the rest, and classes become easier to reuse in isolation.

## What the principle evaluates

Coupling is a measure of how strongly one element is connected to, has knowledge of, or relies on other elements. Low Coupling is not a "do this" rule like Expert or Creator - it is a yardstick you hold against candidate responsibility assignments. When two assignments both work, the one that leaves classes knowing less about each other wins, because it buys the three benefits the principle names: lower dependency between classes, lower impact of a change in one class, and higher reuse potential.

Consider two assignments of the same responsibility - persisting a sale:

```java
// Assignment A: the sale persists itself - Sale now knows JDBC
class Sale {
    void save(java.sql.Connection connection) throws java.sql.SQLException {
        // INSERT INTO sales ... - domain object married to storage details
    }
}

// Assignment B: persistence moves to a dedicated class - Sale knows nothing about storage
class Sale {
    // domain state and behavior only
}

class JdbcSaleRepository {
    private final java.sql.Connection connection;

    JdbcSaleRepository(java.sql.Connection connection) {
        this.connection = connection;
    }

    void save(Sale sale) {
        // INSERT INTO sales ...
    }
}
```

**Listing 1.** Both assignments produce working code, but assignment B spreads less knowledge across the design: the domain object's coupling to storage drops to zero.

```d2
direction: right
a: "Assignment A\nSale -> JDBC Connection\ncoupling: 2 classes touched\nby a storage change" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
b: "Assignment B\nSale -> (nothing)\nJdbcSaleRepository -> JDBC\ncoupling: storage change is\ncontained in one class" {
  width: 300
  height: 120
  style.fill: "#e8f5e9"
}
note: "Same behavior\ndifferent knowledge spread" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
a -> note
b -> note
```

**Fig. 1.** The principle compares designs by how much they must know: a storage change ripples through the domain object in assignment A and stays inside the repository in assignment B.

## Reading coupling in both directions

The measurable side of this principle lives in [[What are afferent coupling and efferent coupling]]: efferent coupling counts how many elements a class depends on, afferent counts how many depend on it. A responsibility assignment that inflates either number is a candidate for reassignment - which is exactly how this principle teams up with [[What is the Pure Fabrication principle in GRASP]] when the natural owner would couple a domain object to infrastructure. The maintainability effect of the pairing is measured in [[What are coupling and cohesion and how do they affect maintainability]], and [[What is the Law of Demeter]] is its best-known local rule of thumb for everyday code.

> [!warning] Low Coupling is not zero coupling
> A system where nothing knows anything about anything else does nothing; collaboration always couples someone to someone. The goal is the lowest coupling that still expresses the domain, not layers of pass-through wrappers that merely hide dependencies. Also remember that hiding coupling behind [[What is the Indirection principle in GRASP]] does not remove it - a leaky intermediary that forwards the other side's types has just moved the problem one hop.

> [!tip] Interview answer
> Low Coupling is an evaluative GRASP principle: when choosing where a responsibility goes, prefer the assignment that leaves classes knowing about fewer others. It is measurable through afferent and efferent coupling, it buys smaller blast radius for changes and better reuse, and it is the yardstick that often overrides Expert - a sale holds its data, but persistence still goes to a fabricated repository so the domain object stays decoupled from storage.
