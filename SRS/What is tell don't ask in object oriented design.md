<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Methodologies/Principles #SRS

# What is tell don't ask in object oriented design?

> [!abstract] Short answer
> A design heuristic from *The Pragmatic Programmer* (Hunt & Thomas, 2000): **tell** an object what to do instead of **asking** it for its state and deciding for it outside. `if (account.getBalance() >= amount) { account.setBalance(...); }` relocates the account's business rule into the caller; `account.withdraw(amount)` keeps the rule where the state lives. The point of message passing is exactly this: behavior beside data ([[What is message passing in object oriented programming]]).

## The ask-smell

Asking produces three recognizable costs. The decision logic (`balance >= amount`) is **duplicated** in every client that needs the same judgment, and soon they disagree. The object's **invariants** are unenforced — anyone who can read the balance can also write it, which is how anemic models happen ([[What is an anemic domain model and is it useful]]). And the client exhibits **feature envy**: it manipulates someone else's data more than its own, the textbook extract-class signal. Asking also walks hand in hand with train wrecks — the more a client asks, the deeper it reaches ([[What is the Law of Demeter]]).

## The tell-shape

Telling inverts the direction: the client states intent, the object decides *how* from its own state. Public surface shrinks to operations; fields go private; invariants get enforced in one place. The method name becomes vocabulary: `withdraw` versus a balance dance. This is not decoration — it is the same change-locality argument as encapsulation itself ([[What is encapsulation]]): rules move with the data they guard, so changing the overdraft policy touches one class instead of every caller.

## Where asking is legitimate

Boundaries need data: DTOs over the wire, query results for reports, records for persistence, form objects for binding — objects whose whole job is to carry values have nothing to tell. The smell is not the presence of getters but **decision logic that migrated out** of domain objects. Command–query separation keeps the vocabulary clean: commands change state and are told, queries return data and are asked — the trouble starts when a query's result feeds a decision the object itself should have made ([[What is CQS and how does it relate to CQRS]]).

```d2
direction: down
ask: "ASK\nstate travels out\ndecision lives in the client" {
  width: 260
  height: 72
  style.fill: "#ffebee"
}
tell: "TELL\nintent travels in\ndecision lives with the data" {
  width: 260
  height: 72
  style.fill: "#e8f5e9"
}
inv: "invariants enforced in one place" {
  width: 280
  height: 48
  style.fill: "#fff8e1"
}
tell -> inv
ask -> inv: "impossible: N clients, N copies"
```

**Fig. 1.** Telling centralizes the decision; asking replicates it wherever the state was read.

```java
// ASK: the overdraft rule is now copy-pasted across the codebase
if (account.getBalance() >= amount) {
    account.setBalance(account.getBalance() - amount);
}

// TELL: the rule and the state live together
account.withdraw(amount);   // or throws InsufficientFundsException
```

**Listing 1.** Conceptual. The same operation under both shapes: the ask version is the anemic-model seed.

> [!warning] "Tell don't ask means no getters ever" is false
> Reporting, persistence, and transport legitimately read state. The violation is **business logic outside the object**, not the existence of accessors — banning getters on DTOs is ceremony, and keeping domain rules in services is the actual disease ([[What is an anemic domain model and is it useful]]).

> [!tip] Interview answer
> Instead of asking an object for its state and branching outside, I hand it the operation: not `if (cart.total() > limit)` but `cart.qualifiesForDiscount()`. Rules stay in one place, invariants get enforced where the data lives, and clients shrink to intent. I still use getters at boundaries for transport and reporting — the heuristic targets domain logic, not data carriers.
