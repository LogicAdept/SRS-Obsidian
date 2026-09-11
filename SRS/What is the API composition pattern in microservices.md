<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices #Patterns/DistributedSystems #SRS

# What is the API composition pattern in microservices

> [!abstract] Short answer
> API composition is Richardson's query-side pattern for microservices: to answer a query spanning several services, a composer (often the API gateway or a BFF) calls each owning service and performs an in-memory join of the results. It is the simplest answer to "how do I query data scattered across services" — no query store of its own, just orchestration of existing APIs.

## The mechanism: fan out, join in memory, return

The pattern has three moving parts. A composer — gateway, BFF or a dedicated query service — knows which services own the pieces of the answer. It invokes them (in parallel when independent, sequentially when one call's output feeds another) and joins the responses in memory into the client's view shape. The join is real application logic: identity mapping, field stitching, filtering. This is the counterpart of database-per-service: when no single store holds the data, the query capability lives in composition ([[How would you explain the database per service pattern]] is the storage decision it compensates for; [[What is CQRS]] places it on the query side of the house).

```d2
direction: right
client: "Client" {style.fill: "#eceff1"}
comp: "API Composer
in-memory join" {style.fill: "#fff3e0"}
o: "Order service" {style.fill: "#e8f5e9"}
c: "Customer service" {style.fill: "#e8f5e9"}
p: "Product service" {style.fill: "#e8f5e9"}
client -> comp: GET order details
comp -> o: order 7
comp -> c: customer 3
comp -> p: skus
o -> comp
c -> comp
p -> comp
comp -> client: joined view
```

**Fig. 1.** The composer fans out to the owning services and stitches the answer in memory; no service sees the join.

```java
OrderDetails compose(int orderId) {
    OrderInfo o = orders.get();                      // remote call in a real system
    CustomerInfo c = customers.get();                // remote call
    List<String> titles = products.all().stream()    // remote call
            .map(ProductInfo::title).toList();
    return new OrderDetails(o.id(), o.status(), c.name(), titles);
}
```

**Listing 1.** Verified on JDK 21 (G03_ApiComposition in empirics): the composer joins three in-memory providers into `OrderDetails[orderId=7, status=PAID, customerName=Ada Lovelace, productTitles=[Keyboard, Mouse]]` — three logical remote calls, one client round trip (out/G03_ApiComposition.txt).

## Limits that force the heavier alternative

Latency: the client pays the composer's fan-out — parallel calls bound it by the slowest service, but every hop adds queueing and jitter; caching hot compositions softens this. In-memory joins: the pattern joins result sets, not databases — a query like "top 100 customers by open-order value" means pulling large intermediate datasets into one process and joining there; Richardson names exactly this as the disqualifier, pushing to CQRS-style query stores for such cases. Availability: the composition is as available as its weakest dependency — resilience policy per call ([[How would you explain Circuit Breaker]]) and a decided fallback shape (partial answer with a degraded flag vs. hard failure) are part of the design. Composition and read models are complementary, not rival: per-entity views compose fine; cross-entity analytics belongs in event-fed read models ([[What is a projection in CQRS and event sourcing]]).

> [!warning] Sequential composition multiplies failure probability
> If the composer calls three services in sequence with 99.5% availability each, the composition succeeds only ~98.5% of the time — the weakest link multiplied. Parallelize independent calls, set budgets, and decide per call whether failure degrades the answer (skip recommendations) or invalidates it (no order, no answer). A composer without per-call timeouts turns one slow service into a broken endpoint.

> [!tip] Interview answer
> API composition answers cross-service queries with a composer — usually the gateway or a BFF — that calls each owning service and joins the results in memory. It's the natural companion of database-per-service: simple, no extra store, great for per-entity views. Its limits are fan-out latency, big in-memory joins and the multiplied availability of the calls involved — for heavy cross-entity queries I move to event-fed read models instead.
