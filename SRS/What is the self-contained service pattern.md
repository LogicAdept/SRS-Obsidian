<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/ServiceBoundaries #SRS

# What is the self-contained service pattern

> [!abstract] Short answer
> A self-contained service answers a synchronous request without waiting for any other service's response. The trick: merge the needed functionality into the service, serve reads from a CQRS replica of other services' data, and settle any cross-service writes asynchronously with a saga. Availability of a synchronous operation is the product of the availabilities of everything it calls - so the fewer live calls, the higher the product.

## The availability arithmetic behind it

If handling a request synchronously touches three services at 99.5% each, the operation's availability is 0.995 cubed - about 98.5%; every added hop multiplies another failure chance into the chain. The pattern attacks that multiplication from three directions. First, re-examine the boundary: if the collaborator exists only to serve this service's request path, fold it in as a module - the classic example is merging Order Service and Restaurant Service when they are always needed together. Second, reads: keep a replica of the data you would otherwise fetch - the CQRS move - so validation and pricing read a local materialized view instead of calling out ([[What is CQRS]] is the full pattern; the query-side counterpart of composition lives in [[What is the API composition pattern in microservices]]). Third, writes: instead of a synchronous chain "reserve credit, then create order", initiate a saga - do the local step, publish an event, let the rest converge asynchronously ([[What is a saga and how would you explain one with a real-world example]] has the compensation mechanics).

```d2
direction: right
client: "Client" {style.fill: "#eceff1"}
osvc: "Order Service
self-contained" {style.fill: "#e8f5e9"}
repl: "Restaurant replica
CQRS view" {style.fill: "#fff3e0"}
rsvc: "Restaurant Service" {style.fill: "#eceff1"}
saga: "CreateOrder saga
async" {style.fill: "#ffe0b2"}
csvc: "Customer Service" {style.fill: "#eceff1"}
client -> osvc: POST /orders
osvc -> repl: local read, no call
repl -> rsvc: async feed
osvc -> saga: start, return PENDING
saga -> csvc: reserve credit (async)
```

**Fig. 1.** The request path touches only the Order Service: a local replica answers reads, a saga carries the cross-service write after the response.

The worked example: createOrder() validates and prices the order against a CQRS replica of restaurant data, then starts the create-order saga - the synchronous window never leaves the service. The caller gets an acknowledged PENDING order instead of a chain of live calls.

## What it costs

The pattern trades distributed complexity for local complexity. Replicas need event feeds, projection code and staleness monitoring; sagas need compensations and make the API asynchronous by nature - the caller must understand that an accepted request is not yet a completed business transaction, which changes the client contract ([[What is eventual consistency]] is the consistency posture this imposes). The service also grows: functionality that was a separate service is now a module inside this one, so the pattern pushes against the "small services" aesthetic - and that is the point: service size serves team autonomy and availability, not a count in a dashboard. Ownership stays clean when the folded-in module is one the service effectively owned anyway.

> [!warning] Not every dependency can go async
> The pattern is a match for flows where the caller can tolerate an eventually-consistent outcome - order placement, account creation. It is a mismatch where the response must contain a fresh, authoritative answer from another service in the same round trip: card authorization at checkout time, an OTP check, an inventory hard reservation with immediate confirmation. Forcing those into "start a saga and return PENDING" changes the product, not just the architecture. The second trap: replicas silently going stale - a replica without an age/heartbeat check turns "self-contained" into "self-deceived".

> [!tip] Interview answer
> A self-contained service completes synchronous requests without live cross-service calls: it merges needed functionality, reads from a CQRS replica of other services' data, and uses sagas for cross-service writes. The reason is availability math - a synchronous chain's uptime is the product of each hop's uptime. The price is replica staleness and async APIs, so I apply it where eventual consistency is an acceptable contract.
