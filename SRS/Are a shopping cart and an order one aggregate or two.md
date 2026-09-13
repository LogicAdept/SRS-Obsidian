<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# Are a shopping cart and an order one aggregate or two?

> [!abstract] Short answer
> Two aggregates - often two bounded contexts - because their lifecycles, invariants, and consistency needs are different. The cart is a short-lived, high-churn workspace: many concurrent edits, availability matters more than precision, and prices may be stale because nothing is contractual yet. The order is a frozen financial-legal snapshot: totals must always equal line sums, prices are fixed at the moment of purchase, and mutation rules tighten to nearly read-only. Checkout is the boundary: the cart's contents are re-priced and mapped into a new Order aggregate in its own transaction, and an `OrderPlaced` domain event announces the fact. The general rule the case teaches: a lifecycle change plus an invariant change marks an aggregate boundary.

## Reading the two objects by their invariants

Force them into one aggregate and every edit pays the price of rules it does not have. The cart's working set: add, remove, change quantity, several sessions sharing one cart, no invariant stronger than "quantities are positive". The order's working set: line sums equal the header total, the captured unit price never changes even if the catalog does, status transitions are one-way. If one aggregate serves both, then every quantity tweak bumps the optimistic-lock version of an object that also carries financial truth - concurrent shopping sessions fail each other's transactions for no business reason - and every cart mutation must pass order-grade validation that means nothing pre-checkout. Split them and each gets its natural concurrency story: the cart never blocks anyone, the order is contested only by the processes that legitimately touch it ([[How do you choose aggregate boundaries]] is the rulebook this case exercises).

```d2
direction: right
cart: "Cart aggregate
mutable, reprices,
staleness tolerated" {style.fill: "#fff3e0"}
co: "checkout
re-price against catalog\nmap into snapshot" {style.fill: "#ffe0b2"}
order: "Order aggregate
frozen prices,
strict invariants" {style.fill: "#e8f5e9"}
ev: "OrderPlaced
published after commit" {style.fill: "#fffde7"}
cat: "Catalog
prices move freely" {style.fill: "#f3e5f5"}
cart -> co: "contents"
cat -> co: "current prices"
co -> order: "one tx, one aggregate"
order -> ev
```

**Fig. 1.** Checkout is the boundary: the cart contributes contents, the catalog contributes the authoritative prices, and the order freezes both into a snapshot.

## The transition and what crosses it

Checkout does four things, and only one of them is the order transaction. It re-prices the cart against the catalog - the moment where staleness is resolved, because from here the numbers are contractual. It maps cart items into order lines as frozen snapshots - value objects carrying the unit price captured now, not a live reference to a row that will change tomorrow ([[What is a value object and why should you use one]] is why the snapshot shape matters). It commits the new Order aggregate - one transaction, one aggregate, version stamped. It publishes `OrderPlaced` after that commit (outbox in real systems), and the cart's own cleanup - emptying or deleting it - happens in its own later transaction: eventually consistent, and safe, because the cart guards no financial truth that anyone reads after checkout ([[Why should one transaction update only one aggregate]] and [[What is a domain event in DDD]] are the two rules doing the work). Whether this is two aggregates in one module or two full bounded contexts is a team-and-data question: if checkout, payment, and order history belong to different teams and stores, the contexts split as well ([[What is the difference between a bounded context and a subdomain]]); in a small monolith, two aggregates suffice.

```java
// Verified on JDK 21.0.12.1 (scripts/empirics/ddd/D16):
// cart total at add time:   4500
// cart reprices with catalog: 5200            <- catalog moved under the cart
// order frozen at checkout:   5200            <- prices captured at the boundary
// after further price moves:  order=5200, cart would show 5900
// mutation rejected: order is PLACED - placed orders do not mutate
// OrderPlaced events published: 1
```

**Listing 1.** The two halves of the case: the cart follows the catalog because it guards nothing, the order ignores the catalog because it guards a contract.

> [!warning] The reuse trap
> The tempting shortcut - one `CartOrder` class and table serving both lifecycles - fails exactly at the transition: status booleans accumulate, validation becomes "if placed then stricter", and the strict invariants leak into every read path that merely wanted a shopping list. The mirror-image mistake is transactional overreach at checkout: wrapping cart mutation, order creation, and catalog reads in one big transaction re-couples the aggregates the boundary just separated. One aggregate per transaction - the cart's retirement is not the order's problem. The same reasoning repeats across domains: draft versus published, session versus invoice, quote versus policy.

> [!tip] Interview answer
> Two aggregates, and at scale two contexts. The cart optimizes for availability and churn - stale prices are fine because nothing is contractual; the order is a frozen financial snapshot - line sums, captured prices, one-way transitions. Checkout is the boundary: re-price against the catalog, map items into value-object snapshots, commit the new order aggregate in one transaction, publish OrderPlaced, and let the cart clean up in its own transaction. One class serving both lifecycles is the classic modeling bug - lifecycle change plus invariant change marks the boundary.

