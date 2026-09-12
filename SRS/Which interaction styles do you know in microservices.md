<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/CommunicationStyles #DistributedSystems/Communication #SRS

# Which interaction styles do you know in microservices

> [!abstract] Short answer
> Microservice interaction styles differ on two axes: synchronism (does the caller block for the result?) and the number of parties per exchange (one-to-one or one-to-many). Richardson's catalog: one-to-one — request/response (sync RPI) and asynchronous request/response or notification (one-way); one-to-many — publish/subscribe and publish/async-responses. Choosing a style per use case is an architecture decision, not a framework accident.

## The styles, mapped to consequences

Request/response RPI: caller blocks; simplest to write and reason about; couples availability temporally ([[What is the remote procedure invocation pattern between microservices]]). Asynchronous request/response: caller sends and continues; the reply arrives on its own channel later (correlation id matches it up) — latency-tolerant workflows, but reply bookkeeping is on you. One-way notification: fire an event or command and do not care who acts — the basis of choreography; consumers must be idempotent because delivery is at-least-once ([[What is the Messaging Gateway pattern]] shows the transport shape; [[What is the Event Message pattern]] defines the payload discipline). Publish/subscribe: one event, many independent consumers — the integration backbone for fan-out and read models ([[What is a projection in CQRS and event sourcing]] is a classic subscriber). Publish/async-responses: request for interest from several services, replies collected asynchronously — a scouting pattern for aggregations.

```d2
direction: right
caller: "Caller" {style.fill: "#eceff1"}
a: "Request/response
blocks" {style.fill: "#e3f2fd"}
b: "Async request/response
reply later" {style.fill: "#e3f2fd"}
c: "One-way notification
no reply" {style.fill: "#fff3e0"}
d: "Publish/subscribe
many consumers" {style.fill: "#e8f5e9"}
caller -> a
caller -> b
caller -> c
caller -> d
```

**Fig. 1.** Same caller, four contracts: the choice sets the caller's blocking, failure and bookkeeping model.

## How to choose — and the default ladder

The decision inputs are: does the caller need the answer to proceed (sync) or can work continue (async)? how many parties care? what failure semantics are acceptable? The pragmatic ladder: reach for RPI when the caller genuinely needs the answer now (auth checks, pricing lookups); one-way events when the fact matters more than any single reaction (OrderPaid feeds inventory, analytics and loyalty at once); async request/response when the work is slow but the answer is required (report generation). Two cross-cutting rules hold for every style: transport redelivery makes at-least-once the default assumption, so dedupe by id ([[What is idempotency in HTTP and in messaging]]); and a mesh or chassis can move resilience policy out of the callers ([[What is the microservice chassis pattern]] for the library form, [[How would you explain the service mesh pattern]] for the proxy form) — but it cannot make an unsafe operation idempotent. The asynchronous, event-carrying side of that catalog is [[What is the messaging communication style between microservices]].

> [!tip] Interview answer
> I classify interactions on two axes — blocking vs async, one-to-one vs one-to-many. Sync RPI for "need the answer now", async request/response for slow-but-required work, one-way events and pub/sub for facts many parties react to. The style determines failure handling: sync needs timeouts and breakers, async needs idempotent consumers and correlation bookkeeping. Default to async at the edges — pure-sync fleets are distributed monoliths.
