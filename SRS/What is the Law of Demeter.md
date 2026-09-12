<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Methodologies/Principles #SRS

# What is the Law of Demeter?

> [!abstract] Short answer
> A coupling guideline from Lieberherr and Holland (1989), nicknamed "only talk to your immediate friends": a method may call methods on **itself**, its **fields**, its **parameters**, and the **objects it creates** — not on objects reached *through* those friends. `order.getCustomer().getAddress().getCity()` is the classic violation — a **train wreck** — because it hard-codes the internal structure of two other objects into this one ([[What is encapsulation]]).

## The rule, precisely

The friend list per method `m` of class `C`: (1) `C` itself — `this` and statics of `C`; (2) `m`'s parameters; (3) `C`'s fields, including collection elements held in fields; (4) objects `m` creates. Everything else — return values of calls on friends, transitively — is off-limits for method calls. The point is not politeness but **structural coupling**: knowledge of the shape `a -> b -> c` spreads across the codebase, so reshaping `a`'s internals breaks every client that navigated them ([[What are coupling and cohesion and how do they affect maintainability]]).

## Why it works: change locality

Demeter violations are change amplifiers. If `Order` internally replaces `getCustomer().getAddress()` with a shipping snapshot, every client that chained through both getters breaks — the private refactor became a public API break. A class honoring the law exposes the *operation* instead: `order.shippingCity()`. Now the navigation lives once, inside `Order`, where the structure knowledge already is — the same change-locality argument that motivates encapsulation and rep invariants ([[What is a representation invariant and abstraction function]]).

## Costs and the pragmatic reading

Applied mechanically, the law manufactures wrapper methods and pass-through plumbing — critics joke that it "produces interfaces everywhere". The modern reading separates two cases. **Behavior-bearing graphs**: navigating into collaborators to invoke logic is the smell — tell the collaborator's owner what you need ([[What is tell don't ask in object oriented design]]). **Data carriers**: chaining over records, DTOs, builders, or streams is not the target; those are pipelines over values, not journeys through someone else's internals ([[Which principles help you write clean maintainable code]]).

```d2
direction: right
m: "OrderService.m()\nfriends: this, fields,\nparams, new objects" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
f: "order (field)" {
  width: 150
  height: 40
  style.fill: "#fff8e1"
}
x: "customer\nstranger" {
  width: 150
  height: 44
  style.fill: "#ffebee"
}
m -> f: "allowed"
f -> x: "NOT allowed\nthrough a friend"
m -> x: "only as a parameter"
```

**Fig. 1.** Calls on friends: allowed. Calls on strangers reached through friends: the violation.

```java
// ask-chain: OrderService knows Order -> Customer -> Address
String city = order.getCustomer().getAddress().getCity();

// Demeter shape: the navigation lives inside Order, where the structure belongs
String city = order.shippingCity();
```

**Listing 1.** Conceptual. The same value read two ways: the train wreck spreads structural knowledge; the exposed operation localizes it.

> [!warning] "Any method chain is a Demeter violation" is false
> Chains over immutable data carriers, builders, and streams are not the law's subject — the smell is **dispatching behavior** on an object reached through a collaborator's internals. `order.items().stream().filter(...)` is a data pipeline; `order.getCustomer().getAddress().getCity()` hides two other objects' structure inside this method. Judging by chain length instead of by who owns the behavior misses both cases ([[What is tell don't ask in object oriented design]]).

> [!tip] Interview answer
> A method may talk to itself, its fields, its parameters, and what it creates — not to strangers returned by those friends. When I see `order.getCustomer().getAddress().getCity()`, address navigation knowledge has leaked into the caller; I expose `order.shippingCity()` so the structure lives in one place. I don't apply it to data records or builder chains — the law targets behavior, not value pipelines.
