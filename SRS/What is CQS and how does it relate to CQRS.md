<!--
reps: 0
priority: 0
-->
#Methodologies/Principles #SRS

# What is CQS and how does it relate to CQRS?

> [!abstract] Short answer
> CQS - Command-Query Separation, stated by Bertrand Meyer in Object-Oriented Software Construction - is a method-level principle: a method should either do something (a command, which changes state) or answer something (a query, which returns data), never both. The rule of thumb: "asking a question should not change the answer". CQRS - Command and Query Responsibility Segregation, coined by Greg Young - takes that split to the architecture level: separate models (sometimes separate stores) for writes and reads, synchronized by events. CQS is the discipline inside objects; CQRS is a system pattern built on the same instinct.

## The principle and its payoff

A command changes observable state and returns nothing (or at most thin status); a query returns a value and leaves state untouched. The payoff is reasoning: query results can be cached, retried, reordered, or repeated without consequences, and command effects can be stated and tested once. Mixed methods poison that: `pop()` both mutates and answers, so you cannot ask "what is next" without destroying it, and callers cache or retry at their peril. Meyer's assertion connection matters for interviews: postconditions on commands and invariant-friendly queries are what make a class auditable - the pair is the unit of Design by Contract thinking.

```java
interface Account {
    void debit(Money amount);      // command: state change, no return
    Money balance();               // query: no side effects
    // CQS violation style: Money debitAndReturnNewBalance();
}
```

**Listing 1.** Conceptual. Splitting debit and balance lets you call `balance()` freely - cache it, log it, retry it - with zero risk of changing the account.

## The step up to CQRS

CQRS scales the same separation to models: the write side holds aggregates and enforces invariants on commands; the read side holds denormalized projections shaped for queries. They sync asynchronously - the write side publishes events, projections update, reads become eventually consistent. Microsoft's pattern guidance describes exactly this: separate stores let each side "scale to match the load" and pick fitting storage, at the price of eventual consistency and synchronization work (usually via events and an outbox). Where CQS stays strict, CQRS deliberately loosens CQS at the boundary - a command handler may return an ID - because the split's value is architectural isolation, not method-level purity ([[What is CQRS]], [[How would you explain the event sourcing pattern]]).

> [!warning] "CQS violation!" and "CQRS everywhere" are both reflexes
> `pop()`-style mixes are sometimes right: a `Queue.poll` that returns null-or-element IS the API, and Meyer's own exception list starts there - treat the rule as a default, not a law. And CQRS is not a default architecture: it buys scale and independent evolution of reads and writes, and charges eventual consistency, duplicate models, and event infrastructure. For a CRUD service the tax is pure loss - Microsoft's own guidance says apply it to collaborative, high-contention domains, not everywhere ([[What is a projection in CQRS and event sourcing]]).

> [!tip] Interview answer
> CQS is Meyer's method rule: commands change state and return void, queries answer and stay side-effect free - so queries are safely repeatable and commands are auditable. CQRS is Greg Young's architectural escalation of the same idea: separate write model with invariants and read projections, synced by events, eventually consistent. I mention pop() as the accepted exception and that CQRS buys scale at the cost of eventual consistency - so it is a deliberate choice, not a default.
