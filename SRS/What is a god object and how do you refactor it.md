<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Methodologies/Principles #SRS

# What is a god object and how do you refactor it?

> [!abstract] Short answer
> The **god object** anti-pattern: one class accumulates knowledge and responsibilities from most of the system — every field, every use case, every dependency. It **maximizes coupling** (everything depends on it and it depends on everything) while **destroying cohesion** (its methods operate on disjoint subsets of its state) ([[What are coupling and cohesion and how do they affect maintainability]]). The refactor is incremental: pin behavior with tests, extract cohesive clusters of data plus behavior along **domain concepts**, define interfaces at the seams ([[What is an antipattern]]).

## The symptoms

A god object announces itself: a `Manager`/`Processor`/`ServiceImpl` with hundreds of methods; fields where disjoint method groups touch disjoint halves; a constructor taking fifteen dependencies; merge conflicts always in the same file; test setups that construct the world to exercise one method. The economic driver is inertia — adding one more method to the one class everybody already imports is always locally cheaper than a design decision. The cost is global: every feature now risks the god's state, changes radiate in all directions, and the class can be tested only as a whole.

## Why layering alone does not fix it

A common rescue attempt — splitting the god into `Service`, `Repository`, and `DTO` layers — reproduces the disease vertically: each layer becomes a slimmer god that still owns every domain concept at once. The cut that works is **by domain concept**, not by technical role: order lifecycle, pricing, notifications each become small classes owning their data and rules ([[What is tell don't ask in object oriented design]] keeps behavior beside data). The single-responsibility principle is the compass: one reason to change per class ([[How would you explain the single responsibility principle in SOLID]]).

## The refactor path

First, **characterization tests** around existing behavior — the god has no seams, so tests must come before structure. Second, build the method-by-field usage matrix: which methods read and write which state; connected components are extraction candidates. Third, extract cluster by cluster — private fields move with the methods that use them; late-stage the extracted components keep an interface so callers depend on roles, not concretions. Fourth, shrink the god into a **temporary facade** delegating to the new classes, then retire it call site by call site. Attempting a big-bang rewrite instead usually produces a second god — or the same one with a new name ([[What are alternatives to class inheritance]]).

```d2
direction: right
god: "GodObject\n40 fields, 300 methods\nknows everything" {
  width: 240
  height: 84
  style.fill: "#ffebee"
}
after: "extracted by domain concept" {
  width: 260
  height: 44
  style.fill: "#e8f5e9"
}
a: "OrderLifecycle" {
  width: 140
  height: 40
}
b: "Pricing" {
  width: 140
  height: 40
}
c: "Notifications" {
  width: 150
  height: 40
}
god -> after: "tests first, then move"
after -> a
after -> b
after -> c
```

**Fig. 1.** The extraction splits the hub into concepts, each owning the state its methods actually touch.

```java
// BEFORE: one class, disjoint field groups, every reason to change
class OrderManager {
    private final List<Order> orders; private final EmailSender email;
    private final PricingRules pricing; private final AuditLog audit;
    void place(Order o) { pricing.apply(o); email.confirm(o); audit.log(o); orders.add(o); }
    void refund(Order o, Money m) { /* pricing + email + audit + ledger ... */ }
    void monthlyReport(YearMonth m) { /* orders + audit ... */ }
}

// AFTER: cohesive concepts with interfaces at the seams
class OrderService {
    private final Pricer pricer; private final Notifier notifier;
    void place(Order o) { pricer.apply(o); notifier.confirmed(o); }
}
```

**Listing 1.** Conceptual. Same operations, but each extracted class now has one reason to change and testable seams.

> [!warning] "Split by Service/Repository layers and the god is gone" is false
> Technical layering re-creates one vertical god per layer, each still entangled with every domain concept. The unit of extraction is the **domain concept with its data** — not the architectural role. A slim `OrderService` that still owns pricing, notification, audit, and reporting is the same god after a diet ([[What is an antipattern]]).

> [!tip] Interview answer
> A god object is where every feature's state and logic meet — maximal coupling, no cohesion, one file every change must visit. I refactor incrementally: characterization tests first, then a method-to-field usage map, then extract by domain concept — data travels with its behavior — interfaces at the seams, and the god shrinks into a temporary facade I retire call by call.
