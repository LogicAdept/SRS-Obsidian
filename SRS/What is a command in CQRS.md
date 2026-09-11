<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/CQRS #SRS

# What is a command in CQRS

> [!abstract] Short answer
> A command in CQRS is an imperative, named request to change state — CreateOrder, CancelSubscription, TransferFunds. It is expressed in the language of the domain's intent, carries the data needed to execute it, is validated against invariants by the write side, and returns nothing about the new state. Its declarative twin is the query; its effect twin is the event ([[What is the difference between a command and an event]]).

## Anatomy of a command

Three properties make a message a command rather than a generic DTO. Intent: the name is a verb phrase from the ubiquitous language — `CancelOrder`, not `UpdateOrderStatusFlag` — so the business rule it triggers is visible at the call site. Direction and expectation: a command is sent to exactly one destination (the handler that owns the invariant) with the expectation that it will be executed or rejected — an optimistic expectation, not a guarantee. Shape: identity of the target aggregate plus minimal parameters (`CancelOrder(orderId, reason)`); timestamps, actor identity and correlation ids ride along as metadata for audit ([[What is the audit logging pattern in microservices]]), not as part of the domain payload.

```d2
direction: right
sender: "Sender" {style.fill: "#eceff1"}
cmd: "CancelOrder(orderId, reason)" {style.fill: "#fff3e0"}
handler: "Command handler
validates invariants" {style.fill: "#e8f5e9"}
agg: "Aggregate
Order #7 -> CANCELLED" {style.fill: "#f3e5f5"}
ev: "OrderCancelled event" {shape: cylinder; style.fill: "#fffde7"}
sender -> cmd -> handler -> agg -> ev
```

**Fig. 1.** A command is an instruction: one sender, one handler, one target aggregate; the event it triggers is the record of what actually happened.

## Command versus event versus query

The command says "do this" — it may be refused; the event says "this happened" — it is a fact no one can refuse ([[Should commands and events be immutable]] covers why events are immutable records). The query says "tell me" — it must not change observable state. Mixing these concerns is the smell CQRS removes: a `GetOrderAndRecalculateTotals` method that both returns data and mutates a cache forces every caller to understand side effects. In transports, commands usually travel over point-to-point channels (RPC, command queue) because they need exactly one consumer; events travel over publish-subscribe channels because many parties care ([[Which interaction styles do you know in microservices]] contrasts the transport styles; [[What is a command handler in CQRS]] shows the receiving side).

> [!warning] A command has no authority over what happened
> The sender states intent; the handler decides. If the invariant fails — credit limit exceeded, order already shipped — the command is rejected, and the rejection itself is typically delivered as a reply or failure event. Code that assumes a command "succeeded" because it was accepted onto a queue has reinvented the phantom-write problem the outbox pattern exists to solve ([[How does an aggregate persist and publish events without a distributed transaction]]).

> [!tip] Interview answer
> A command is a named, imperative request to change state — CreateOrder, CancelOrder — written in the domain's language, addressed to exactly one handler that validates invariants and either executes or rejects it. It returns no result; what actually happened is published afterwards as immutable events. That intent/fact split is the point: commands are refused if invariants fail, events never are.
