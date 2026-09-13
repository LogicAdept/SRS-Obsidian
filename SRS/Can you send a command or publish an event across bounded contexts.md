<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# Can you send a command or publish an event across bounded contexts?

> [!abstract] Short answer
> Both are possible, and the difference is coupling. A command is a request addressed to a specific receiving handler - sending one across a boundary means you know the other context, its API, and its availability, and it may reject you. An event is a published fact - "this happened here" - that other contexts subscribe to and translate into their own local commands. The general contrast between the two message kinds is in [[What is the difference between a command and an event in DDD]]. For integration between bounded contexts, publishing events is the default: it preserves each context's autonomy and lets consumers evolve independently; direct cross-context commands are acceptable for a deliberate, synchronous, request-driven relationship.

## What each one means across a boundary

Inside a bounded context, a command targets an aggregate handler and can be validated and refused; an event records something that already happened ([[What is the difference between a command and an event]]). Across the boundary the asymmetry matters more. If Sales sends `ReserveStockCommand` directly to Shipping, Sales now knows Shipping's contract, waits on its availability, and breaks when Shipping renames or repartitions - the two contexts are temporally coupled. If Sales instead publishes `OrderPlaced`, Shipping subscribes, decides that it means "reserve stock", and handles it with its own internal command to its own aggregate. Ownership of the decision moved to the consumer - that is the autonomy DDD boundaries are buying ([[What is the domain-specific boundary pattern in microservice design]]).

```d2
direction: right
sales: "Sales context" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
bus: "Integration events\n(published)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
ship: "Shipping context" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
bill: "Billing context" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
sales -> bus: "OrderPlaced"
bus -> ship: "translate ->\nReserveStock (local)"
bus -> bill: "translate ->\nOpenInvoice (local)"
```

**Fig. 1.** The event crosses the boundary; the commands stay local. Each consuming context translates the fact into its own operation.

## Mechanics that make it work

The publisher must announce the fact atomically with its own state change - write the event to an outbox in the same transaction, then relay it - or accept "database updated but nobody told" failures ([[How would you explain the transactional outbox pattern]]). Event delivery is at-least-once, so consumers handle duplicates idempotently. Contracts between contexts are the published event schemas; when a consumer's language differs from the publisher's, an anti-corruption translation keeps foreign vocabulary out of the local model. And some pairs genuinely want synchronous coupling - a checkout UI waiting for a payment decision - which is the legitimate case for a cross-context command/rpc-style call, chosen deliberately rather than by habit ([[What is a saga and how would you explain one with a real-world example]]).

> [!warning] "Events across contexts" does not mean "one shared event type everywhere"
> Publishing one canonical `OrderChanged` mega-event consumed by every service re-couples all contexts to a single schema and turns it into the enterprise model through the back door. Each context publishes its own events in its own language, and consumers translate - or subscribe to explicitly versioned integration contracts. Also, a published event is a fact: if consumers need the originator to do something, that is a command, and it belongs in the other context's API, not smuggled into the event payload.

> [!tip] Interview answer
> You can do both: commands are point-to-point requests to a known handler and can be rejected; events are broadcast facts other contexts react to. Across bounded contexts I default to publishing events and letting each consumer translate them into its own local commands - that keeps autonomy and loose coupling. I reserve direct cross-context commands for deliberate synchronous dependencies, and I make publishing atomic with an outbox.
