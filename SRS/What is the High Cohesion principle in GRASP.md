<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #SRS

# What is the High Cohesion principle in GRASP

> [!abstract] Short answer
> High Cohesion is an evaluative GRASP principle: keep the responsibilities of each class strongly related and focused on one topic. Low cohesion - a class carrying many unrelated jobs - is hard to comprehend, reuse, maintain, and change as a whole.

## Reading cohesion in a design

High cohesion means the responsibilities of a set of elements are strongly related and focused on a rather specific topic. The failure mode has recognizable symptoms: a class that parses input, enforces business rules, and writes to the database; grab-bag names like Manager, Helper, or Util; methods that each touch a different, disjoint subset of the fields. Subsystems whose elements have low cohesion end up hard to comprehend, reuse, maintain, and change.

```java
// Low cohesion: one class, three unrelated jobs
class Register {
    void paintScreen(Screen screen) { /* UI rendering */ }

    Money priceSale(Sale sale) { /* domain pricing rules */ }

    void saveSale(Sale sale) { /* JDBC persistence */ }
}
```

**Listing 1.** Each method belongs to a different concern; a change to pricing can force re-reading UI and persistence code, and none of the three jobs is reusable without dragging the other two along.

```java
// Higher cohesion: one job per class
class Register {                 // UI concern only
    void paintScreen(Screen screen) { /* UI rendering */ }
}

class PricingPolicy {            // domain pricing only
    Money priceSale(Sale sale) { /* domain pricing rules */ }
}

class JdbcSaleRepository {       // persistence only
    void saveSale(Sale sale) { /* JDBC persistence */ }
}
```

**Listing 2.** The split gives each class a single focused topic, which is what makes each of them understandable and reusable on its own.

```d2
direction: right
blob: "Low cohesion\nRegister = UI + pricing + JDBC" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
split: "Split by responsibility" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ui: "Register\nUI" {
  width: 160
  height: 70
  style.fill: "#e8f5e9"
}
price: "PricingPolicy\ndomain" {
  width: 170
  height: 70
  style.fill: "#e8f5e9"
}
repo: "JdbcSaleRepository\npersistence" {
  width: 210
  height: 70
  style.fill: "#e8f5e9"
}
blob -> split
split -> ui
split -> price
split -> repo
```

**Fig. 1.** Breaking one low-cohesion class along responsibility lines raises the cohesion of every resulting class - which is the payoff the principle asks you to look for.

## Cohesion and coupling travel together

High cohesion is generally used in support of Low Coupling - and both are evaluative: they judge designs made with the other seven principles rather than telling you where to put a method. The measured relationship between the two qualities and maintainability lives in [[What are coupling and cohesion and how do they affect maintainability]]. Breaking a blob along responsibility lines also serves [[What is the Low Coupling principle in GRASP]], because focused classes depend on fewer collaborators.

> [!warning] Cohesion is not size, and splitting can overshoot
> A small class can still be incohesive - two unrelated one-line methods - while a large arithmetic class can be perfectly cohesive. Splitting along arbitrary lines creates fragmented logic that jumps between classes and often raises coupling instead of lowering it. Also keep the question separate from [[How would you explain the single responsibility principle in SOLID]]: SRP counts reasons to change, while cohesion counts how related the responsibilities are; one class can pass one test and fail the other.

> [!tip] Interview answer
> High Cohesion asks me to keep each class focused on strongly related responsibilities and to treat scattered jobs inside one class as a design smell. It is an evaluative principle - I use it, together with Low Coupling, to judge the assignments Expert and Creator propose. When a class mixes UI, domain, and persistence, I split it by responsibility; when a split would just fragment related logic, I keep it together.
