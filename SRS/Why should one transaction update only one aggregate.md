<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# Why should one transaction update only one aggregate?

> [!abstract] Short answer
> Because the aggregate is the unit of transactional consistency: its invariants are guaranteed only if everything inside one boundary commits together. Touching a second aggregate in the same transaction couples their consistency, their locks, and their failure modes - and quietly voids the boundary design. The replacement for the second write is a domain event, published after commit, with the reacting aggregate updated in its own transaction: eventually consistent between aggregates, strictly consistent inside each.

## What the rule protects

Inside one aggregate, the invariant story is clean: commit means valid, every time. The moment a transaction spans two aggregates, three things break at once. Consistency reasoning: aggregate B's invariants are now checked under aggregate A's concurrency - two users touching unrelated parts of A can serialize through B and fail each other. Contention: optimistic locking on the shared transaction scope turns unrelated operations into retry storms - the large-aggregate failure mode, rebuilt across the boundary. And coupling: A and B can no longer deploy, scale, or even be stored independently, since one transaction binds them. The rule is a rule of thumb, not physics - but it is what makes [[How do you choose aggregate boundaries]] mean anything; without it, the boundary dissolves under the first convenient two-object write.

```java
// Application service: ONE aggregate modified per transaction.
Tx tx = new Tx();
order.place();                                  // Order aggregate only
System.out.println("inside tx, events visible? " + tx.committed);   // false
tx.commit();
order.drainEvents().forEach(broker::add);       // events become visible after commit

// The reaction is its own transaction on a different aggregate.
Tx tx2 = new Tx();
stats.on((OrderPlaced) broker.poll());          // CustomerStats updated eventually
tx2.commit();
System.out.println("customer stats ordersSeen = " + stats.ordersSeen);
```

**Listing 1.** Verified on JDK 21.0.12.1: the placing transaction touches only the Order aggregate; its event surfaces after commit, and the customer statistics update in a second transaction - consistent per aggregate, eventual between them.

```d2
direction: right
tx1: "Transaction 1\nOrder aggregate only" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
evt: "Domain event\npublished after commit" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
tx2: "Transaction 2\nCustomerStats aggregate" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
tx1 -> evt: "recorded by aggregate,\ndispatched post-commit"
evt -> tx2: "handler reacts in\nits own tx"
```

**Fig. 1.** Two transactions, one event between them: each aggregate stays atomically consistent, and the bridge between them is a fact, not a shared lock.

## Living with eventual consistency

The honest cost: after placing the order, the customer's statistics lag - a reader may see the order before the projection catches up. Whether that is acceptable is a business question, and the rule forces it to be asked per case instead of answered "transaction" by default. When a process genuinely spans several aggregates with intermediate rules - flight booking reserving seats, then payment, then confirmation - the multi-step consistency wants an explicit coordinator: a saga with its compensations ([[What is a saga and how would you explain one with a real-world example]], [[How would you orchestrate communication between multiple services]]). And when the event must survive a crash between the database commit and the broker publish, the outbox pattern closes the gap ([[How would you explain the transactional outbox pattern]]).

> [!warning] The rule is not enforced by tooling
> Nothing stops `@Transactional` from wrapping three aggregate writes - the compiler is fine with it. The evidence arrives later as contention and "spooky" retries that nobody connects to the transaction layout. The one case that justifies breaking the rule is a genuine same-instant user expectation of consistency across aggregates - and even then the first question remains whether the boundary was drawn wrong ([[What is a domain event in DDD]] records the fact that bridges the gap).

> [!tip] Interview answer
> The aggregate is the transactional consistency unit, so one transaction per aggregate keeps invariants and locks local - no cross-aggregate contention, no coupled failures. Anything cross-aggregate becomes a domain event published after commit and handled in its own transaction, eventually consistent. Multi-step processes that need it use sagas; true instant cross-aggregate consistency is a boundary-design smell.

