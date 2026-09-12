<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/CommunicationStyles #DistributedSystems #Messaging #SRS

# How would you orchestrate communication between multiple services

> [!abstract] Short answer
> When one use case spans several services, there are two coordination styles: orchestration — a central orchestrator invokes the participating services in order and reacts to failures by running compensations; choreography — there is no coordinator, each service performs its step and publishes events, and the next services react to those events. Both are the coordination half of the saga pattern; messaging style underlies choreography, request/reply underlies orchestration.

## Orchestration: explicit flow, one place to read

An orchestrator (a dedicated saga class or process manager) holds the use case's state machine: call billing to reserve credit, call inventory to reserve stock, call shipping, and on any failure run the compensating actions of already-completed steps in reverse order ([[What is a saga and how would you explain one with a real-world example]] walks the full saga semantics). Benefits: the business flow is written in one inspectable place — add a step, see the step; participants stay dumb, they just answer commands. Costs: the orchestrator owns extra state and must be persisted/relied upon like any stateful component; it can accrete god-object gravity as flows grow; it adds one more hop to every step.

```d2
direction: right
orch: "Orchestrator
saga state machine" {style.fill: "#fff3e0"}
b: "Billing" {style.fill: "#e8f5e9"}
i: "Inventory" {style.fill: "#e8f5e9"}
s: "Shipping" {style.fill: "#e8f5e9"}
orch -> b: reserve credit
orch -> i: reserve stock
orch -> s: book shipping
s -> orch: done / failed
orch -> i: compensate (undo)
orch -> b: compensate (refund)
```

**Fig. 1.** The orchestrator drives each step and, on failure, runs compensations top-down in reverse.

## Choreography: implicit flow, maximal decoupling

In the choreographed version the first service publishes an event — OrderPlaced — and every subsequent service reacts and publishes its own outcome: billing emits CreditReserved, inventory listens and emits StockReserved, shipping listens and books. No one owns the whole picture; the flow is the composition of reactions. Benefits: loose coupling (a new participant subscribes without anyone editing the flow), no central bottleneck, natural fit for event-driven integration ([[What is the Messaging Gateway pattern]] and channel patterns carry the events). Costs: the flow is implicit — "who reacts to OrderPlaced?" has no single answer, so the process must be documented in tooling and tests; cyclic reactions are easy to create by accident; and failure semantics are subtler — compensation happens by reacting to failure events, and nobody is watching the whole. Operational danger: observing the system requires tracing across participants ([[What is the distributed tracing pattern in microservices]]). The asynchronous substrate both coordination styles ride on is [[What is the messaging communication style between microservices]].

> [!tip] Interview answer
> Orchestration puts a central coordinator in charge: it invokes each participating service, tracks the saga state and runs compensations on failure — explicit, inspectable, but one more stateful component. Choreography has no coordinator: services react to each other's events and the flow emerges from the subscriptions — maximally decoupled, but implicit and harder to see or debug. I orchestrate complex branching flows and choreograph simple stable ones.
