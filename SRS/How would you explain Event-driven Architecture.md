<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/EventDriven #SRS

# How would you explain Event-driven Architecture

> [!abstract] Short answer
> Event-driven architecture (EDA) structures a system around the production, detection, and reaction to events: components emit facts about state changes without knowing who consumes them. It gives strong decoupling, fault tolerance, and scalability, at the price of eventual consistency, harder testing, and flow that is harder to trace. The two classical topologies are a central mediator that orchestrates event workflow and a broker where components react to each other's events directly.

## The core mechanism

An event is a record that something significant happened - "order placed", "door opened". Emitters publish events to event channels; consumers subscribe and react. The emitter does not know the consequences of its cause, which is why EDA is described as extremely loosely coupled and well distributed: the door does not know the alarm system will log its opening. Events typically carry light payloads - often just identifiers - and consumers fetch or infer the rest. Within a bounded context these are domain events, the vocabulary shared with [[How would you explain the event sourcing pattern]] and [[What is the difference between a command and an event]].

```d2
direction: right
pub: "Emitter\npublishes fact" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
med: "Mediator topology\norchestrator controls\nthe workflow" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
brk: "Broker topology\nno orchestrator,\ncomponents react" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
s1: "Step consumers\ncontrolled sequence" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
f1: "Reactive consumers\nchain of reactions" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
pub -> med
pub -> brk
med -> s1: "higher control,\nerror handling"
brk -> f1: "higher performance,\nscalability"
```

**Fig. 1.** The two topologies differ in who owns the flow: a mediator orchestrates each step, while a broker lets consumers trigger each other; hybrids combine them.

Event processing itself comes in styles - simple event processing (a reaction to one event), event stream processing (reacting to streams in near real time), and complex event processing (patterns across many events). Kafka pipelines, webhook fan-outs, and Spring's `ApplicationEventPublisher` with `@EventListener` are all small-letter implementations of the same shape.

```java
// Conceptual Spring: in-process event channel
record OrderPlaced(Long orderId, String customer) {}

publisher.publishEvent(new OrderPlaced(id, customer));

@EventListener
void on(OrderPlaced e) {
    mailer.sendConfirmation(e.orderId());   // emitter does not know this exists
}
```

**Listing 1.** The emitter only publishes the fact; adding another listener never changes the emitter's code, which is the decoupling EDA buys.

## What it costs

The event does not know its consumers, so the overall flow lives nowhere in particular: tracing a failure means following reactions across components, and tests need infrastructure to observe asynchronous behavior. Consistency becomes eventual - after "order placed", the shipping service may not know yet. Schema evolution becomes an interface problem: events need versioning and backward-compatible formats so consumers can upgrade independently.

> [!warning] EDA is not a replacement for request-reply
> Asking "what is the balance" is a question expecting an answer, not a fact announcing itself. Event-driven design fits announcing facts and reacting to them; commands and synchronous queries keep their place, which is why hybrid designs dominate. Also "broker topology is always better" is false - without an orchestrator, long workflows lose error handling and monitoring discipline.

> [!tip] Interview answer
> EDA organizes the system around events - immutable facts published by emitters to channels and consumed by subscribers who react. The emitter never knows the consumers, so coupling drops dramatically and scaling per component is natural; the classical split is mediator topology, where an orchestrator controls the workflow, versus broker topology, where components react to each other. The price is eventual consistency, asynchronous testing, and distributed tracing of flows. I reach for it when components genuinely react to business facts, as in [[What is CQRS]] write-side integration or [[What is the Event-Driven Consumer pattern]] endpoints, not as a religion for every interaction - and cross-service fan-out still needs the data-ownership discipline of [[How would you explain the database per service pattern]].
