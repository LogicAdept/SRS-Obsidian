<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the difference between an entity and a value object?

> [!abstract] Short answer
> An entity is defined by identity: it has an id that persists through state changes, two instances with the same id are the same thing, and its state is expected to change. A value object is defined by its attributes: no identity, immutable, two instances with equal attributes are interchangeable and typically replace each other rather than mutate. Equality by id versus equality by value is the mechanical difference; track-over-time versus describe-a-state is the modeling difference.

## The two equality contracts

The distinction becomes concrete the moment both land in a `HashSet`. Two `Money(500, "EUR")` instances are the same value - a set keeps one. Two orders with the same total but different ids are different orders - a set keeps both. Conversely the same order with different statuses is still the same order: the id outlives every attribute change. That is why value objects are immutable: if you need a different value, you create a new instance, and "changing" a value means replacing it in its holder. Entities carry mutable state deliberately - their job is to persist through change while staying themselves.

```java
record Money(long cents, String currency) {}                    // value object

static final class Order {                                      // entity
    final long id; String status;
    Order(long id) { this.id = id; }
    @Override public boolean equals(Object o) {
        return o instanceof Order other && other.id == id;      // by identity
    }
    @Override public int hashCode() { return Long.hashCode(id); }
}

Money a = new Money(500, "EUR");
System.out.println(a.equals(new Money(500, "EUR")));             // true - same value
Order o1 = new Order(1); o1.status = "SHIPPED";
Order o2 = new Order(2); o2.status = "SHIPPED";
System.out.println(o1.equals(o2));                               // false - same attrs, different id
```

**Listing 1.** Verified on JDK 21.0.12.1: equal `Money` values collapse to one element in a `Set`; two orders with the same id collapse to one, while `o1.equals(o2)` is false for ids 1 and 2 even with identical attributes.

```d2
direction: down
q: "Does the concept need a trackable identity\nover time?" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
ent: "Entity\nid persists, state mutates,\nequality by id" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
vo: "Value object\nimmutable, attribute-defined,\nequality by value" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
q -> ent: "yes"
q -> vo: "no"
replace: "update = replace\nthe whole value" {
  width: 220
  height: 70
  style.fill: "#f3e5f5"
}
vo -> replace
```

**Fig. 1.** The modeling question is whether identity must survive over time; everything else - mutability, equality, replacement - follows from that answer.

## Choosing and converting

The default recommendation is value objects wherever possible: they are immutable, thread-safe, trivially testable, and interchangeable, which keeps aggregates small and reasoning local. Promote a concept to an entity only when identity genuinely matters - when the business tracks the same thing across state changes, or must distinguish two identical-attribute instances (two shipped orders that both cost 500 EUR are still two orders). The same real-world thing can be an entity in one context and a value object in another: an address is a value inside an order, but a tracked record in an audit context. Conversion goes both ways - a postal code string becomes a `PostalCode` value object the moment its format rules matter, and a value gains a row in a table the moment it must be tracked.

> [!warning] Entity does not mean "has a database id"
> A common lie: "every JPA class is an entity". The DDD entity is a domain judgment about identity, not a persistence annotation. A JPA class whose equality rests on a generated surrogate key, whose instances are compared attribute by attribute elsewhere in the code, is neither fish nor fowl - and equals/hashCode bugs follow ([[In a business context must equals consider all entity fields]]). Also beware the reverse overshoot: making everything an entity "for flexibility" costs immutability, hash safety, and aggregation clarity ([[What is a value object and why should you use one]]).

> [!tip] Interview answer
> An entity has identity that survives state changes - equality by id, mutable state, tracked over time. A value object has no identity - equality by attributes, immutable, interchangeable, "updated" by replacement. The modeling question is whether the business tracks the same thing through change; the mechanical tell is what equality means for each.

