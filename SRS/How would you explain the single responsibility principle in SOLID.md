<!--
reps: 0
priority: 0
-->
#Methodologies/Principles/SOLID #SRS

# How would you explain the single responsibility principle in SOLID?

> [!abstract] Short answer
> SRP says a module should be responsible to one, and only one, actor - Martin's 2014 restatement of the classic "one, and only one, reason to change". Responsibility here means "for whom does this code change": if the same class holds reporting logic that the CFO drives and calculation logic that the CTO drives, it has two reasons to change and violates SRP, even if both features look related. The principle is about cohesion around stakeholders, not about "a class should do one thing" in the vague sense.

## Why "reason to change" is the operational test

Two actors' requirements change independently and often in opposite directions. A class coupling their logic guarantees that a change for one actor risks the other's behavior - every merge into that class is a negotiation. That is why the SRP question is "who asks this code to change?", not "what does this code do?": a `TradeService` doing pricing, persistence, and audit email serves three actors, and its size is just a symptom. Martin's original formulation in the 2000s paper - "a class should have only one reason to change" - and the 2014 actor-based restatement say the same thing at different altitudes ([[What are coupling and cohesion and how do they affect maintainability]]).

```java
// Violation: three actors share one class
class TradeService {
    Money price(Trade t) { ... }              // trader's rules change
    Trade save(Trade t) { ... }               // DBA's schema changes
    void auditEmail(Trade t) { ... }          // compliance format changes
}

// SRP applied: one module per actor's concern
class TradePricer { Money price(Trade t) { ... } }
class TradeRepository { Trade save(Trade t) { ... } }
class TradeAuditor { void auditEmail(Trade t) { ... } }
```

**Listing 1.** Conceptual. Splitting by actor-concern means the compliance email format can change without retesting the pricing engine.

## The boundaries of the principle

SRP does not demand one-method classes, and it does not forbid a class from doing several things for the SAME actor - a `TradePricer` with pricing rules, fees, and rounding is still one responsibility if only the trading desk drives its changes. It also does not decide granularity for you: extract when different actors actually collide on the class, not preemptively per method. The practical smell is the class name with "Manager", "Service", or "Helper" holding logic for multiple stakeholders - plus a git history where unrelated features keep editing the same file ([[What can violating SOLID principles lead to]]).

> [!warning] "Single responsibility = one method" and "small classes are SRP" are both wrong
> A 200-line class whose changes all come from one actor is SRP-clean; a 20-line class mixing two actors' concerns is not. Chasing microscopic classes produces shotgun-surgery of a different kind: every behavior change edits six files. The unit of the principle is the ACTOR-reason axis - responsibility - and that takes domain knowledge to see, which is why mechanical "small = good" refactors often make coupling worse instead of better ([[How would you explain the SOLID design principles as a set]]).

> [!tip] Interview answer
> SRP means a module answers to exactly one actor: one group of stakeholders whose requests cause it to change. I test it by asking who wants this code changed - if two unrelated parties can both demand edits, the class merges their risks and should split along that line. It is cohesion measured by stakeholders, not by method count.
