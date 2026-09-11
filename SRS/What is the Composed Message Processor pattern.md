<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging #SRS

# What is the Composed Message Processor pattern?

> [!abstract] Short answer
> A **Composed Message Processor** handles one composite message end to end: it **splits** the message into sub-messages, **routes** each to the destination that processes it, and **re-aggregates** the responses back into a single message — a split, a router, and an aggregator composed into one unit.

## Split, route per item, aggregate back

The order flow again: an order arrives with line items, each item needs an inventory check against its own inventory system, and only after **all** items are verified does the validated order move on. Neither a [[What is the Splitter pattern]] nor an [[What is the Aggregator pattern]] alone maintains that overall flow — the composition does: split the order into item messages, use a [[What is the Content-Based Router pattern]] to send each item to the right inventory system, and feed every response into an Aggregator keyed to the order. Each processing unit replies with the stock status for its item; once the aggregator's completeness condition is satisfied, it publishes the single reconciled order message onward. In practice this composition appears as one framework component — Camel's `split` + `aggregate` completion strategy, Spring Integration's `scatter-gather`-style chains — rather than three separately deployed boxes; the routing leg is content-based, the reconciliation leg is an [[What is the Aggregator pattern]] with its correlation, completeness, and algorithm choices.

```d2
direction: down
ord: "Order
3 line items" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
sp: "Split" {
  width: 110
  height: 45
  style.fill: "#fff3e0"
}
rt: "Route per item
(content-based)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
s1: "Inventory A" {
  width: 150
  height: 50
  style.fill: "#e8f5e9"
}
s2: "Inventory B" {
  width: 150
  height: 50
  style.fill: "#e8f5e9"
}
ag: "Aggregate
responses -> one order" {
  width: 240
  height: 65
  style.fill: "#fff3e0"
}
out: "Validated order" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
ord -> sp -> rt
rt -> s1
rt -> s2
s1 -> ag
s2 -> ag
ag -> out
```

**Fig. 1.** One composite in, per-item processing in the middle, one reconciled message out — the flow never forks permanently.

## The three legs as one flow

```java
from("orders.incoming")
    .split(simple("${body.items}"))
        .choice()                                  // route each item
            .when(simple("${body.type} == 'food'")).to("inv.perishables")
            .otherwise().to("inv.general")
        .end()
    .aggregate(header("orderId"), new OrderCheckStrategy())  // re-aggregate
        .completionSize(header("itemCount"))
    .to("orders.validated");
```

**Listing 1.** The same route expresses all three legs: split, content-based fan-out, and an aggregator completed by the expected item count.

> [!warning] The composed flow is only as strong as its aggregator's failure policy
> One inventory system failing means one response never arrives — the whole order stalls at the aggregate step unless the completeness condition has a timeout or error path. And because sub-messages fan out to different systems, per-item redelivery can duplicate responses; the aggregator must dedup its inputs or the reconciled order double-counts stock checks.

> [!tip] Interview answer
> A Composed Message Processor is the split-route-aggregate composition: it breaks a composite message apart, routes each sub-message to the appropriate destination — usually content-based — and re-aggregates the responses into a single message before the flow continues. Frameworks expose it as split-plus-aggregate routes; its reliability hinges on the aggregator's completeness condition and dedup, since one missing or duplicated response breaks the reconciled result.
