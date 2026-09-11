<!--
reps: 0
priority: 0
-->
#Methodologies/Principles #SRS

# Where should you prefer inheritance versus aggregation?

> [!abstract] Short answer
> Prefer inheritance only for a true, stable is-a relationship where the subclass honors the base contract everywhere the base is used - substitutability is the entry fee, and polymorphism through a shared interface is the point. Prefer aggregation (has-a with delegation) for reusing behavior, sharing roles, varying at runtime, and anything where "part of" or "uses" is the honest relation. The GoF formulation is the tiebreaker: favor object composition over class inheritance - and Java's single-inheritance budget makes spending it on code reuse a waste.

## The decision, step by step

First question: is the relation genuinely is-a in BEHAVIOR, not just in English? A `Square` is-a `Rectangle` geometrically and still breaks `Rectangle`'s contract behaviorally - the language feeling is not the test, substitutability is ([[How would you explain is-a versus has-a relationships in object oriented design]]). Second: will clients use the object through the base type's interface (polymorphism, framework hooks, sealed hierarchies)? That is inheritance paying rent. Third: is the base stable and documented for extension - a fragile base class changes its internals and silently breaks subclasses. If any answer is no, aggregate: hold the object, delegate the calls, and stay free to swap, compose, and test independently ([[How does composition differ from inheritance]]).

```java
// Inheritance earns its cost: framework extension point, substitutable behavior
class AuditingOrderRepo implements OrderRepository {
    private final OrderRepository delegate;      // aggregation first
    AuditingOrderRepo(OrderRepository delegate) { this.delegate = delegate; }
    public Order save(Order o) { audit(o); return delegate.save(o); }
}

// Aggregation for reuse: role composed, swappable at runtime
class PricingService {
    private final TaxPolicy tax;                 // has-a, not is-a
    PricingService(TaxPolicy tax) { this.tax = tax; }
}
```

**Listing 1.** Conceptual. The decorator aggregates and delegates instead of extending the repository; the service composes a policy. Neither needs inheritance to vary behavior.

## Where inheritance remains right

Extension points DESIGNED for it: abstract skeleton implementations (`AbstractList`-style templates with documented hooks), sealed type hierarchies where the author controls the variant set, genuine taxonomies of substitutable behavior consumed polymorphically. In those cases inheritance is not code reuse - it is TYPE declaration: the subclass says "I honor that contract", which is information the compiler and readers use. What inheritance should not be used for: borrowing convenience methods, reusing constants, forcing `extends` for shared helpers - all of that is aggregation or composition of a utility ([[What are alternatives to class inheritance]], [[How would you explain common guidelines for using inheritance in OOP]]).

> [!warning] "Is-a in the domain means extends in code" breaks both directions
> Domain language is loose - a manager IS an employee, but `Manager extends Employee` freezes an org-chart accident into the type system; tomorrow a person is both, or the role changes, and inheritance cannot un-become. The reverse is equally wrong: reflexively delegating for EVERYTHING (a class with forty one-line forwarding methods) buys nothing and buries the reader. The scale: inherit for type substitutability on stable contracts; aggregate for flexibility; compose for parts-whole; and let the base class's documentation for extension - not vocabulary - make the call ([[How does composition differ from inheritance]]).

> [!tip] Interview answer
> I reach for inheritance only when substitutability is real and clients consume the base type - stable frameworks, sealed hierarchies, designed extension hooks. Everything else - behavior reuse, roles, runtime variability, testing seams - is aggregation with delegation, which stays swappable and avoids the fragile base class trap. Java gives me one parent slot, so I refuse to spend it on convenience reuse.
